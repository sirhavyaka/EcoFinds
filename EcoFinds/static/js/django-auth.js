// Simple Django Authentication JavaScript
console.log('Django authentication script loaded');

// Add some basic form enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Add Bootstrap classes to Django form fields
    const formFields = document.querySelectorAll('input[type="text"], input[type="password"], input[type="email"]');
    formFields.forEach(field => {
        if (!field.classList.contains('form-control')) {
            field.classList.add('form-control');
        }
    });
    
    // Add form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                event.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    });
});

// Simple logout confirmation
function confirmLogout() {
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = '/auth/logout/';
    }
}
