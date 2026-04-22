// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const extractBtn = document.getElementById('extractBtn');
const extractTableBtn = document.getElementById('extractTableBtn');
const extractAllBtn = document.getElementById('extractAllBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const textResults = document.getElementById('textResults');
const tableResults = document.getElementById('tableResults');
const comprehensiveResults = document.getElementById('comprehensiveResults');

let selectedFile = null;
let currentPageIndex = 0;
let extractedData = null;

// Upload Box Click
uploadBox.addEventListener('click', () => fileInput.click());

// File Input Change
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

// Drag and Drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    
    const file = e.dataTransfer.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

// Handle File Selection
function handleFileSelect(file) {
    const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/bmp', 'image/tiff'];
    
    if (!allowedTypes.some(type => file.type.includes(type.split('/')[1]) || file.name.endsWith('.pdf'))) {
        showError('Please upload a PDF or image file (PDF, PNG, JPG, BMP, TIFF)');
        return;
    }
    
    if (file.size > 50 * 1024 * 1024) {
        showError('File size exceeds 50MB limit');
        return;
    }
    
    selectedFile = file;
    
    // Update UI
    uploadBox.innerHTML = `
        <div style="font-size: 2em; margin-bottom: 10px;">✓</div>
        <h2>File Selected</h2>
        <p>${file.name}</p>
        <p style="font-size: 0.9em; color: #999; margin-top: 5px;">${(file.size / 1024).toFixed(2)} KB</p>
    `;
    
    extractBtn.disabled = false;
    extractTableBtn.disabled = false;
    extractAllBtn.disabled = false;
    
    dismissError();
}

// Extract Text
extractBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    await extractData('/api/extract', formData, 'text');
});

// Extract Tables
extractTableBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    await extractData('/api/extract-tables', formData, 'table');
});

// Extract Everything
extractAllBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    await extractData('/api/extract-all', formData, 'all');
});

// Extract Data Function
async function extractData(endpoint, formData, type) {
    try {
        loading.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        errorSection.classList.add('hidden');
        
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        loading.classList.add('hidden');
        
        if (!response.ok || !data.success) {
            showError(data.error || 'Failed to extract data');
            return;
        }
        
        displayResults(data, type);
        
    } catch (error) {
        loading.classList.add('hidden');
        showError('Error: ' + error.message);
    }
}

// Display Results
function displayResults(data, type) {
    // Update file info
    document.getElementById('fileName').textContent = selectedFile.name;
    document.getElementById('pageCount').textContent = data.pages || data.total_pages || 1;
    
    // Hide all result types first
    textResults.classList.add('hidden');
    tableResults.classList.add('hidden');
    comprehensiveResults.classList.add('hidden');
    
    if (type === 'text') {
        displayTextResults(data);
    } else if (type === 'table') {
        displayTableResults(data);
    } else if (type === 'all') {
        displayComprehensiveResults(data);
    }
    
    resultsSection.classList.remove('hidden');
    errorSection.classList.add('hidden');
}

// Display Text Results
function displayTextResults(data) {
    const textOutput = document.getElementById('textOutput');
    textOutput.textContent = data.text;
    textResults.classList.remove('hidden');
}

// Display Table Results
function displayTableResults(data) {
    const tableOutput = document.getElementById('tableOutput');
    tableOutput.innerHTML = '';
    
    if (!data.tables || data.tables.length === 0) {
        tableOutput.innerHTML = '<p>No tables found in the PDF</p>';
        tableResults.classList.remove('hidden');
        return;
    }
    
    data.tables.forEach(table => {
        const pageHeader = document.createElement('div');
        pageHeader.className = 'page-header';
        pageHeader.textContent = `Page ${table.page}`;
        tableOutput.appendChild(pageHeader);
        
        const tableElement = document.createElement('table');
        
        // Create rows
        table.rows.forEach((row, index) => {
            const tr = document.createElement('tr');
            row.forEach(cell => {
                const td = document.createElement(index === 0 ? 'th' : 'td');
                td.textContent = cell.trim();
                tr.appendChild(td);
            });
            tableElement.appendChild(tr);
        });
        
        tableOutput.appendChild(tableElement);
    });
    
    tableResults.classList.remove('hidden');
}

// Display Comprehensive Results
function displayComprehensiveResults(data) {
    extractedData = data;
    currentPageIndex = 0;
    
    // Display metadata
    displayMetadata(data.metadata);
    
    // Display statistics
    displayStatistics(data);
    
    // Display pages
    if (data.pages && data.pages.length > 0) {
        displayCurrentPage();
    }
    
    comprehensiveResults.classList.remove('hidden');
}

// Display Metadata
function displayMetadata(metadata) {
    const metadataOutput = document.getElementById('metadataOutput');
    metadataOutput.innerHTML = '';
    
    if (!metadata || Object.keys(metadata).length === 0) {
        document.getElementById('metadataSection').classList.add('hidden');
        return;
    }
    
    for (const [key, value] of Object.entries(metadata)) {
        const item = document.createElement('div');
        item.className = 'metadata-item';
        item.innerHTML = `<strong>${formatKey(key)}:</strong><span>${String(value).substring(0, 100)}</span>`;
        metadataOutput.appendChild(item);
    }
    
    document.getElementById('metadataSection').classList.remove('hidden');
}

