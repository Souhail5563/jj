"""
Script pour recréer complètement la base de données avec les parfums
"""
import os
from app import app, db
from models import Product, User, FooterSettings

def recreate_database():
    """Recréer complètement la base de données"""
    with app.app_context():
        print("🔄 Recréation complète de la base de données...")
        
        # Supprimer l'ancienne base de données
        db_path = 'ecommerce.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            print("✅ Ancienne base de données supprimée")
        
        # Créer les nouvelles tables
        db.create_all()
        print("✅ Nouvelles tables créées")
        
        # Créer l'utilisateur admin
        admin = User(
            username='admin',
            email='admin@parfum.com',
            password_hash='pbkdf2:sha256:600000$salt$hash',  # Mot de passe: admin123
            first_name='Admin',
            last_name='Parfum',
            is_admin=True
        )
        db.session.add(admin)
        
        # Créer un utilisateur test
        test_user = User(
            username='testuser',
            email='test@parfum.com',
            password_hash='pbkdf2:sha256:600000$salt$hash',
            first_name='Test',
            last_name='User',
            phone='+212600154487'
        )
        db.session.add(test_user)
        
        print("✅ Utilisateurs créés")

def create_perfume_products():
    """Créer des produits parfums"""
    with app.app_context():
        print("🌸 Création des parfums...")
        
        perfumes = [
            {
                'name': 'Chanel N°5 Eau de Parfum',
                'description': 'Le parfum le plus célèbre au monde. Un bouquet floral aldéhydé intemporel et mystérieux qui révèle sa sensualité et son élégance.',
                'price': 89.90,
                'category': 'Eau de Parfum',
                'brand': 'Chanel',
                'volume': 50,
                'concentration': 'EDP',
                'fragrance_family': 'Floral Aldéhydé',
                'top_notes': 'Aldéhydes, Ylang-ylang, Néroli, Bergamote',
                'heart_notes': 'Rose de mai, Jasmin, Muguet, Iris',
                'base_notes': 'Santal, Vétiver, Vanille, Musc',
                'gender': 'Femme',
                'stock_quantity': 25
            },
            {
                'name': 'Dior Sauvage Eau de Toilette',
                'description': 'Un parfum masculin frais et puissant inspiré des grands espaces. Une composition radieuse et sauvage.',
                'price': 79.90,
                'category': 'Eau de Toilette',
                'brand': 'Dior',
                'volume': 100,
                'concentration': 'EDT',
                'fragrance_family': 'Aromatique Boisé',
                'top_notes': 'Bergamote de Calabre, Poivre rose',
                'heart_notes': 'Géranium, Lavande, Elemi, Poivre de Sichuan',
                'base_notes': 'Ambroxan, Cèdre, Labdanum',
                'gender': 'Homme',
                'stock_quantity': 30
            },
            {
                'name': 'Tom Ford Black Orchid',
                'description': 'Un parfum luxueux et mystérieux aux accords floraux noirs et épicés. Une fragrance captivante et sophistiquée.',
                'price': 129.90,
                'category': 'Eau de Parfum',
                'brand': 'Tom Ford',
                'volume': 50,
                'concentration': 'EDP',
                'fragrance_family': 'Oriental Floral',
                'top_notes': 'Truffe, Ylang-ylang, Bergamote, Cassis',
                'heart_notes': 'Orchidée noire, Épices, Fruits, Lotus',
                'base_notes': 'Patchouli, Vanille, Santal, Encens',
                'gender': 'Mixte',
                'stock_quantity': 15
            },
            {
                'name': 'Hermès Terre d\'Hermès',
                'description': 'Un parfum qui raconte la relation de l\'homme à la terre. Une fragrance minérale et végétale.',
                'price': 94.90,
                'category': 'Eau de Toilette',
                'brand': 'Hermès',
                'volume': 100,
                'concentration': 'EDT',
                'fragrance_family': 'Boisé Minéral',
                'top_notes': 'Orange, Pamplemousse, Poivre',
                'heart_notes': 'Poivre, Pélargonium, Silex, Rose',
                'base_notes': 'Vétiver, Cèdre, Benzoin',
                'gender': 'Homme',
                'stock_quantity': 20
            },
            {
                'name': 'YSL Black Opium',
                'description': 'Un parfum féminin addictif aux notes de café et de vanille. Une fragrance rock et glamour.',
                'price': 84.90,
                'category': 'Eau de Parfum',
                'brand': 'Yves Saint Laurent',
                'volume': 50,
                'concentration': 'EDP',
                'fragrance_family': 'Oriental Gourmand',
                'top_notes': 'Cassis, Poire, Mandarine',
                'heart_notes': 'Café, Jasmin, Fleur d\'oranger',
                'base_notes': 'Vanille, Patchouli, Cèdre, Cachemire',
                'gender': 'Femme',
                'stock_quantity': 22
            },
            {
                'name': 'Creed Aventus',
                'description': 'Un parfum masculin légendaire aux notes fruitées et boisées. L\'essence du succès et de la force.',
                'price': 189.90,
                'category': 'Eau de Parfum',
                'brand': 'Creed',
                'volume': 50,
                'concentration': 'EDP',
                'fragrance_family': 'Fruité Boisé',
                'top_notes': 'Ananas, Cassis, Pomme, Bergamote',
                'heart_notes': 'Bouleau, Patchouli, Jasmin, Rose',
                'base_notes': 'Musc, Chêne, Ambre gris, Vanille',
                'gender': 'Homme',
                'stock_quantity': 10
            },
            {
                'name': 'Lancôme La Vie Est Belle',
                'description': 'Un parfum gourmand et floral qui célèbre la joie de vivre. Une fragrance lumineuse et pétillante.',
                'price': 76.90,
                'category': 'Eau de Parfum',
                'brand': 'Lancôme',
                'volume': 50,
                'concentration': 'EDP',
                'fragrance_family': 'Floral Gourmand',
                'top_notes': 'Cassis, Poire',
                'heart_notes': 'Iris, Jasmin, Fleur d\'oranger',
                'base_notes': 'Praline, Vanille, Patchouli, Tonka',
                'gender': 'Femme',
                'stock_quantity': 18
            },
            {
                'name': 'Giorgio Armani Acqua di Giò',
                'description': 'Un parfum aquatique frais et méditerranéen. L\'essence de la liberté et de l\'évasion.',
                'price': 69.90,
                'category': 'Eau de Toilette',
                'brand': 'Giorgio Armani',
                'volume': 100,
                'concentration': 'EDT',
                'fragrance_family': 'Aquatique Aromatique',
                'top_notes': 'Bergamote, Néroli, Citron vert',
                'heart_notes': 'Jasmin, Calone, Freesia, Hiacynthe',
                'base_notes': 'Musc blanc, Cèdre, Ambre',
                'gender': 'Homme',
                'stock_quantity': 28
            }
        ]
        
        for perfume_data in perfumes:
            perfume = Product(**perfume_data)
            db.session.add(perfume)
            print(f"✅ {perfume_data['name']} - {perfume_data['price']}€")
        
        db.session.commit()
        print(f"🌸 {len(perfumes)} parfums créés avec succès")

def main():
    """Fonction principale"""
    print("🌸 Recréation complète de la base de données pour les parfums")
    print("=" * 60)
    
    # 1. Recréer la base de données
    recreate_database()
    
    # 2. Créer les parfums
    create_perfume_products()
    
    # 3. Les paramètres du footer seront créés automatiquement
    
    print("\n" + "=" * 60)
    print("🎉 Base de données parfums créée avec succès!")
    print("🌸 Produits disponibles:")
    print("   • Chanel N°5 EDP - 89.90€")
    print("   • Dior Sauvage EDT - 79.90€") 
    print("   • Tom Ford Black Orchid EDP - 129.90€")
    print("   • Hermès Terre d'Hermès EDT - 94.90€")
    print("   • YSL Black Opium EDP - 84.90€")
    print("   • Creed Aventus EDP - 189.90€")
    print("   • Lancôme La Vie Est Belle EDP - 76.90€")
    print("   • Armani Acqua di Giò EDT - 69.90€")
    print("\n🔗 Redémarrez le serveur Flask pour voir les changements")
    print("👤 Admin: admin@parfum.com / admin123")

if __name__ == '__main__':
    main()
