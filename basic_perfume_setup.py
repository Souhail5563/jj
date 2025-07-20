"""
Script basique pour créer des parfums avec les champs de base seulement
"""
import os
from app import app, db
from models import Product, User, FooterSettings

def setup_basic_perfumes():
    """Créer des parfums avec les champs de base seulement"""
    with app.app_context():
        print("🌸 Configuration basique pour les parfums...")
        
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
        
        # Créer un utilisateur test avec WhatsApp
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
        
        # Créer des parfums avec les champs de base seulement
        perfumes = [
            {
                'name': 'Chanel N°5 EDP 50ml',
                'description': 'Le parfum le plus célèbre au monde. Un bouquet floral aldéhydé intemporel et mystérieux. Notes: Aldéhydes, Rose, Jasmin, Santal, Vanille. Concentration: Eau de Parfum.',
                'price': 89.90,
                'category': 'Eau de Parfum',
                'material': 'Chanel - Femme - 50ml',
                'stock_quantity': 25
            },
            {
                'name': 'Dior Sauvage EDT 100ml',
                'description': 'Un parfum masculin frais et puissant inspiré des grands espaces. Notes: Bergamote, Poivre rose, Géranium, Ambroxan, Cèdre. Concentration: Eau de Toilette.',
                'price': 79.90,
                'category': 'Eau de Toilette',
                'material': 'Dior - Homme - 100ml',
                'stock_quantity': 30
            },
            {
                'name': 'Tom Ford Black Orchid EDP 50ml',
                'description': 'Un parfum luxueux et mystérieux aux accords floraux noirs et épicés. Notes: Truffe, Orchidée noire, Patchouli, Vanille. Concentration: Eau de Parfum.',
                'price': 129.90,
                'category': 'Eau de Parfum',
                'material': 'Tom Ford - Mixte - 50ml',
                'stock_quantity': 15
            },
            {
                'name': 'Hermès Terre d\'Hermès EDT 100ml',
                'description': 'Un parfum qui raconte la relation de l\'homme à la terre. Notes: Orange, Pamplemousse, Poivre, Vétiver, Cèdre. Concentration: Eau de Toilette.',
                'price': 94.90,
                'category': 'Eau de Toilette',
                'material': 'Hermès - Homme - 100ml',
                'stock_quantity': 20
            },
            {
                'name': 'YSL Black Opium EDP 50ml',
                'description': 'Un parfum féminin addictif aux notes de café et de vanille. Notes: Cassis, Café, Jasmin, Vanille, Patchouli. Concentration: Eau de Parfum.',
                'price': 84.90,
                'category': 'Eau de Parfum',
                'material': 'YSL - Femme - 50ml',
                'stock_quantity': 22
            },
            {
                'name': 'Creed Aventus EDP 50ml',
                'description': 'Un parfum masculin légendaire aux notes fruitées et boisées. Notes: Ananas, Cassis, Bouleau, Musc, Chêne, Vanille. Concentration: Eau de Parfum.',
                'price': 189.90,
                'category': 'Eau de Parfum',
                'material': 'Creed - Homme - 50ml',
                'stock_quantity': 10
            },
            {
                'name': 'Lancôme La Vie Est Belle EDP 50ml',
                'description': 'Un parfum gourmand et floral qui célèbre la joie de vivre. Notes: Cassis, Iris, Jasmin, Praline, Vanille. Concentration: Eau de Parfum.',
                'price': 76.90,
                'category': 'Eau de Parfum',
                'material': 'Lancôme - Femme - 50ml',
                'stock_quantity': 18
            },
            {
                'name': 'Armani Acqua di Giò EDT 100ml',
                'description': 'Un parfum aquatique frais et méditerranéen. Notes: Bergamote, Néroli, Jasmin, Musc blanc, Cèdre. Concentration: Eau de Toilette.',
                'price': 69.90,
                'category': 'Eau de Toilette',
                'material': 'Armani - Homme - 100ml',
                'stock_quantity': 28
            },
            {
                'name': 'Versace Eros EDT 100ml',
                'description': 'Un parfum masculin passionné et audacieux. Notes: Menthe, Pomme verte, Tonka, Vanille, Cèdre. Concentration: Eau de Toilette.',
                'price': 59.90,
                'category': 'Eau de Toilette',
                'material': 'Versace - Homme - 100ml',
                'stock_quantity': 35
            },
            {
                'name': 'Paco Rabanne 1 Million EDT 100ml',
                'description': 'Un parfum masculin doré et séducteur. Notes: Pamplemousse, Menthe, Cannelle, Cuir, Ambre. Concentration: Eau de Toilette.',
                'price': 64.90,
                'category': 'Eau de Toilette',
                'material': 'Paco Rabanne - Homme - 100ml',
                'stock_quantity': 32
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
    print("🌸 Configuration basique du site de parfums")
    print("=" * 50)
    
    setup_basic_perfumes()
    
    print("\n" + "=" * 50)
    print("🎉 Site de parfums configuré avec succès!")
    print("🌸 Parfums disponibles:")
    print("   • Chanel N°5 EDP 50ml - 89.90€")
    print("   • Dior Sauvage EDT 100ml - 79.90€") 
    print("   • Tom Ford Black Orchid EDP 50ml - 129.90€")
    print("   • Hermès Terre d'Hermès EDT 100ml - 94.90€")
    print("   • YSL Black Opium EDP 50ml - 84.90€")
    print("   • Creed Aventus EDP 50ml - 189.90€")
    print("   • Lancôme La Vie Est Belle EDP 50ml - 76.90€")
    print("   • Armani Acqua di Giò EDT 100ml - 69.90€")
    print("   • Versace Eros EDT 100ml - 59.90€")
    print("   • Paco Rabanne 1 Million EDT 100ml - 64.90€")
    print("\n👤 Connexion admin: admin@parfum.com / admin123")
    print("📱 Utilisateur test WhatsApp: test@parfum.com / admin123")
    print("\n🚀 Démarrez le serveur Flask: python app.py")

if __name__ == '__main__':
    main()
