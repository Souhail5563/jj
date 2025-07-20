"""
Correction du mot de passe admin
"""
from app import app, db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

def fix_admin_password():
    """Corriger le mot de passe admin"""
    with app.app_context():
        print("🔧 CORRECTION DU MOT DE PASSE ADMIN")
        print("=" * 45)
        
        # Trouver l'utilisateur admin
        admin = User.query.filter_by(email='admin@parfum.com').first()
        
        if admin:
            print(f"👤 Utilisateur trouvé: {admin.email}")
            print(f"📧 Email: {admin.email}")
            print(f"👤 Nom: {admin.first_name} {admin.last_name}")
            print(f"🔐 Admin: {'Oui' if admin.is_admin else 'Non'}")
            
            # Vérifier le mot de passe actuel
            current_password = "admin123"
            if check_password_hash(admin.password_hash, current_password):
                print("✅ Le mot de passe actuel est correct")
            else:
                print("❌ Le mot de passe actuel est incorrect")
                print("🔧 Mise à jour du mot de passe...")
                
                # Générer un nouveau hash
                new_hash = generate_password_hash(current_password)
                admin.password_hash = new_hash
                
                db.session.commit()
                print("✅ Mot de passe mis à jour")
                
                # Vérifier le nouveau mot de passe
                if check_password_hash(admin.password_hash, current_password):
                    print("✅ Vérification: Nouveau mot de passe correct")
                else:
                    print("❌ Erreur: Nouveau mot de passe incorrect")
        else:
            print("❌ Utilisateur admin non trouvé")
            print("🔧 Création de l'utilisateur admin...")
            
            # Créer l'utilisateur admin
            admin = User(
                username='admin',
                email='admin@parfum.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='Parfum',
                phone='+212600154488',
                is_admin=True
            )
            
            db.session.add(admin)
            db.session.commit()
            print("✅ Utilisateur admin créé")

def fix_test_user_password():
    """Corriger le mot de passe utilisateur de test"""
    with app.app_context():
        print("\n🔧 CORRECTION DU MOT DE PASSE UTILISATEUR TEST")
        print("=" * 50)
        
        # Trouver l'utilisateur de test
        test_user = User.query.filter_by(email='test@parfum.com').first()
        
        if test_user:
            print(f"👤 Utilisateur trouvé: {test_user.email}")
            
            # Vérifier le mot de passe actuel
            current_password = "admin123"
            if check_password_hash(test_user.password_hash, current_password):
                print("✅ Le mot de passe actuel est correct")
            else:
                print("❌ Le mot de passe actuel est incorrect")
                print("🔧 Mise à jour du mot de passe...")
                
                # Générer un nouveau hash
                new_hash = generate_password_hash(current_password)
                test_user.password_hash = new_hash
                
                db.session.commit()
                print("✅ Mot de passe mis à jour")
        else:
            print("❌ Utilisateur de test non trouvé")
            print("🔧 Création de l'utilisateur de test...")
            
            # Créer l'utilisateur de test
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

def test_login_credentials():
    """Tester les identifiants de connexion"""
    print("\n🧪 TEST DES IDENTIFIANTS DE CONNEXION")
    print("=" * 45)
    
    import requests
    session = requests.Session()
    
    # Test admin
    print("\n1️⃣ Test connexion admin...")
    login_data = {
        'email': 'admin@parfum.com',
        'password': 'admin123'
    }
    
    response = session.post('http://127.0.0.1:5001/login', data=login_data, allow_redirects=False)
    print(f"  Status: {response.status_code}")
    print(f"  Headers: {dict(response.headers)}")
    
    if response.status_code == 302:  # Redirection = succès
        print("  ✅ Connexion admin réussie (redirection)")
        location = response.headers.get('Location', '')
        if 'login' not in location:
            print(f"  ✅ Redirection vers: {location}")
        else:
            print("  ❌ Redirection vers login (échec)")
    elif response.status_code == 200:
        if 'Email ou mot de passe incorrect' in response.text:
            print("  ❌ Connexion admin échouée (identifiants incorrects)")
        else:
            print("  ⚠️ Connexion admin: statut 200 (à vérifier)")
    else:
        print(f"  ❌ Erreur connexion admin: {response.status_code}")
    
    # Test utilisateur normal
    print("\n2️⃣ Test connexion utilisateur normal...")
    session = requests.Session()  # Nouvelle session
    login_data = {
        'email': 'test@parfum.com',
        'password': 'admin123'
    }
    
    response = session.post('http://127.0.0.1:5001/login', data=login_data, allow_redirects=False)
    print(f"  Status: {response.status_code}")
    
    if response.status_code == 302:
        print("  ✅ Connexion utilisateur réussie (redirection)")
        location = response.headers.get('Location', '')
        print(f"  ✅ Redirection vers: {location}")
    elif response.status_code == 200:
        if 'Email ou mot de passe incorrect' in response.text:
            print("  ❌ Connexion utilisateur échouée (identifiants incorrects)")
        else:
            print("  ⚠️ Connexion utilisateur: statut 200 (à vérifier)")
    else:
        print(f"  ❌ Erreur connexion utilisateur: {response.status_code}")

def show_all_users():
    """Afficher tous les utilisateurs"""
    with app.app_context():
        print("\n📋 LISTE DE TOUS LES UTILISATEURS")
        print("=" * 40)
        
        users = User.query.all()
        print(f"📊 Total: {len(users)} utilisateur(s)")
        
        for i, user in enumerate(users, 1):
            print(f"\n{i}️⃣ Utilisateur {i}:")
            print(f"   📧 Email: {user.email}")
            print(f"   👤 Nom: {user.first_name} {user.last_name}")
            print(f"   📱 Téléphone: {user.phone or 'Non renseigné'}")
            print(f"   🔐 Admin: {'Oui' if user.is_admin else 'Non'}")
            print(f"   🆔 ID: {user.id}")
            
            # Test du mot de passe
            if check_password_hash(user.password_hash, 'admin123'):
                print(f"   ✅ Mot de passe 'admin123': Correct")
            else:
                print(f"   ❌ Mot de passe 'admin123': Incorrect")

def main():
    """Correction complète des mots de passe"""
    print("🔐 CORRECTION DES MOTS DE PASSE UTILISATEURS")
    print("=" * 55)
    
    # Afficher les utilisateurs actuels
    show_all_users()
    
    # Corriger les mots de passe
    fix_admin_password()
    fix_test_user_password()
    
    # Tester les connexions
    test_login_credentials()
    
    print("\n" + "=" * 55)
    print("🎉 CORRECTION TERMINÉE")
    print("=" * 55)
    print("✅ Mots de passe corrigés et vérifiés")
    print("✅ Tests de connexion effectués")
    
    print("\n🔑 IDENTIFIANTS DE CONNEXION:")
    print("👨‍💼 Admin:")
    print("   📧 Email: admin@parfum.com")
    print("   🔐 Mot de passe: admin123")
    print("   🌐 Accès: http://127.0.0.1:5001/admin")
    
    print("\n👤 Utilisateur test:")
    print("   📧 Email: test@parfum.com")
    print("   🔐 Mot de passe: admin123")
    print("   🌐 Accès: http://127.0.0.1:5001")
    
    print("\n🌸 Vous pouvez maintenant vous connecter!")

if __name__ == '__main__':
    main()
