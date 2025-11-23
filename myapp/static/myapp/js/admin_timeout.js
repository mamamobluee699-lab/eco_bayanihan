// Admin Session Timeout Handler
// Warns user 1 minute before timeout and redirects after 5 minutes of inactivity

let timeoutTimer;
let warningTimer;
const INACTIVITY_LIMIT = 5 * 60 * 1000; // 5 minutes in milliseconds
const WARNING_TIME = 1 * 60 * 1000; // 1 minute warning

function resetTimers() {
    clearTimeout(timeoutTimer);
    clearTimeout(warningTimer);
    
    // Set warning timer (4 minutes from now)
    warningTimer = setTimeout(showWarning, INACTIVITY_LIMIT - WARNING_TIME);
    
    // Set timeout timer (5 minutes from now)
    timeoutTimer = setTimeout(handleTimeout, INACTIVITY_LIMIT);
}

function showWarning() {
    // Create warning modal
    const modalHtml = `
        <div class="modal fade" id="timeoutWarningModal" tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-warning text-dark">
                        <h5 class="modal-title">
                            <span class="bi bi-exclamation-triangle-fill"></span> Session Timeout Warning
                        </h5>
                    </div>
                    <div class="modal-body">
                        <p>Your admin session will expire in <strong>1 minute</strong> due to inactivity.</p>
                        <p>Please click "Continue Session" to stay logged in, or you will be automatically logged out.</p>
                        <div class="progress">
                            <div class="progress-bar bg-warning progress-bar-striped progress-bar-animated" 
                                 role="progressbar" style="width: 0%" id="timeoutProgress"></div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" onclick="continueSession()">
                            <span class="bi bi-clock"></span> Continue Session
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="logoutNow()">
                            <span class="bi bi-box-arrow-right"></span> Logout Now
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if present
    const existingModal = document.getElementById('timeoutWarningModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('timeoutWarningModal'));
    modal.show();
    
    // Start progress bar animation
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 100 / 60; // Update every second for 60 seconds
        document.getElementById('timeoutProgress').style.width = progress + '%';
        
        if (progress >= 100) {
            clearInterval(progressInterval);
        }
    }, 1000);
}

function continueSession() {
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('timeoutWarningModal'));
    if (modal) {
        modal.hide();
    }
    
    // Reset timers
    resetTimers();
    
    // Show success message
    showNotification('Session extended!', 'success');
}

function logoutNow() {
    window.location.href = '/admin/logout/';
}

function handleTimeout() {
    showNotification('Session expired due to inactivity. Redirecting to login...', 'warning');
    setTimeout(() => {
        window.location.href = '/admin/login/';
    }, 2000);
}

function showNotification(message, type = 'info') {
    const notificationHtml = `
        <div class="alert alert-${type} alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            <span class="bi bi-info-circle"></span> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', notificationHtml);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

// Track user activity
function trackActivity() {
    resetTimers();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Only activate on admin pages
    if (window.location.pathname.includes('admin') || window.location.pathname.includes('custom_admin')) {
        resetTimers();
        
        // Track various user activities
        const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
        events.forEach(event => {
            document.addEventListener(event, trackActivity, true);
        });
        
        // Track window focus/blur
        window.addEventListener('focus', trackActivity);
        window.addEventListener('blur', trackActivity);
        
        // Clean up on page unload
        window.addEventListener('beforeunload', function() {
            clearTimeout(timeoutTimer);
            clearTimeout(warningTimer);
        });
    }
});
