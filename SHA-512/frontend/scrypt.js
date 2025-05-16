document.addEventListener('DOMContentLoaded', () => {
    // ===== 1. COPY-TO-CLIPBOARD =============================================
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const target = document.getElementById(btn.dataset.target);
            try {
                await navigator.clipboard.writeText(target.textContent);
                btn.textContent = '✓';
                setTimeout(() => (btn.textContent = '📋'), 2000);
            } catch (err) {
                console.error('Failed to copy text:', err);
            }
        });
    });

    // ===== 2. HASH FUNCTION ================================================
    document.getElementById('hash-btn').addEventListener('click', async () => {
        const message = document.getElementById('message').value;

        if (!message) {
            alert('Please enter text to hash');
            return;
        }

        try {
            const response = await fetch('/hash', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();
            if (data.error) throw new Error(data.error);

            document.getElementById('hash-result').textContent = data.digest;
        } catch (error) {
            alert('Hashing failed: ' + error.message);
        }
    });
});