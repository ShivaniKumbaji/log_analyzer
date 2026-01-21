// DOM Elements
const uploadForm = document.getElementById('uploadForm');
const logFileInput = document.getElementById('logFile');
const fileNameDisplay = document.getElementById('fileName');
const analyzeBtn = document.getElementById('analyzeBtn');
const analyzeDefaultBtn = document.getElementById('analyzeDefaultBtn');
const loadingDiv = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const errorMessageDiv = document.getElementById('errorMessage');
const errorTitle = document.getElementById('errorTitle');
const errorText = document.getElementById('errorText');
const progressBar = document.getElementById('progressBar');
const progressText = document.getElementById('progressText');

// Chart instances
let errorChartInstance = null;
let ipChartInstance = null;

// Event Listeners
logFileInput.addEventListener('change', function() {
    if (this.files.length > 0) {
        fileNameDisplay.textContent = this.files[0].name;
        fileNameDisplay.style.color = '#28a745';
        fileNameDisplay.innerHTML = `<i class="fas fa-check-circle"></i> ${this.files[0].name}`;
    } else {
        fileNameDisplay.textContent = 'No file chosen';
        fileNameDisplay.style.color = '#666';
    }
});

uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (logFileInput.files.length === 0) {
        showError('No File Selected', 'Please choose a log file to analyze.');
        return;
    }
    
    const formData = new FormData();
    formData.append('log_file', logFileInput.files[0]);
    
    await analyzeFile(formData);
});

analyzeDefaultBtn.addEventListener('click', async function() {
    await analyzeDefaultFile();
});

// Functions
async function analyzeFile(formData) {
    showLoading();
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            displayResults(data);
        } else {
            showError('Analysis Failed', data.message || 'Unknown error occurred');
        }
    } catch (error) {
        showError('Network Error', 'Could not connect to the server. Please try again.');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

async function analyzeDefaultFile() {
    showLoading();
    
    try {
        const response = await fetch('/analyze/default');
        const data = await response.json();
        
        if (data.status === 'success') {
            displayResults(data);
        } else {
            showError('Analysis Failed', data.message || 'Unknown error occurred');
        }
    } catch (error) {
        showError('Network Error', 'Could not connect to the server. Please try again.');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

function displayResults(data) {
    // Update summary cards
    updateSummaryCards(data);
    
    // Create charts
    createErrorChart(data.error_codes);
    createIPChart(data.top_ips);
    
    // Update tables
    updateErrorTable(data.error_codes, data.error_requests);
    updateIPTable(data.top_ips, data.error_requests);
    
    // Update download links
    updateDownloadLinks(data);
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function updateSummaryCards(data) {
    const summaryCards = document.getElementById('summaryCards');
    
    const cards = [
        {
            icon: 'fa-file-lines',
            title: 'Total Lines',
            value: data.total_lines.toLocaleString(),
            label: 'Processed'
        },
        {
            icon: 'fa-chart-line',
            title: 'Success Rate',
            value: `${data.success_rate.toFixed(2)}%`,
            label: 'Parsing Accuracy'
        },
        {
            icon: 'fa-triangle-exclamation',
            title: 'Error Requests',
            value: data.error_requests.toLocaleString(),
            label: `${data.error_percentage.toFixed(2)}% of total`
        },
        {
            icon: 'fa-network-wired',
            title: 'Unique IPs',
            value: data.unique_ips.toLocaleString(),
            label: `${data.unique_error_ips} with errors`
        }
    ];
    
    summaryCards.innerHTML = cards.map(card => `
        <div class="summary-card">
            <i class="fas ${card.icon}"></i>
            <h3>${card.title}</h3>
            <div class="value">${card.value}</div>
            <div class="label">${card.label}</div>
        </div>
    `).join('');
}

function createErrorChart(errorCodes) {
    const ctx = document.getElementById('errorChart').getContext('2d');
    
    // Destroy previous chart if exists
    if (errorChartInstance) {
        errorChartInstance.destroy();
    }
    
    const labels = Object.keys(errorCodes);
    const data = Object.values(errorCodes);
    
    // Generate colors
    const colors = labels.map((_, index) => {
        const hue = (index * 137) % 360; // Golden angle for color distribution
        return `hsl(${hue}, 70%, 60%)`;
    });
    
    errorChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Error Count',
                data: data,
                backgroundColor: colors,
                borderColor: colors.map(color => color.replace('60%)', '50%)')),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'HTTP Error Code Distribution',
                    font: {
                        size: 16
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Error Count'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'HTTP Error Code'
                    }
                }
            }
        }
    });
}

