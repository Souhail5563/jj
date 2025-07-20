from app import app, db
from models import User, Product, Slider, FooterSettings
from werkzeug.security import generate_password_hash

def init_sample_data():
    with app.app_context():
        # Créer les tables
        db.create_all()
        
        # Créer un admin par défaut
        admin = User.query.filter_by(email='admin@bijoux.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@bijoux.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='Bijoux Store',
                is_admin=True
            )
            db.session.add(admin)
        
        # Créer un utilisateur de test
        user = User.query.filter_by(email='client@test.com').first()
        if not user:
            user = User(
                username='client',
                email='client@test.com',
                password_hash=generate_password_hash('client123'),
                first_name='Jean',
                last_name='Dupont'
            )
            db.session.add(user)
        
        # Créer des produits de démonstration
        products_data = [
            {
                'name': 'Bague Solitaire Diamant',
                'description': 'Magnifique bague solitaire en or blanc 18 carats avec diamant de 1 carat.',
                'price': 2500.00,
                'category': 'Bagues',
                'material': 'Or',
                'stock_quantity': 5
            },
            {
                'name': 'Collier Perles Akoya',
                'description': 'Collier élégant en perles Akoya naturelles avec fermoir en or.',
                'price': 850.00,
                'category': 'Colliers',
                'material': 'Or',
                'stock_quantity': 8
            },
            {
                'name': 'Bracelet Tennis Diamants',
                'description': 'Bracelet tennis serti de diamants brillants en or blanc.',
                'price': 1200.00,
                'category': 'Bracelets',
                'material': 'Or',
                'stock_quantity': 3
            },
            {
                'name': 'Boucles d\'oreilles Émeraude',
                'description': 'Boucles d\'oreilles pendantes avec émeraudes et diamants.',
                'price': 950.00,
                'category': 'Boucles d\'oreilles',
                'material': 'Or',
                'stock_quantity': 6
            },
            {
                'name': 'Alliance Or Rose',
                'description': 'Alliance classique en or rose 18 carats, finition polie.',
                'price': 450.00,
                'category': 'Bagues',
                'material': 'Or rose',
                'stock_quantity': 12
            },
            {
                'name': 'Pendentif Coeur Argent',
                'description': 'Pendentif en forme de coeur en argent sterling avec chaîne.',
                'price': 120.00,
                'category': 'Colliers',
                'material': 'Argent',
                'stock_quantity': 15
            },
            {
                'name': 'Montre Bracelet Femme',
                'description': 'Montre élégante avec bracelet en acier inoxydable et cadran nacré.',
                'price': 320.00,
                'category': 'Bracelets',
                'material': 'Acier inoxydable',
                'stock_quantity': 7
            },
            {
                'name': 'Créoles Diamants',
                'description': 'Créoles modernes serties de petits diamants brillants.',
                'price': 680.00,
                'category': 'Boucles d\'oreilles',
                'material': 'Or',
                'stock_quantity': 4
            }
        ]
        
        for product_data in products_data:
            existing_product = Product.query.filter_by(name=product_data['name']).first()
            if not existing_product:
                product = Product(**product_data)
                db.session.add(product)

        # Créer des sliders de démonstration
        sliders_data = [
            {
                'title': 'Collection Exclusive 2024',
                'subtitle': 'Découvrez nos nouveautés',
                'description': 'Des bijoux d\'exception créés par nos maîtres artisans pour sublimer votre élégance.',
                'button_text': 'Découvrir',
                'button_link': '/catalog',
                'order_position': 0,
                'image_filename': 'slider1.jpg'  # Image par défaut
            },
            {
                'title': 'Bagues de Fiançailles',
                'subtitle': 'L\'amour éternel',
                'description': 'Trouvez la bague parfaite pour votre demande en mariage. Diamants certifiés et or 18 carats.',
                'button_text': 'Voir les Bagues',
                'button_link': '/catalog?category=Bagues',
                'order_position': 1,
                'image_filename': 'slider2.jpg'
            },
            {
                'title': 'Offre Spéciale',
                'subtitle': '-20% sur tous les colliers',
                'description': 'Profitez de notre promotion exceptionnelle sur toute la collection de colliers.',
                'button_text': 'Profiter de l\'offre',
                'button_link': '/catalog?category=Colliers',
                'order_position': 2,
                'image_filename': 'slider3.jpg'
            }
        ]

        for slider_data in sliders_data:
            existing_slider = Slider.query.filter_by(title=slider_data['title']).first()
            if not existing_slider:
                slider = Slider(**slider_data)
                db.session.add(slider)

        # Créer les paramètres du footer par défaut
        footer_settings = FooterSettings.query.first()
        if not footer_settings:
            footer_settings = FooterSettings(
                company_name='Bijoux Store',
                company_description='Votre boutique de bijoux de luxe depuis 1995. Nous proposons une sélection exclusive de bijoux artisanaux de haute qualité.',
                address='123 Rue de la Paix\n75001 Paris, France',
                phone='+33 1 23 45 67 89',
                email='contact@bijoux-store.com',
                facebook_url='https://facebook.com/bijouxstore',
                instagram_url='https://instagram.com/bijouxstore',
                twitter_url='https://twitter.com/bijouxstore',
                opening_hours='Lundi - Vendredi: 9h00 - 19h00\nSamedi: 10h00 - 18h00\nDimanche: Fermé',
                copyright_text='© 2024 Bijoux Store. Tous droits réservés.',
                show_newsletter=True,
                newsletter_title='Newsletter',
                newsletter_description='Restez informé de nos dernières nouveautés et offres exclusives'
            )
            db.session.add(footer_settings)

        db.session.commit()
        print("Données de démonstration créées avec succès!")
        print("Admin: admin@bijoux.com / admin123")
        print("Client: client@test.com / client123")
        print("3 sliders de démonstration ajoutés")
        print("Paramètres du footer initialisés")

if __name__ == '__main__':
    init_sample_data()
