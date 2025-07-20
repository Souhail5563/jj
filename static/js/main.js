// Main JavaScript for Bijoux Store

document.addEventListener('DOMContentLoaded', function() {
    // Initialize 3D effects
    init3DEffects();

    // Auto-hide alerts after 5 seconds with 3D animation
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert, index) {
        // Stagger the animation
        setTimeout(function() {
            alert.style.animation = 'slideIn3D 0.5s ease-out';
        }, index * 100);

        setTimeout(function() {
            alert.style.animation = 'slideOut3D 0.5s ease-in forwards';
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 500);
        }, 5000);
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
                e.preventDefault();
            }
        });
    });

    // Image preview for file uploads
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = document.getElementById('image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = 'image-preview';
                        preview.className = 'img-thumbnail mt-2';
                        preview.style.maxWidth = '200px';
                        input.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Quantity validation in cart
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const max = parseInt(this.getAttribute('max'));
            const value = parseInt(this.value);
            
            if (value > max) {
                alert(`Quantité maximale disponible: ${max}`);
                this.value = max;
            }
            
            if (value < 1) {
                this.value = 1;
            }
        });
    });

    // Search functionality (if implemented)
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const productCards = document.querySelectorAll('.product-card');
            
            productCards.forEach(function(card) {
                const productName = card.querySelector('.card-title').textContent.toLowerCase();
                const productDescription = card.querySelector('.card-text').textContent.toLowerCase();
                
                if (productName.includes(searchTerm) || productDescription.includes(searchTerm)) {
                    card.closest('.col-lg-3, .col-md-6, .col-lg-4').style.display = 'block';
                } else {
                    card.closest('.col-lg-3, .col-md-6, .col-lg-4').style.display = 'none';
                }
            });
        });
    }

    // Loading states for forms
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<span class="loading"></span> Traitement...';
                
                // Re-enable after 10 seconds as fallback
                setTimeout(function() {
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalText;
                }, 10000);
            }
        });
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Tooltip initialization
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Cart update functionality
    function updateCartQuantity(itemId, newQuantity) {
        fetch(`/update_cart_item/${itemId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                quantity: newQuantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Erreur lors de la mise à jour du panier');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Erreur lors de la mise à jour du panier');
        });
    }

    // Price formatting
    function formatPrice(price) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR'
        }).format(price);
    }

    // Stock status update
    function updateStockStatus() {
        const stockElements = document.querySelectorAll('[data-stock]');
        stockElements.forEach(function(element) {
            const stock = parseInt(element.getAttribute('data-stock'));
            const minStock = parseInt(element.getAttribute('data-min-stock') || 5);
            
            if (stock <= 0) {
                element.className = 'badge bg-danger';
                element.textContent = 'Rupture';
            } else if (stock <= minStock) {
                element.className = 'badge bg-warning';
                element.textContent = 'Stock bas';
            } else {
                element.className = 'badge bg-success';
                element.textContent = 'En stock';
            }
        });
    }

    // Initialize stock status
    updateStockStatus();

    // Admin dashboard charts (if Chart.js is loaded)
    if (typeof Chart !== 'undefined') {
        // Sales chart example
        const salesCtx = document.getElementById('salesChart');
        if (salesCtx) {
            new Chart(salesCtx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
                    datasets: [{
                        label: 'Ventes',
                        data: [12, 19, 3, 5, 2, 3],
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }
});

// 3D Effects Initialization
function init3DEffects() {
    // Add parallax effect to hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }

    // Add mouse tracking for 3D card effects
    const cards = document.querySelectorAll('.product-card, .category-card, .admin-card');
    cards.forEach(function(card) {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
        });

        card.addEventListener('mouseleave', function() {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
        });
    });

    // Add floating animation to specific elements
    const floatingElements = document.querySelectorAll('.navbar-brand .fas, .hero-section .btn');
    floatingElements.forEach(function(element) {
        element.classList.add('float-element');
    });

    // Add staggered animation to product cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(function(card, index) {
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Add staggered animation to category cards
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(function(card, index) {
        card.style.animationDelay = `${index * 0.2}s`;
    });

    // Add smooth scroll with 3D effect
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                // Add 3D transition effect
                document.body.style.transform = 'perspective(1000px) rotateX(2deg)';
                setTimeout(function() {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    document.body.style.transform = 'perspective(1000px) rotateX(0deg)';
                }, 100);
            }
        });
    });

    // Add 3D hover effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(function(button) {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.05)';
        });

        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add ripple effect to clickable elements
    const clickableElements = document.querySelectorAll('.btn, .card, .list-group-item');
    clickableElements.forEach(function(element) {
        element.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple-effect');

            this.appendChild(ripple);

            setTimeout(function() {
                ripple.remove();
            }, 600);
        });
    });
}

// Add CSS for ripple effect
const rippleCSS = `
.ripple-effect {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 215, 0, 0.6);
    transform: scale(0);
    animation: ripple 0.6s linear;
    pointer-events: none;
    z-index: 1000;
}

@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

@keyframes slideOut3D {
    0% {
        transform: translateX(0) rotateY(0deg);
        opacity: 1;
    }
    100% {
        transform: translateX(100px) rotateY(90deg);
        opacity: 0;
    }
}
`;

// Inject ripple CSS
const style = document.createElement('style');
style.textContent = rippleCSS;
document.head.appendChild(style);

// Utility functions
window.BijouxStore = {
    formatPrice: function(price) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR'
        }).format(price);
    },
    
    showAlert: function(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
            
            // Auto-hide after 5 seconds
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }, 5000);
        }
    }
};
