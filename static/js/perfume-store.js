/**
 * JavaScript pour Parfum Store
 * Fonctionnalités interactives pour l'interface parfums
 */

// Fonctions pour les boutons de quantité
function decreaseQuantity() {
    const quantityInput = document.getElementById('quantity');
    const currentValue = parseInt(quantityInput.value);
    const minValue = parseInt(quantityInput.min);
    
    if (currentValue > minValue) {
        quantityInput.value = currentValue - 1;
    }
}

function increaseQuantity(maxQuantity) {
    const quantityInput = document.getElementById('quantity');
    const currentValue = parseInt(quantityInput.value);
    
    if (currentValue < maxQuantity) {
        quantityInput.value = currentValue + 1;
    }
}

// Animation des cartes parfums au scroll
function animateOnScroll() {
    const cards = document.querySelectorAll('.perfume-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
}

// Effet de particules parfum
function createPerfumeParticles() {
    const hero = document.querySelector('.perfume-hero');
    if (!hero) return;

    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'perfume-particle';
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255, 215, 0, 0.6);
            border-radius: 50%;
            pointer-events: none;
            animation: floatParticle ${5 + Math.random() * 5}s infinite linear;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation-delay: ${Math.random() * 5}s;
        `;
        hero.appendChild(particle);
    }
}

// Animation des particules
const style = document.createElement('style');
style.textContent = `
    @keyframes floatParticle {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Effet hover sur les boutons parfum
function enhancePerfumeButtons() {
    const buttons = document.querySelectorAll('.perfume-btn, .perfume-btn-outline');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Effet de brillance sur les cartes parfum
function addShimmerEffect() {
    const cards = document.querySelectorAll('.perfume-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const shimmer = document.createElement('div');
            shimmer.className = 'shimmer-effect';
            shimmer.style.cssText = `
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
                animation: shimmer 0.8s ease-out;
                pointer-events: none;
                z-index: 10;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(shimmer);
            
            setTimeout(() => {
                if (shimmer.parentNode) {
                    shimmer.parentNode.removeChild(shimmer);
                }
            }, 800);
        });
    });
}

// Animation shimmer
const shimmerStyle = document.createElement('style');
shimmerStyle.textContent = `
    @keyframes shimmer {
        0% {
            left: -100%;
        }
        100% {
            left: 100%;
        }
    }
`;
document.head.appendChild(shimmerStyle);

// Fonction pour afficher les notifications parfum
function showPerfumeNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `perfume-notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-spray-can me-2"></i>
        <span>${message}</span>
        <button class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #28a745, #20c997)' : 'linear-gradient(135deg, #dc3545, #e83e8c)'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        animation: slideInNotification 0.5s ease-out;
        max-width: 350px;
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove après 5 secondes
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOutNotification 0.5s ease-out';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 500);
        }
    }, 5000);
}

// Animations pour les notifications
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    @keyframes slideInNotification {
        0% {
            transform: translateX(100%);
            opacity: 0;
        }
        100% {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutNotification {
        0% {
            transform: translateX(0);
            opacity: 1;
        }
        100% {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .btn-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
    }
`;
document.head.appendChild(notificationStyle);

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Activer les animations
    animateOnScroll();
    enhancePerfumeButtons();
    addShimmerEffect();
    createPerfumeParticles();

    // Initialiser la galerie d'images
    initPerfumeGallery();

    // Ajouter des effets aux formulaires
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && submitBtn.classList.contains('perfume-btn')) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Traitement...';
                submitBtn.disabled = true;
            }
        });
    });

    // Effet sur les badges de marque
    const brandTags = document.querySelectorAll('.brand-tag');
    brandTags.forEach(tag => {
        tag.addEventListener('click', function() {
            const brand = this.textContent;
            showPerfumeNotification(`Filtrage par marque: ${brand}`, 'success');
        });
    });

    console.log('🌸 Parfum Store JavaScript initialisé avec galerie d\'images');
});

// Fonction utilitaire pour formater les prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
}

// ===== GALERIE D'IMAGES PARFUMS =====

// Changer l'image principale
function changeMainImage(imageUrl, altText, thumbnailElement) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        // Animation de transition
        mainImage.style.opacity = '0.5';

        setTimeout(() => {
            mainImage.src = imageUrl;
            mainImage.alt = altText;
            mainImage.style.opacity = '1';
        }, 150);

        // Mettre à jour les miniatures actives
        document.querySelectorAll('.thumbnail-item').forEach(thumb => {
            thumb.classList.remove('active');
        });
        thumbnailElement.classList.add('active');

        // Notification
        showPerfumeNotification('Image changée', 'success');
    }
}

// Modal de zoom d'image
function openImageModal(imageSrc, altText) {
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <span class="image-modal-close">&times;</span>
        <img class="image-modal-content" src="${imageSrc}" alt="${altText}">
    `;

    document.body.appendChild(modal);
    modal.style.display = 'block';

    // Fermer le modal
    modal.addEventListener('click', function(e) {
        if (e.target === modal || e.target.classList.contains('image-modal-close')) {
            document.body.removeChild(modal);
        }
    });

    // Fermer avec Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.parentNode) {
            document.body.removeChild(modal);
        }
    });
}

