from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Créer l'instance db ici
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    orders = db.relationship('Order', backref='user', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Eau de Parfum, Eau de Toilette, Eau de Cologne, Parfum
    material = db.Column(db.String(50))  # Marque - Genre - Volume (ex: "Chanel - Femme - 50ml")
    stock_quantity = db.Column(db.Integer, default=0)
    min_stock_alert = db.Column(db.Integer, default=5)
    image_filename = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    images = db.relationship('ProductImage', backref='product', lazy=True, cascade='all, delete-orphan')
    
    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.min_stock_alert
    
    @property
    def image_url(self):
        """URL de l'image principale (pour compatibilité)"""
        primary_image = self.get_primary_image()
        if primary_image:
            return primary_image.image_url
        elif self.image_filename:
            return f'/static/uploads/{self.image_filename}'
        return '/static/images/no-image.jpg'

    def get_primary_image(self):
        """Récupère l'image principale du produit"""
        return ProductImage.query.filter_by(product_id=self.id, is_primary=True).first()

    def get_all_images(self):
        """Récupère toutes les images du produit triées par ordre d'affichage"""
        return ProductImage.query.filter_by(product_id=self.id).order_by(ProductImage.display_order, ProductImage.id).all()

    def get_gallery_images(self):
        """Récupère les images de la galerie (non principales)"""
        return ProductImage.query.filter_by(product_id=self.id, is_primary=False).order_by(ProductImage.display_order, ProductImage.id).all()

    @property
    def has_multiple_images(self):
        """Vérifie si le produit a plusieurs images"""
        return len(self.images) > 1

class ProductImage(db.Model):
    """Modèle pour les images multiples des produits parfums"""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    alt_text = db.Column(db.String(200))  # Texte alternatif pour l'accessibilité
    is_primary = db.Column(db.Boolean, default=False)  # Image principale
    display_order = db.Column(db.Integer, default=0)  # Ordre d'affichage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def image_url(self):
        """URL de l'image"""
        if self.filename:
            return f'/static/uploads/{self.filename}'
        return '/static/images/no-image.jpg'

    def __repr__(self):
        return f'<ProductImage {self.filename}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, shipped, delivered, cancelled
    shipping_address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Prix au moment de la commande

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Slider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300))
    description = db.Column(db.Text)
    image_filename = db.Column(db.String(100), nullable=False)
    button_text = db.Column(db.String(50))
    button_link = db.Column(db.String(200))
    order_position = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def image_url(self):
        if self.image_filename:
            return f'/static/uploads/sliders/{self.image_filename}'
        return '/static/images/slider-default.jpg'

class FooterSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False, default='Parfum Store')
    company_description = db.Column(db.Text)
    address = db.Column(db.Text)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    facebook_url = db.Column(db.String(200))
    instagram_url = db.Column(db.String(200))
    twitter_url = db.Column(db.String(200))
    linkedin_url = db.Column(db.String(200))
    youtube_url = db.Column(db.String(200))
    opening_hours = db.Column(db.Text)
    copyright_text = db.Column(db.String(200))
    show_newsletter = db.Column(db.Boolean, default=True)
    newsletter_title = db.Column(db.String(200), default='Newsletter')
    newsletter_description = db.Column(db.Text, default='Restez informé de nos dernières nouveautés')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def get_settings():
        """Récupère les paramètres du footer (crée des valeurs par défaut si aucune n'existe)"""
        settings = FooterSettings.query.first()
        if not settings:
            settings = FooterSettings(
                company_name='Parfum Store',
                company_description='Votre boutique de parfums de luxe depuis 1995. Nous proposons une sélection exclusive de parfums authentiques des plus grandes marques.',
                address='123 Avenue des Champs-Élysées\n75008 Paris, France',
                phone='+33 1 23 45 67 89',
                email='contact@parfum-store.com',
                opening_hours='Lundi - Vendredi: 9h00 - 19h00\nSamedi: 10h00 - 18h00\nDimanche: Fermé',
                copyright_text='© 2024 Parfum Store. Tous droits réservés.'
            )
            db.session.add(settings)
            db.session.commit()
        return settings
