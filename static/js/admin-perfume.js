/**
 * JavaScript pour l'administration des parfums
 * Gestion des images multiples et aperçu
 */

// Gestion de l'upload d'images multiples
document.addEventListener('DOMContentLoaded', function() {
    initImageUploads();
    initFormValidation();
    console.log('🌸 Admin Parfum JavaScript initialisé');
});

function initImageUploads() {
    const imageInputs = document.querySelectorAll('.image-input');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const previewId = this.dataset.preview;
            const previewContainer = document.getElementById(previewId);
            const uploadItem = this.closest('.image-upload-item');
            
            if (file) {
                // Vérifier le type de fichier
                if (!file.type.startsWith('image/')) {
                    showNotification('Veuillez sélectionner un fichier image valide.', 'error');
                    return;
                }
                
                // Vérifier la taille (5MB max)
                if (file.size > 5 * 1024 * 1024) {
                    showNotification('L\'image ne doit pas dépasser 5MB.', 'error');
                    return;
                }
                
                // Créer l'aperçu
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewContainer.innerHTML = `
                        <img src="${e.target.result}" alt="Aperçu">
                        <button type="button" class="btn btn-sm btn-danger remove-image" onclick="removeImage('${previewId}', this)">
                            <i class="fas fa-times"></i>
                        </button>
                    `;
                    uploadItem.classList.add('has-image');
                    showNotification('Image ajoutée avec succès!', 'success');
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

function removeImage(previewId, button) {
    const previewContainer = document.getElementById(previewId);
    const uploadItem = button.closest('.image-upload-item');
    const input = uploadItem.querySelector('.image-input');
    
    // Réinitialiser l'input
    input.value = '';
    
    // Réinitialiser l'aperçu
    const isMain = previewId === 'preview-main';
    previewContainer.innerHTML = `
        <i class="fas fa-image ${isMain ? 'fa-3x' : 'fa-2x'} text-muted"></i>
        <p class="text-muted">${isMain ? 'Cliquez pour ajouter' : 'Optionnel'}</p>
    `;
    
    uploadItem.classList.remove('has-image');
    showNotification('Image supprimée.', 'info');
}

function initFormValidation() {
    const form = document.getElementById('perfumeForm');
    const inputs = form.querySelectorAll('.perfume-input[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearValidation);
    });
    
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            showNotification('Veuillez corriger les erreurs dans le formulaire.', 'error');
        }
    });
}

function validateField(e) {
    const field = e.target;
    const value = field.value.trim();
    
    // Validation de base
    if (field.hasAttribute('required') && !value) {
        setFieldError(field, 'Ce champ est obligatoire.');
        return false;
    }
    
    // Validations spécifiques
    switch (field.id) {
        case 'name':
            if (value.length < 3) {
                setFieldError(field, 'Le nom doit contenir au moins 3 caractères.');
                return false;
            }
            break;
            
        case 'price':
            const price = parseFloat(value);
            if (isNaN(price) || price <= 0) {
                setFieldError(field, 'Le prix doit être un nombre positif.');
                return false;
            }
            if (price > 1000) {
                setFieldError(field, 'Le prix semble très élevé. Vérifiez la valeur.');
                return false;
            }
            break;
            
        case 'stock_quantity':
            const stock = parseInt(value);
            if (isNaN(stock) || stock < 0) {
                setFieldError(field, 'La quantité doit être un nombre positif ou zéro.');
                return false;
            }
            break;
            
        case 'description':
            if (value.length < 10) {
                setFieldError(field, 'La description doit contenir au moins 10 caractères.');
                return false;
            }
            break;
    }
    
    setFieldSuccess(field);
    return true;
}

function setFieldError(field, message) {
    field.classList.remove('is-valid');
    field.classList.add('is-invalid');
    
    // Supprimer l'ancien message d'erreur
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
    
    // Ajouter le nouveau message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function setFieldSuccess(field) {
    field.classList.remove('is-invalid');
    field.classList.add('is-valid');
    
    // Supprimer le message d'erreur
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

function clearValidation(e) {
    const field = e.target;
    field.classList.remove('is-valid', 'is-invalid');
    
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

function validateForm() {
    const form = document.getElementById('perfumeForm');
    const requiredFields = form.querySelectorAll('.perfume-input[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!validateField({ target: field })) {
            isValid = false;
        }
    });
    
    return isValid;
}

