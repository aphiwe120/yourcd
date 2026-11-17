/**
 * Medical Coding Assistant - Frontend Application
 * Doctor-friendly interface for ICD-10 code lookup
 */

const API_BASE = '/api';

// DOM Elements
const queryForm = document.getElementById('queryForm');
const questionInput = document.getElementById('question');
const askBtn = document.getElementById('askBtn');
const loadingDiv = document.getElementById('loading');
const resultsSection = document.getElementById('results');
const answerText = document.getElementById('answer-text');
const codesContainer = document.getElementById('codes-container');
const codesList = document.getElementById('codes-list');
const errorBox = document.getElementById('errorBox');
const errorText = document.getElementById('error-text');

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    attachEventListeners();
});

/**
 * Attach event listeners
 */
function attachEventListeners() {
    queryForm.addEventListener('submit', handleQuerySubmit);
}

/**
 * Handle query form submission
 */
async function handleQuerySubmit(event) {
    event.preventDefault();

    const question = questionInput.value.trim();
    if (!question) {
        showError('Please describe the patient diagnosis or symptoms');
        return;
    }

    await executeQuery(question);
}

/**
 * Execute a query against the backend
 */
async function executeQuery(question) {
    // Show loading state
    askBtn.disabled = true;
    loadingDiv.style.display = 'block';
    resultsSection.style.display = 'none';
    errorBox.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Query failed');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        showError(`Failed to retrieve codes: ${error.message}`);
    } finally {
        askBtn.disabled = false;
        loadingDiv.style.display = 'none';
    }
}

/**
 * Display query results for doctors
 */
function displayResults(data) {
    // Set answer text
    answerText.textContent = data.answer || 'No matching codes found';

    // Display codes if available
    if (data.rows && Array.isArray(data.rows) && data.rows.length > 0) {
        displayCodes(data.rows);
        codesContainer.style.display = 'block';
    } else {
        codesContainer.style.display = 'none';
    }

    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Display ICD-10 codes in doctor-friendly format
 */
function displayCodes(rows) {
    codesList.innerHTML = '';

    rows.forEach((row, index) => {
        const codeCard = document.createElement('div');
        codeCard.className = 'code-card';

        const header = document.createElement('div');
        header.className = 'code-card-header';

        const badge = document.createElement('div');
        badge.className = 'code-badge';
        badge.textContent = row.code || 'N/A';

        header.appendChild(badge);

        const description = document.createElement('div');
        description.className = 'code-description';
        description.textContent = row.description || row.full_desc || 'No description';

        const details = document.createElement('div');
        details.className = 'code-details';
        if (row.full_desc && row.full_desc !== row.description) {
            details.innerHTML = `<strong>Definition:</strong> ${escapeHtml(row.full_desc)}`;
        }

        codeCard.appendChild(header);
        codeCard.appendChild(description);
        if (details.textContent) {
            codeCard.appendChild(details);
        }

        codesList.appendChild(codeCard);
    });
}

/**
 * Show error message to doctor
 */
function showError(message) {
    errorBox.style.display = 'block';
    errorText.textContent = escapeHtml(message);
    resultsSection.style.display = 'none';

    errorBox.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Escape HTML special characters to prevent XSS
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

