document.addEventListener('DOMContentLoaded', () => {
    // ===== 0. GLOBAL VARIABLES ===============================================
    const API_BASE_URL = ''; // Use relative URLs for same-origin API
    let currentCipherType = 'caesar'; // Default cipher
    
    // ===== 1. UI ELEMENTS ===================================================
    const cipherTypeSelect = document.getElementById('cipher-type');
    const caesarControls = document.getElementById('caesar-controls');
    const monoControls = document.getElementById('mono-controls');
    const caesarDecryptControls = document.getElementById('caesar-decrypt-controls');
    const monoDecryptControls = document.getElementById('mono-decrypt-controls');
    const caesarInfo = document.getElementById('caesar-info');
    const monoInfo = document.getElementById('mono-info');
    const customKeyInput = document.getElementById('custom-key-input');
    const keyMappingsContainer = document.getElementById('key-mappings');
    
    // ===== 2. TAB SWITCHING ==================================================
    const tabs = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.add('active');
        });
    });

    // ===== 3. CIPHER TYPE SWITCHING =========================================
    cipherTypeSelect.addEventListener('change', () => {
        currentCipherType = cipherTypeSelect.value;
        updateCipherInterface();
    });
    
    function updateCipherInterface() {
        // Update encryption controls
        if (currentCipherType === 'caesar') {
            caesarControls.style.display = 'block';
            monoControls.style.display = 'none';
            caesarDecryptControls.style.display = 'block';
            monoDecryptControls.style.display = 'none';
            caesarInfo.style.display = 'block';
            monoInfo.style.display = 'none';
        } else {
            caesarControls.style.display = 'none';
            monoControls.style.display = 'block';
            caesarDecryptControls.style.display = 'none';
            monoDecryptControls.style.display = 'block';
            caesarInfo.style.display = 'none';
            monoInfo.style.display = 'block';
        }
    }
    
    // ===== 4. COPY-TO-CLIPBOARD =============================================
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

    // ===== 5. RANDOM SHIFT FOR CAESAR =======================================
    document.getElementById('random-shift').addEventListener('click', () => {
        const randomShift = Math.floor(Math.random() * 256);
        document.getElementById('caesar-shift').value = randomShift;
    });
    
    // ===== 6. KEY TYPE SELECTION FOR MONO ==================================
    const keyTypeRadios = document.querySelectorAll('input[name="key-type"]');
    keyTypeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            if (radio.value === 'custom') {
                customKeyInput.style.display = 'block';
            } else {
                customKeyInput.style.display = 'none';
            }
        });
    });
    
    // ===== 7. ADD CUSTOM KEY MAPPING =======================================
    document.getElementById('add-mapping').addEventListener('click', addKeyMapping);
    
    function addKeyMapping() {
        const mappingDiv = document.createElement('div');
        mappingDiv.className = 'key-mapping';
        
        mappingDiv.innerHTML = `
            <input type="text" class="from-char" maxlength="1" placeholder="a">
            <span class="key-mapping-arrow">→</span>
            <input type="text" class="to-char" maxlength="1" placeholder="x">
            <button class="remove-mapping">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        mappingDiv.querySelector('.remove-mapping').addEventListener('click', () => {
            mappingDiv.remove();
        });
        
        keyMappingsContainer.appendChild(mappingDiv);
    }
    
    // Add a few mappings by default
    for (let i = 0; i < 3; i++) {
        addKeyMapping();
    }
    
    // ===== 8. COLLECT CUSTOM KEY MAPPINGS =================================
    function collectCustomKeyMappings() {
        const key = {};
        const mappings = document.querySelectorAll('.key-mapping');
        
        mappings.forEach(mapping => {
            const fromChar = mapping.querySelector('.from-char').value;
            const toChar = mapping.querySelector('.to-char').value;
            
            if (fromChar && toChar) {
                key[fromChar] = toChar;
            }
        });
        
        return Object.keys(key).length > 0 ? key : null;
    }
    
    // ===== 9. ENCRYPT ====================================================
    document.getElementById('encrypt-btn').addEventListener('click', async () => {
        const plaintext = document.getElementById('plaintext').value;
        
        if (!plaintext) {
            alert('Please enter text to encrypt');
            return;
        }
        
        try {
            let response;
            
            if (currentCipherType === 'caesar') {
                const shift = parseInt(document.getElementById('caesar-shift').value);
                
                if (isNaN(shift) || shift < 0 || shift > 255) {
                    alert('Shift must be a number between 0 and 255');
                    return;
                }
                
                response = await fetch(`${API_BASE_URL}/caesar/encrypt`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: plaintext, shift }),
                });
                
                const data = await response.json();
                document.getElementById('encrypted-result').textContent = data.result;
                document.getElementById('encryption-key-display').textContent = 
                    JSON.stringify({ type: 'caesar', shift }, null, 2);
                
            } else { // Monoalphabetic
                const useCustomKey = document.querySelector('input[name="key-type"]:checked').value === 'custom';
                const substitution_key = useCustomKey ? collectCustomKeyMappings() : null;
                
                response = await fetch(`${API_BASE_URL}/monoalphabetic/encrypt`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: plaintext, substitution_key }),
                });
                
                const data = await response.json();
                document.getElementById('encrypted-result').textContent = data.result;
                document.getElementById('encryption-key-display').textContent = 
                    JSON.stringify({ type: 'monoalphabetic', key: data.key }, null, 2);
            }
            
        } catch (error) {
            alert('Encryption failed: ' + error.message);
        }
    });
    
    // ===== 10. DECRYPT ====================================================
    document.getElementById('decrypt-btn').addEventListener('click', async () => {
        const ciphertext = document.getElementById('ciphertext').value;
        
        if (!ciphertext) {
            alert('Please enter text to decrypt');
            return;
        }
        
        try {
            let response;
            
            if (currentCipherType === 'caesar') {
                const shift = parseInt(document.getElementById('caesar-decrypt-shift').value);
                
                if (isNaN(shift) || shift < 0 || shift > 255) {
                    alert('Shift must be a number between 0 and 255');
                    return;
                }
                
                response = await fetch(`${API_BASE_URL}/caesar/decrypt`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: ciphertext, shift }),
                });
                
            } else { // Monoalphabetic
                const keyInput = document.getElementById('key-input').value;
                let substitution_key;
                
                try {
                    substitution_key = JSON.parse(keyInput);
                    
                    // Check if it's wrapped in a metadata object
                    if (substitution_key.type === 'monoalphabetic' && substitution_key.key) {
                        substitution_key = substitution_key.key;
                    }
                    
                } catch (e) {
                    alert('Invalid key format. Please enter a valid JSON object.');
                    return;
                }
                
                response = await fetch(`${API_BASE_URL}/monoalphabetic/decrypt`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: ciphertext, substitution_key }),
                });
            }
            
            const data = await response.json();
            document.getElementById('decrypted-result').textContent = data.result;
            
        } catch (error) {
            alert('Decryption failed: ' + error.message);
        }
    });
    
    // ===== 11. ANALYZE/ATTACK CIPHERTEXT ====================================
    document.getElementById('attack-btn').addEventListener('click', async () => {
        const ciphertext = document.getElementById('attack-text').value;
        
        if (!ciphertext) {
            alert('Please enter text to analyze');
            return;
        }
        
        try {
            let response;
            
            if (currentCipherType === 'caesar') {
                response = await fetch(`${API_BASE_URL}/caesar/attack`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: ciphertext }),
                });
                
                const data = await response.json();
                displayCaesarAttackResults(data.results);
                
            } else { // Monoalphabetic
                response = await fetch(`${API_BASE_URL}/monoalphabetic/attack`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: ciphertext }),
                });
                
                const data = await response.json();
                displayMonoAttackResults(data.results);
            }
            
        } catch (error) {
            alert('Analysis failed: ' + error.message);
        }
    });
    
    function displayCaesarAttackResults(results) {
        const container = document.getElementById('attack-results');
        container.innerHTML = '';
        
        if (!results || results.length === 0) {
            container.innerHTML = '<div class="no-results">No analysis results found.</div>';
            return;
        }
        
        // Only show a subset of potential shifts for brevity
        const significantShifts = [1, 2, 3, 4, 5, 7, 8, 9, 10, 13, 16, 26, 32, 64, 128];
        const filteredResults = results.filter(r => significantShifts.includes(r.shift));
        
        for (const result of filteredResults) {
            const resultDiv = document.createElement('div');
            resultDiv.className = 'attack-result-item';
            
            resultDiv.innerHTML = `
                <div class="attack-result-header">
                    <h4>Shift: ${result.shift}</h4>
                    <button class="use-result-btn" data-shift="${result.shift}">
                        <i class="fas fa-check"></i> Use this
                    </button>
                </div>
                <div class="attack-result-content">
                    ${escapeHTML(result.decrypted.substring(0, 200))}${result.decrypted.length > 200 ? '...' : ''}
                </div>
            `;
            
            resultDiv.querySelector('.use-result-btn').addEventListener('click', () => {
                document.getElementById('ciphertext').value = document.getElementById('attack-text').value;
                document.getElementById('caesar-decrypt-shift').value = result.shift;
                
                // Switch to decrypt tab
                tabs.forEach(t => t.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));
                document.querySelector('[data-tab="decrypt"]').classList.add('active');
                document.getElementById('decrypt').classList.add('active');
            });
            
            container.appendChild(resultDiv);
        }
    }
    
    function displayMonoAttackResults(results) {
        const container = document.getElementById('attack-results');
        container.innerHTML = '';
        
        if (!results || results.length === 0) {
            container.innerHTML = '<div class="no-results">No analysis results found.</div>';
            return;
        }
        
        for (const result of results) {
            const resultDiv = document.createElement('div');
            resultDiv.className = 'attack-result-item';
            
            resultDiv.innerHTML = `
                <div class="attack-result-header">
                    <h4>${result.description}</h4>
                </div>
                <div class="attack-result-content">
                    <p>Most frequent letters: ${result.frequencies.substring(0, 10)}...</p>
                    <p class="frequency-note">In English, common letters are: E, T, A, O, I, N, S, H, R, D, L, U</p>
                </div>
            `;
            
            container.appendChild(resultDiv);
        }
        
        // Add a frequency attack helper
        const helperDiv = document.createElement('div');
        helperDiv.className = 'attack-result-item';
        helperDiv.innerHTML = `
            <div class="attack-result-header">
                <h4>Frequency Analysis Helper</h4>
            </div>
            <div class="attack-result-content">
                <p>Based on frequency analysis, try substituting common letters and test decryption.</p>
                <p>Consider building a partial key and testing incrementally.</p>
            </div>
        `;
        
        container.appendChild(helperDiv);
    }
    
    // ===== 12. HELPER FUNCTIONS ============================================
    function escapeHTML(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
    
    // ===== 13. INITIALIZE INTERFACE ==========================================
    updateCipherInterface();
});