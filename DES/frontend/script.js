document.addEventListener('DOMContentLoaded', () => {
    // ===== 0. TAB SWITCHING ==================================================
    const tabs        = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.add('active');
        });
    });

    // ===== 1. COPY-TO-CLIPBOARD =============================================
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const target = document.getElementById(btn.dataset.target);
            try {
                await navigator.clipboard.writeText(target.textContent);
                const icon = btn.querySelector('i');
                icon.className = 'fas fa-check';
                setTimeout(() => (icon.className = 'fas fa-copy'), 2000);
            } catch (err) {
                console.error('Failed to copy text:', err);
            }
        });
    });

    // ===== 2. RANDOM 64-BIT KEY (binary) =====================================
    document.getElementById('generate-key').addEventListener('click', () => {
        const key = Array.from({ length: 64 }, () =>
            Math.random() < 0.5 ? '0' : '1'
        ).join('');
        document.getElementById('encryption-key').value = key;
    });

    // ===== 3. ENCRYPT ========================================================
    document.getElementById('encrypt-btn').addEventListener('click', async () => {
        const plaintext = document.getElementById('plaintext').value;
        const key       = document.getElementById('encryption-key').value;

        if (!plaintext) {
            alert('Please enter text to encrypt');
            return;
        }
        if (key && !/^[01]{64}$/.test(key)) {
            alert('Key must be exactly 64 binary digits (0/1)');
            return;
        }

        try {
            const response = await fetch('/encrypt', {
                method : 'POST',
                headers: { 'Content-Type': 'application/json' },
                body   : JSON.stringify({ plaintext, key }),
            });

            const data = await response.json();
            if (data.error) throw new Error(data.error);

            document.getElementById('encrypted-result').textContent = data.encrypted;
            // also show the (possibly auto-generated) key
            document.getElementById('encryption-key').value = data.key;
        } catch (error) {
            alert('Encryption failed: ' + error.message);
        }
    });

    // ===== 4. DECRYPT ========================================================
    document.getElementById('decrypt-btn').addEventListener('click', async () => {
        const ciphertext = document.getElementById('ciphertext').value;
        const key        = document.getElementById('decryption-key').value;

        if (!ciphertext) { alert('Please enter text to decrypt'); return; }
        if (!key)        { alert('Please enter the decryption key'); return; }
        if (!/^[01]{64}$/.test(key)) {
            alert('Key must be exactly 64 binary digits (0/1)');
            return;
        }

        try {
            const response = await fetch('/decrypt', {
                method : 'POST',
                headers: { 'Content-Type': 'application/json' },
                body   : JSON.stringify({ ciphertext, key }),
            });

            const data = await response.json();
            if (data.error) throw new Error(data.error);

            document.getElementById('decrypted-result').textContent = data.decrypted;
        } catch (error) {
            alert('Decryption failed: ' + error.message);
        }
    });

    // ===== 5. INPUT MASK FOR BINARY KEYS =====================================
    document.querySelectorAll('#encryption-key, #decryption-key').forEach(input => {
        input.addEventListener('input', e => {
            e.target.value = e.target.value.replace(/[^01]/g, '').slice(0, 64);
        });
    });
});
