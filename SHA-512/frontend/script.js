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
                alert('Failed to copy: ' + err.message);
            }
        });
    });

    // ===== 2. HASH FUNCTION ================================================
    document.getElementById('hash-btn').addEventListener('click', async () => {
        const hashResult = document.getElementById('hash-result');
        const message = document.getElementById('message').value;
        const hashBtn = document.getElementById('hash-btn');

        if (!message) {
            hashResult.textContent = 'Please enter text to hash';
            return;
        }

        try {
            // Show loading state
            hashBtn.disabled = true;
            hashBtn.textContent = 'Processing...';
            hashResult.textContent = 'Computing hash...';
            
            console.log('Sending request to /hash with message:', message);
            
            const response = await fetch('/hash', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message }),
            });
            
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Response data:', data);
            
            if (data.error) throw new Error(data.error);

            hashResult.textContent = data.digest;
        } catch (error) {
            console.error('Error during hash operation:', error);
            hashResult.textContent = 'Error: ' + error.message;
        } finally {
            // Reset button state
            hashBtn.disabled = false;
            hashBtn.textContent = '🔐 Generate Hash';
        }
    });
});