function createIPChart(topIPs) {
    const ctx = document.getElementById('ipChart').getContext('2d');
    
    // Destroy previous chart if exists
    if (ipChartInstance) {
        ipChartInstance.destroy();
    }
    
    const labels = Object.keys(topIPs);
    const data = Object.values(topIPs);
    
    ipChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Error Count',
                data: data,
                backgroundColor: 'rgba(255, 99, 132, 0.7)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Top IP Addresses with Errors',
                    font: {
                        size: 16
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Error Count'
                    }
                }
            }
        }
    });
}

function updateErrorTable(errorCodes, totalErrors) {
    const tbody = document.querySelector('#errorTable tbody');
    
    // Sort by count descending
    const sortedCodes = Object.entries(errorCodes)
        .sort(([, a], [, b]) => b - a);
    
    tbody.innerHTML = sortedCodes.map(([code, count]) => {
        const percentage = ((count / totalErrors) * 100).toFixed(2);
        return `
            <tr>
                <td><span class="badge badge-error">HTTP ${code}</span></td>
                <td>${count.toLocaleString()}</td>
                <td>${percentage}%</td>
            </tr>
        `;
    }).join('');
}

function updateIPTable(topIPs, totalErrors) {
    const tbody = document.querySelector('#ipTable tbody');
    
    // Sort by count descending
    const sortedIPs = Object.entries(topIPs)
        .sort(([, a], [, b]) => b - a);
    
    tbody.innerHTML = sortedIPs.map(([ip, count]) => {
        const percentage = ((count / totalErrors) * 100).toFixed(2);
        return `
            <tr>
                <td><code>${ip}</code></td>
                <td>${count.toLocaleString()}</td>
                <td>${percentage}%</td>
            </tr>
        `;
    }).join('');
}

function updateDownloadLinks(data) {
    const downloadLinks = document.getElementById('downloadLinks');
    
    const links = [
        {
            icon: 'fa-file-text',
            text: 'Download Report',
            url: data.report,
            filename: 'summary_report.txt'
        },
        {
            icon: 'fa-chart-bar',
            text: 'Error Chart',
            url: data.charts.error_distribution,
            filename: 'error_distribution.png'
        },
        {
            icon: 'fa-server',
            text: 'IP Analysis Chart',
            url: data.charts.top_ips,
            filename: 'top_ips.png'
        }
    ];
    
    downloadLinks.innerHTML = links.map(link => `
        <a href="${link.url}" class="download-link" download="${link.filename}">
            <i class="fas ${link.icon}"></i>
            <span>${link.text}</span>
        </a>
    `).join('');
}

function showLoading() {
    loadingDiv.style.display = 'block';
    resultsSection.style.display = 'none';
    analyzeBtn.disabled = true;
    analyzeDefaultBtn.disabled = true;
    
    // Simulate progress bar
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 10;
        if (progress > 90) {
            clearInterval(interval);
            progressBar.style.width = '100%';
            progressText.textContent = 'Finalizing analysis...';
        } else {
            progressBar.style.width = `${progress}%`;
            progressText.textContent = `Processing... ${Math.floor(progress)}%`;
        }
    }, 200);
}

function hideLoading() {
    loadingDiv.style.display = 'none';
    analyzeBtn.disabled = false;
    analyzeDefaultBtn.disabled = false;
    progressBar.style.width = '0%';
    progressText.textContent = 'Processing...';
}

function showError(title, message) {
    errorTitle.textContent = title;
    errorText.textContent = message;
    errorMessageDiv.style.display = 'flex';
}

function hideError() {
    errorMessageDiv.style.display = 'none';
}

// Close error message when clicking outside
errorMessageDiv.addEventListener('click', function(e) {
    if (e.target === this) {
        hideError();
    }
});

// Check server status on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch('/status');
        const data = await response.json();
        console.log('Server status:', data);
    } catch (error) {
        console.log('Server not responding, but frontend is loaded');
    }
});