// Display Statistics
function displayStatistics(data) {
    const statsOutput = document.getElementById('statisticsOutput');
    statsOutput.innerHTML = '';
    
    // Overall stats
    const stats = [
        { label: 'Total Pages', value: data.total_pages },
        { label: 'File Size (MB)', value: data.file_size_mb ? data.file_size_mb.toFixed(2) : 'N/A' },
    ];
    
    // Aggregate page statistics
    if (data.pages && data.pages.length > 0) {
        let totalText = 0;
        let totalLines = 0;
        let totalTables = 0;
        
        data.pages.forEach(page => {
            if (page.statistics) {
                totalText += page.statistics.text_length || 0;
                totalLines += page.statistics.lines || 0;
                totalTables += page.statistics.tables_count || 0;
            }
        });
        
        stats.push({ label: 'Total Text Length', value: totalText });
        stats.push({ label: 'Total Lines', value: totalLines });
        stats.push({ label: 'Tables Found', value: totalTables });
    }
    
    stats.forEach(stat => {
        const card = document.createElement('div');
        card.className = 'stat-card';
        card.innerHTML = `
            <div class="stat-value">${stat.value}</div>
            <div class="stat-label">${stat.label}</div>
        `;
        statsOutput.appendChild(card);
    });
    
    document.getElementById('statisticsSection').classList.remove('hidden');
}

// Display Current Page
function displayCurrentPage() {
    if (!extractedData || !extractedData.pages || extractedData.pages.length === 0) return;
    
    const page = extractedData.pages[currentPageIndex];
    document.getElementById('pageIndicator').textContent = `Page ${currentPageIndex + 1} of ${extractedData.pages.length}`;
    
    // Show/hide navigation buttons
    document.getElementById('prevPageBtn').disabled = currentPageIndex === 0;
    document.getElementById('nextPageBtn').disabled = currentPageIndex === extractedData.pages.length - 1;
    
    // Display page image
    if (page.image) {
        const pageImageEl = document.getElementById('pageImageEl');
        pageImageEl.src = page.image;
        document.getElementById('pageImage').classList.remove('hidden');
    } else {
        document.getElementById('pageImage').classList.add('hidden');
    }
    
    // Display page text
    if (page.text) {
        document.getElementById('pageTextOutput').textContent = page.text;
        document.getElementById('pageText').classList.remove('hidden');
    } else {
        document.getElementById('pageText').classList.add('hidden');
    }
    
    // Display page table
    if (page.tables && page.tables.length > 0) {
        const pageTableOutput = document.getElementById('pageTableOutput');
        pageTableOutput.innerHTML = '';
        
        const table = document.createElement('table');
        page.tables.forEach((row, index) => {
            const tr = document.createElement('tr');
            row.forEach(cell => {
                const td = document.createElement(index === 0 ? 'th' : 'td');
                td.textContent = cell;
                tr.appendChild(td);
            });
            table.appendChild(tr);
        });
        
        pageTableOutput.appendChild(table);
        document.getElementById('pageTable').classList.remove('hidden');
    } else {
        document.getElementById('pageTable').classList.add('hidden');
    }
    
    document.getElementById('pagesSection').classList.remove('hidden');
}

// Page Navigation
document.getElementById('prevPageBtn').addEventListener('click', () => {
    if (currentPageIndex > 0) {
        currentPageIndex--;
        displayCurrentPage();
    }
});

document.getElementById('nextPageBtn').addEventListener('click', () => {
    if (extractedData && currentPageIndex < extractedData.pages.length - 1) {
        currentPageIndex++;
        displayCurrentPage();
    }
});

// Download Functions
document.getElementById('downloadJsonBtn').addEventListener('click', () => {
    if (!extractedData) return;
    const json = JSON.stringify(extractedData, null, 2);
    downloadFile(json, selectedFile.name.replace(/\.[^/.]+$/, '') + '_extracted.json', 'application/json');
});

document.getElementById('downloadTextBtn').addEventListener('click', () => {
    if (!extractedData || !extractedData.pages) return;
    let text = '';
    extractedData.pages.forEach((page, idx) => {
        text += `\n========== PAGE ${idx + 1} ==========\n\n`;
        text += page.text;
    });
    downloadFile(text, selectedFile.name.replace(/\.[^/.]+$/, '') + '_extracted.txt', 'text/plain');
});

document.getElementById('downloadCsvBtn').addEventListener('click', () => {
    if (!extractedData || !extractedData.pages) return;
    let csv = 'Page,Text_Length,Lines,Tables_Count\n';
    extractedData.pages.forEach((page, idx) => {
        csv += `${idx + 1},"${page.statistics.text_length}","${page.statistics.lines}","${page.statistics.tables_count}"\n`;
    });
    downloadFile(csv, selectedFile.name.replace(/\.[^/.]+$/, '') + '_statistics.csv', 'text/csv');
});

// Helper function to download files
function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Helper function to format metadata keys
function formatKey(key) {
    return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Show Error
function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorSection.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    loading.classList.add('hidden');
}

// Dismiss Error
function dismissError() {
    errorSection.classList.add('hidden');
}

// Button Handlers
document.getElementById('dismissError').addEventListener('click', dismissError);

document.getElementById('clearBtn').addEventListener('click', () => {
    selectedFile = null;
    extractedData = null;
    currentPageIndex = 0;
    fileInput.value = '';
    uploadBox.innerHTML = `
        <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
        </svg>
        <h2>Drop your PDF here</h2>
        <p>or click to browse</p>
    `;
    resultsSection.classList.add('hidden');
    extractBtn.disabled = true;
    extractTableBtn.disabled = true;
    extractAllBtn.disabled = true;
});

document.getElementById('copyBtn').addEventListener('click', () => {
    const textOutput = document.getElementById('textOutput');
    if (textOutput.textContent) {
        navigator.clipboard.writeText(textOutput.textContent).then(() => {
            alert('Text copied to clipboard!');
        });
    }
});

document.getElementById('downloadBtn').addEventListener('click', () => {
    const textOutput = document.getElementById('textOutput');
    if (textOutput.textContent) {
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(textOutput.textContent));
        element.setAttribute('download', selectedFile.name.replace(/\.[^/.]+$/, '') + '_extracted.txt');
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
});