// Navigation galerie avec clavier
function setupGalleryKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        const thumbnails = document.querySelectorAll('.thumbnail-item');
        const activeThumbnail = document.querySelector('.thumbnail-item.active');

        if (!activeThumbnail || thumbnails.length <= 1) return;

        let currentIndex = Array.from(thumbnails).indexOf(activeThumbnail);
        let newIndex = currentIndex;

        if (e.key === 'ArrowLeft') {
            newIndex = currentIndex > 0 ? currentIndex - 1 : thumbnails.length - 1;
            e.preventDefault();
        } else if (e.key === 'ArrowRight') {
            newIndex = currentIndex < thumbnails.length - 1 ? currentIndex + 1 : 0;
            e.preventDefault();
        }

        if (newIndex !== currentIndex) {
            thumbnails[newIndex].click();
        }
    });
}

// Préchargement des images
function preloadGalleryImages() {
    const thumbnails = document.querySelectorAll('.thumbnail-item img');
    thumbnails.forEach(thumb => {
        const img = new Image();
        img.src = thumb.src;
    });
}

// Effet de survol sur les miniatures
function enhanceThumbnailHover() {
    const thumbnails = document.querySelectorAll('.thumbnail-item');

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('mouseenter', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'scale(1.1)';
                this.style.boxShadow = '0 5px 15px rgba(255, 215, 0, 0.3)';
            }
        });

        thumbnail.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'scale(1)';
                this.style.boxShadow = 'none';
            }
        });
    });
}

// Lazy loading pour les images
function setupLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Swipe pour mobile
function setupMobileSwipe() {
    const mainImage = document.getElementById('mainImage');
    if (!mainImage) return;

    let startX = 0;
    let startY = 0;

    mainImage.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
    });

    mainImage.addEventListener('touchend', function(e) {
        const endX = e.changedTouches[0].clientX;
        const endY = e.changedTouches[0].clientY;

        const diffX = startX - endX;
        const diffY = startY - endY;

        // Swipe horizontal
        if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
            const thumbnails = document.querySelectorAll('.thumbnail-item');
            const activeThumbnail = document.querySelector('.thumbnail-item.active');

            if (activeThumbnail && thumbnails.length > 1) {
                const currentIndex = Array.from(thumbnails).indexOf(activeThumbnail);
                let newIndex;

                if (diffX > 0) { // Swipe left - image suivante
                    newIndex = currentIndex < thumbnails.length - 1 ? currentIndex + 1 : 0;
                } else { // Swipe right - image précédente
                    newIndex = currentIndex > 0 ? currentIndex - 1 : thumbnails.length - 1;
                }

                thumbnails[newIndex].click();
            }
        }
    });
}

// Initialisation de la galerie
function initPerfumeGallery() {
    // Ajouter le zoom sur l'image principale
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        mainImage.addEventListener('click', function() {
            openImageModal(this.src, this.alt);
        });
    }

    // Configuration des fonctionnalités
    setupGalleryKeyboardNavigation();
    preloadGalleryImages();
    enhanceThumbnailHover();
    setupLazyLoading();
    setupMobileSwipe();

    console.log('🖼️ Galerie parfums initialisée');
}

// Export des fonctions pour utilisation globale
window.PerfumeStore = {
    decreaseQuantity,
    increaseQuantity,
    showPerfumeNotification,
    formatPrice,
    changeMainImage,
    openImageModal,
    initPerfumeGallery
};
