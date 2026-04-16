document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('enrichment-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    
    const resultsContainer = document.getElementById('results-container');
    const errorContainer = document.getElementById('error-container');
    const emailList = document.getElementById('email-list');
    const tierBadge = document.getElementById('tier-badge');
    const errorMsg = document.getElementById('error-msg');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Hide previous results
        resultsContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        emailList.innerHTML = '';
        
        // Loading state
        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
        submitBtn.disabled = true;

        const firstName = document.getElementById('first-name').value;
        const lastName = document.getElementById('last-name').value;
        const domain = document.getElementById('domain').value;

        try {
            const response = await fetch('/api/find_email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    first_name: firstName,
                    last_name: lastName,
                    domain: domain
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch data');
            }

            renderResults(data);
        } catch (error) {
            errorMsg.textContent = error.message;
            errorContainer.classList.remove('hidden');
        } finally {
            // Revert loading state
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });

    function renderResults(data) {
        // Setup tier badge
        tierBadge.className = 'tier-badge'; // reset
        
        if (data.tier === 1) {
            tierBadge.textContent = 'Tier 1 • Exact Match';
            tierBadge.classList.add('tier-1-badge');
            resultsContainer.style.borderTopColor = 'var(--tier-1)';
        } else if (data.tier === 2) {
            tierBadge.textContent = 'Tier 2 • Pattern Deduced';
            tierBadge.classList.add('tier-2-badge');
            resultsContainer.style.borderTopColor = 'var(--tier-2)';
        } else {
            tierBadge.textContent = 'Tier 3 • Mathematically Generated';
            tierBadge.classList.add('tier-3-badge');
            resultsContainer.style.borderTopColor = 'var(--tier-3)';
        }

        // Render emails
        const emailsToRender = data.email ? [data.email] : data.emails;
        
        emailsToRender.forEach(email => {
            const div = document.createElement('div');
            div.className = 'email-item';
            div.innerHTML = `
                <span>${email}</span>
                <button class="copy-btn" title="Copy to clipboard">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                </button>
            `;
            
            // Add copy functionality
            const copyBtn = div.querySelector('.copy-btn');
            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(email);
                copyBtn.innerHTML = `
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                `;
                setTimeout(() => {
                    if(div.isConnected) { // if not removed
                        copyBtn.innerHTML = `
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                            </svg>
                        `;
                    }
                }, 2000);
            });
            
            emailList.appendChild(div);
        });

        resultsContainer.classList.remove('hidden');
    }
});