function previewPerfume() {
    const form = document.getElementById('perfumeForm');
    const formData = new FormData(form);
    
    // Collecter les données
    const perfumeData = {
        name: formData.get('name') || 'Nom du parfum',
        category: formData.get('category') || 'Non spécifié',
        material: formData.get('material') || 'Non spécifié',
        price: formData.get('price') || '0',
        stock_quantity: formData.get('stock_quantity') || '0',
        description: formData.get('description') || 'Aucune description',
        fragrance_family: formData.get('fragrance_family') || 'Non spécifiée',
        top_notes: formData.get('top_notes') || 'Non spécifiées',
        heart_notes: formData.get('heart_notes') || 'Non spécifiées',
        base_notes: formData.get('base_notes') || 'Non spécifiées',
        gender: formData.get('gender') || 'Non spécifié',
        volume: formData.get('volume') || 'Non spécifié',
        concentration: formData.get('concentration') || 'Non spécifiée'
    };
    
    // Générer l'aperçu
    const previewHTML = generatePreviewHTML(perfumeData);
    
    // Afficher dans le modal
    document.getElementById('previewContent').innerHTML = previewHTML;
    
    // Ouvrir le modal
    const modal = new bootstrap.Modal(document.getElementById('previewModal'));
    modal.show();
}

function generatePreviewHTML(data) {
    return `
        <div class="preview-card">
            <div class="row">
                <div class="col-md-4">
                    <div class="preview-image-gallery">
                        <div class="preview-image-placeholder">
                            <i class="fas fa-spray-can fa-4x text-primary"></i>
                        </div>
                    </div>
                    <p class="text-muted text-center">
                        <small>Les images uploadées apparaîtront ici</small>
                    </p>
                </div>
                <div class="col-md-8">
                    <h4 class="text-primary">${data.name}</h4>
                    <div class="mb-3">
                        <span class="badge bg-primary me-1">${data.category}</span>
                        <span class="badge bg-secondary me-1">${data.material.split(' - ')[1] || 'Genre'}</span>
                        <span class="badge bg-info">${data.volume}ml</span>
                    </div>
                    <p class="mb-3">${data.description}</p>
                    
                    <div class="row mb-3">
                        <div class="col-6">
                            <strong>Prix:</strong> ${data.price}€
                        </div>
                        <div class="col-6">
                            <strong>Stock:</strong> ${data.stock_quantity} unités
                        </div>
                    </div>
                    
                    ${data.fragrance_family !== 'Non spécifiée' ? `
                    <div class="mb-3">
                        <strong>Famille olfactive:</strong> ${data.fragrance_family}
                    </div>
                    ` : ''}
                    
                    ${(data.top_notes !== 'Non spécifiées' || data.heart_notes !== 'Non spécifiées' || data.base_notes !== 'Non spécifiées') ? `
                    <div class="notes-preview">
                        <h6><i class="fas fa-leaf me-2"></i>Notes Olfactives</h6>
                        ${data.top_notes !== 'Non spécifiées' ? `
                        <div class="note-item">
                            <i class="fas fa-arrow-up me-2"></i>
                            <strong>Tête:</strong> ${data.top_notes}
                        </div>
                        ` : ''}
                        ${data.heart_notes !== 'Non spécifiées' ? `
                        <div class="note-item">
                            <i class="fas fa-heart me-2"></i>
                            <strong>Cœur:</strong> ${data.heart_notes}
                        </div>
                        ` : ''}
                        ${data.base_notes !== 'Non spécifiées' ? `
                        <div class="note-item">
                            <i class="fas fa-arrow-down me-2"></i>
                            <strong>Fond:</strong> ${data.base_notes}
                        </div>
                        ` : ''}
                    </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove après 5 secondes
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Export des fonctions pour utilisation globale
window.AdminPerfume = {
    previewPerfume,
    removeImage,
    showNotification
};
