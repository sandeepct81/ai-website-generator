// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const promptInput = document.getElementById('promptInput');
const generateBtn = document.getElementById('generateBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const previewSection = document.getElementById('previewSection');
const previewFrame = document.getElementById('previewFrame');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const projectsList = document.getElementById('projectsList');
const downloadBtn = document.getElementById('downloadBtn');
const copyBtn = document.getElementById('copyBtn');

// Current generated code
let currentGeneratedCode = '';

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
});

generateBtn.addEventListener('click', generateWebsite);
downloadBtn.addEventListener('click', downloadWebsite);
copyBtn.addEventListener('click', copyToClipboard);

// Generate Website Function
async function generateWebsite() {
    const prompt = promptInput.value.trim();
    
    if (!prompt) {
        showError('Please enter a prompt first!');
        return;
    }
    
    // Show loading, hide previous results
    loadingSpinner.classList.remove('hidden');
    previewSection.classList.add('hidden');
    errorMessage.classList.add('hidden');
    generateBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Store and display generated code
        currentGeneratedCode = data.generated_code;
        displayPreview(currentGeneratedCode);
        
        // Refresh projects list
        loadProjects();
        
    } catch (error) {
        showError('Failed to generate website. Please try again.');
        console.error('Error:', error);
    } finally {
        loadingSpinner.classList.add('hidden');
        generateBtn.disabled = false;
    }
}

// Display Preview
function displayPreview(htmlCode) {
    // Create a blob and object URL for the iframe
    const blob = new Blob([htmlCode], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    
    // Set iframe source
    previewFrame.src = url;
    
    // Show preview section
    previewSection.classList.remove('hidden');
    
    // Clean up object URL after iframe loads
    previewFrame.onload = () => URL.revokeObjectURL(url);
}

// Download Website
function downloadWebsite() {
    if (!currentGeneratedCode) {
        showError('No website generated yet!');
        return;
    }
    
    // Create download link
    const blob = new Blob([currentGeneratedCode], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'generated-website.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Copy to Clipboard
async function copyToClipboard() {
    if (!currentGeneratedCode) {
        showError('No website generated yet!');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(currentGeneratedCode);
        alert('Code copied to clipboard!');
    } catch (err) {
        showError('Failed to copy code');
    }
}

// Load Projects from Database
async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE_URL}/projects`);
        const projects = await response.json();
        
        displayProjects(projects);
    } catch (error) {
        console.error('Error loading projects:', error);
        projectsList.innerHTML = '<div class="loading-projects">Failed to load projects</div>';
    }
}

// Display Projects
function displayProjects(projects) {
    if (projects.length === 0) {
        projectsList.innerHTML = '<div class="loading-projects">No projects yet. Generate your first website!</div>';
        return;
    }
    
    projectsList.innerHTML = projects.map(project => `
        <div class="project-card" onclick="loadProject(${project.id})">
            <h3>${escapeHtml(project.prompt.substring(0, 50))}${project.prompt.length > 50 ? '...' : ''}</h3>
            <p>${escapeHtml(project.prompt)}</p>
            <div class="project-date">${new Date(project.created_at).toLocaleString()}</div>
            <button class="delete-project" onclick="deleteProject(${project.id}, event)">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `).join('');
}

// Load Specific Project
window.loadProject = async function(projectId) {
    try {
        loadingSpinner.classList.remove('hidden');
        
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}`);
        const project = await response.json();
        
        currentGeneratedCode = project.generated_code;
        displayPreview(currentGeneratedCode);
        
    } catch (error) {
        showError('Failed to load project');
    } finally {
        loadingSpinner.classList.add('hidden');
    }
};

// Delete Project
window.deleteProject = async function(projectId, event) {
    event.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this project?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadProjects(); // Refresh list
        }
    } catch (error) {
        showError('Failed to delete project');
    }
};

// Helper Functions
function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}