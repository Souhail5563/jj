"""
Configuration des utilisateurs de test
"""
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def setup_test_users():
    """Créer les utilisateurs de test"""
    with app.app_context():
        print("👤 Configuration des utilisateurs de test...")
        
        # Vérifier les utilisateurs existants
        users = User.query.all()
        print(f"📊 Utilisateurs existants: {len(users)}")
        
        for user in users:
            print(f"  • {user.email} ({'Admin' if user.is_admin else 'Client'})")
        
        # Créer l'utilisateur de test s'il n'existe pas
        test_user = User.query.filter_by(email='test@parfum.com').first()
        if not test_user:
            print("\n🔧 Création de l'utilisateur de test...")
            test_user = User(
                username='testuser',
                email='test@parfum.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Test',
                last_name='User',
                phone='+212600154487',
                is_admin=False
            )
            db.session.add(test_user)
            db.session.commit()
            print("✅ Utilisateur de test créé")
        else:
            print("✅ Utilisateur de test existe déjà")
        
        # Créer l'admin s'il n'existe pas
        admin_user = User.query.filter_by(email='admin@parfum.com').first()
        if not admin_user:
            print("\n🔧 Création de l'utilisateur admin...")
            admin_user = User(
                username='admin',
                email='admin@parfum.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='Parfum',
                phone='+212600154488',
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Utilisateur admin créé")
        else:
            print("✅ Utilisateur admin existe déjà")
        
        print("\n📋 Résumé des utilisateurs:")
        users = User.query.all()
        for user in users:
            print(f"  • {user.email} - {user.first_name} {user.last_name} ({'Admin' if user.is_admin else 'Client'})")

def test_login():
    """Tester la connexion des utilisateurs"""
    print("\n🔐 Test de connexion des utilisateurs...")
    
    import requests
    session = requests.Session()
    
    # Test connexion utilisateur normal
    print("\n1️⃣ Test connexion utilisateur normal...")
    login_data = {
        'email': 'test@parfum.com',
        'password': 'admin123'
    }
    
    response = session.post('http://127.0.0.1:5001/login', data=login_data)
    print(f"  Status: {response.status_code}")
    print(f"  URL finale: {response.url}")
    
    if 'login' not in response.url and response.status_code == 200:
        print("  ✅ Connexion utilisateur réussie")
        
        # Test accès au panier
        response = session.get('http://127.0.0.1:5001/cart')
        if response.status_code == 200:
            print("  ✅ Accès au panier autorisé")
        else:
            print(f"  ❌ Accès au panier refusé: {response.status_code}")
    else:
        print("  ❌ Connexion utilisateur échouée")
    
    # Test connexion admin
    print("\n2️⃣ Test connexion admin...")
    session = requests.Session()  # Nouvelle session
    login_data = {
        'email': 'admin@parfum.com',
        'password': 'admin123'
    }
    
    response = session.post('http://127.0.0.1:5001/login', data=login_data)
    print(f"  Status: {response.status_code}")
    print(f"  URL finale: {response.url}")
    
    if 'login' not in response.url and response.status_code == 200:
        print("  ✅ Connexion admin réussie")
        
        # Test accès admin
        response = session.get('http://127.0.0.1:5001/admin')
        if response.status_code == 200:
            print("  ✅ Accès admin autorisé")
        else:
            print(f"  ❌ Accès admin refusé: {response.status_code}")
    else:
        print("  ❌ Connexion admin échouée")

def main():
    """Configuration complète des utilisateurs de test"""
    print("🚀 CONFIGURATION DES UTILISATEURS DE TEST")
    print("=" * 50)
    
    # Configuration des utilisateurs
    setup_test_users()
    
    # Test des connexions
    test_login()
    
    print("\n" + "=" * 50)
    print("✅ CONFIGURATION TERMINÉE")
    print("👤 Utilisateurs de test configurés:")
    print("   • test@parfum.com / admin123 (Client)")
    print("   • admin@parfum.com / admin123 (Admin)")
    print("\n🌐 Testez maintenant sur: http://127.0.0.1:5001")

if __name__ == '__main__':
    main()
