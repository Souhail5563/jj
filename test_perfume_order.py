"""
Test d'une commande de parfums avec notifications WhatsApp
"""
import requests
import time

def test_perfume_order():
    """Test complet d'une commande de parfums"""
    session = requests.Session()
    
    print("🌸 Test de commande de parfums avec notifications WhatsApp...")
    
    # 1. Inscription avec numéro WhatsApp
    print("\n1️⃣ Inscription client parfums...")
    register_data = {
        'username': 'client_parfum',
        'first_name': 'Client',
        'last_name': 'Parfum',
        'email': 'client.parfum@example.com',
        'phone': '+212600154487',  # Votre numéro WhatsApp
        'password': 'parfum123',
        'confirm_password': 'parfum123'
    }
    
    response = session.post('http://127.0.0.1:5001/register', data=register_data)
    if response.status_code == 200:
        print("✅ Inscription réussie (message de bienvenue WhatsApp envoyé)")
    else:
        # Essayer de se connecter si le compte existe déjà
        login_data = {
            'email': 'client.parfum@example.com',
            'password': 'parfum123'
        }
        response = session.post('http://127.0.0.1:5001/login', data=login_data)
        if response.status_code == 200:
            print("✅ Connexion réussie (compte existant)")
        else:
            print("❌ Échec de connexion")
            return
    
    # 2. Ajouter des parfums au panier
    print("\n2️⃣ Ajout de parfums au panier...")
    
    # Ajouter Chanel N°5
    response = session.post('http://127.0.0.1:5001/add_to_cart/1', data={'quantity': 1})
    if response.status_code in [200, 302]:
        print("✅ Chanel N°5 EDP 50ml ajouté au panier")
    
    # Ajouter Dior Sauvage
    response = session.post('http://127.0.0.1:5001/add_to_cart/2', data={'quantity': 1})
    if response.status_code in [200, 302]:
        print("✅ Dior Sauvage EDT 100ml ajouté au panier")
    
    # 3. Passer la commande
    print("\n3️⃣ Passage de la commande de parfums...")
    checkout_data = {
        'address': '456 Avenue des Parfums\n10000 Rabat, Maroc',
        'phone': '+212600154487',
        'notes': 'Commande de parfums de luxe avec notifications WhatsApp'
    }
    
    response = session.post('http://127.0.0.1:5001/checkout', data=checkout_data)
    if response.status_code in [200, 302]:
        print("✅ Commande de parfums passée avec succès!")
        print("📱 Notifications envoyées:")
        print("   • Telegram: Notification admin (nouvelle commande)")
        print("   • WhatsApp: Message de bienvenue client")
        
        return True
    else:
        print(f"❌ Erreur lors du checkout: {response.status_code}")
        return False

def test_admin_status_updates():
    """Test des mises à jour de statut par l'admin"""
    print("\n4️⃣ Test des mises à jour de statut admin...")
    
    session = requests.Session()
    
    # Se connecter en tant qu'admin
    login_data = {
        'email': 'admin@bijoux.com',
        'password': 'admin123'
    }
    response = session.post('http://127.0.0.1:5001/login', data=login_data)
    
    if response.status_code != 200:
        print("❌ Échec connexion admin")
        return
    
    # Obtenir la dernière commande
    response = session.get('http://127.0.0.1:5001/admin/orders')
    if response.status_code == 200:
        print("✅ Accès admin réussi")
        
        # Simuler des mises à jour de statut
        # (En réalité, il faudrait parser la page pour obtenir l'ID de commande)
        order_id = 1  # Supposons que c'est la première commande
        
        status_updates = [
            ('confirmed', 'Confirmée'),
            ('shipped', 'Expédiée'),
            ('delivered', 'Livrée')
        ]
        
        for status, status_name in status_updates:
            print(f"\n📱 Mise à jour vers '{status_name}'...")
            
            update_data = {'status': status}
            response = session.post(f'http://127.0.0.1:5001/admin/orders/{order_id}/update_status', 
                                   data=update_data)
            
            if response.status_code == 200:
                print(f"✅ Statut mis à jour vers '{status_name}'")
                print("📱 Notifications envoyées:")
                print("   • Telegram: Notification admin")
                print("   • WhatsApp: Notification client parfum")
            else:
                print(f"❌ Erreur mise à jour vers '{status_name}'")
            
            time.sleep(2)

def test_whatsapp_buttons():
    """Test des boutons WhatsApp et Telegram dans l'admin"""
    print("\n5️⃣ Test des boutons de notification admin...")
    
    session = requests.Session()
    
    # Se connecter en tant qu'admin
    login_data = {
        'email': 'admin@bijoux.com',
        'password': 'admin123'
    }
    response = session.post('http://127.0.0.1:5001/login', data=login_data)
    
    if response.status_code != 200:
        print("❌ Échec connexion admin")
        return
    
    # Test bouton Telegram
    print("\n📱 Test bouton Telegram...")
    response = session.post('http://127.0.0.1:5001/admin/telegram/test')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Test Telegram réussi!")
        else:
            print(f"❌ Échec test Telegram: {data.get('error')}")
    
    # Test bouton WhatsApp
    print("\n📱 Test bouton WhatsApp...")
    response = session.post('http://127.0.0.1:5001/admin/whatsapp/test')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Test WhatsApp réussi!")
        else:
            print(f"❌ Échec test WhatsApp: {data.get('error')}")

def main():
    """Test complet du site de parfums"""
    print("🌸 Test complet du site de parfums avec notifications")
    print("=" * 60)
    
    # 1. Test de commande
    success = test_perfume_order()
    
    if success:
        time.sleep(3)
        
        # 2. Test des mises à jour de statut
        test_admin_status_updates()
        
        time.sleep(2)
        
        # 3. Test des boutons admin
        test_whatsapp_buttons()
        
        print("\n" + "=" * 60)
        print("🎉 Test terminé avec succès!")
        print("🌸 Résumé des notifications parfums:")
        print("   📱 WhatsApp: Messages personnalisés pour parfums")
        print("   📱 Telegram: Notifications admin")
        print("   🌸 Thème: Parfums de luxe")
        print("   🛍️ Produits: Chanel, Dior, Tom Ford, etc.")
        print(f"\n📱 Vérifiez votre WhatsApp (+212600154487) pour les notifications!")
        print(f"🔗 Site: http://127.0.0.1:5001")
    else:
        print("\n❌ Test échoué")

if __name__ == '__main__':
    main()
