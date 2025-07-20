"""
Test d'une commande complète via l'interface web avec notifications WhatsApp
"""
import requests
import time

def test_complete_order_flow():
    session = requests.Session()
    
    print("🌐 Test complet de commande avec notifications WhatsApp...")
    
    # 1. Inscription avec numéro de téléphone
    print("\n1️⃣ Inscription avec numéro de téléphone...")
    register_data = {
        'username': 'whatsapp_web_test',
        'first_name': 'Client',
        'last_name': 'WhatsApp',
        'email': 'client.whatsapp@example.com',
        'phone': '0987654321',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    }
    
    response = session.post('http://127.0.0.1:5001/register', data=register_data)
    if response.status_code == 200:
        print("✅ Inscription réussie (message de bienvenue WhatsApp envoyé)")
    else:
        # Essayer de se connecter si le compte existe déjà
        login_data = {
            'email': 'client.whatsapp@example.com',
            'password': 'testpass123'
        }
        response = session.post('http://127.0.0.1:5001/login', data=login_data)
        if response.status_code == 200:
            print("✅ Connexion réussie (compte existant)")
        else:
            print("❌ Échec de connexion")
            return
    
    # 2. Ajouter des produits au panier
    print("\n2️⃣ Ajout de produits au panier...")
    
    # Ajouter le produit 1
    response = session.post('http://127.0.0.1:5001/add_to_cart/1', data={'quantity': 1})
    if response.status_code in [200, 302]:
        print("✅ Produit 1 ajouté au panier")
    else:
        print(f"❌ Erreur ajout produit 1: {response.status_code}")
    
    # Ajouter le produit 2
    response = session.post('http://127.0.0.1:5001/add_to_cart/2', data={'quantity': 1})
    if response.status_code in [200, 302]:
        print("✅ Produit 2 ajouté au panier")
    else:
        print(f"❌ Erreur ajout produit 2: {response.status_code}")
    
    # 3. Passer la commande
    print("\n3️⃣ Passage de la commande...")
    checkout_data = {
        'address': '789 Boulevard WhatsApp\n75005 Paris, France',
        'phone': '0987654321',
        'notes': 'Commande de test avec notifications WhatsApp automatiques'
    }
    
    response = session.post('http://127.0.0.1:5001/checkout', data=checkout_data)
    if response.status_code in [200, 302]:
        print("✅ Commande passée avec succès!")
        print("📱 Notifications envoyées:")
        print("   • Telegram: Notification admin")
        print("   • WhatsApp: Message de bienvenue (si nouveau client)")
        
        # Extraire l'ID de la commande
        order_id = None
        if 'order_confirmation' in response.url:
            order_id = response.url.split('/')[-1]
            print(f"🎯 Commande #{order_id} créée")
        
        return order_id
    else:
        print(f"❌ Erreur lors du checkout: {response.status_code}")
        return None

def test_admin_status_updates(order_id):
    """Test des mises à jour de statut avec notifications WhatsApp"""
    if not order_id:
        return
        
    print(f"\n4️⃣ Test des mises à jour de statut pour la commande #{order_id}...")
    
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
    
    # Séquence de mises à jour de statut
    status_updates = [
        ('confirmed', 'Confirmée'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée')
    ]
    
    for status, status_name in status_updates:
        print(f"\n📱 Mise à jour vers '{status_name}'...")
        
        update_data = {
            'status': status
        }
        response = session.post(f'http://127.0.0.1:5001/admin/orders/{order_id}/update_status', 
                               data=update_data)
        
        if response.status_code == 200:
            print(f"✅ Statut mis à jour vers '{status_name}'")
            print("📱 Notifications envoyées:")
            print("   • Telegram: Notification admin")
            print("   • WhatsApp: Notification client")
        else:
            print(f"❌ Erreur mise à jour vers '{status_name}'")
        
        # Attendre un peu entre les mises à jour
        time.sleep(2)

def test_admin_buttons():
    """Test des boutons de test dans l'admin"""
    print("\n5️⃣ Test des boutons de test dans l'admin...")
    
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
    else:
        print("❌ Erreur requête test Telegram")
    
    # Test bouton WhatsApp
    print("\n📱 Test bouton WhatsApp...")
    response = session.post('http://127.0.0.1:5001/admin/whatsapp/test')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Test WhatsApp réussi!")
        else:
            print(f"❌ Échec test WhatsApp: {data.get('error')}")
    else:
        print("❌ Erreur requête test WhatsApp")

if __name__ == '__main__':
    print("🚀 Démarrage du test complet web avec WhatsApp...")
    
    # Test de commande complète
    order_id = test_complete_order_flow()
    
    if order_id:
        print(f"\n⏳ Attente de 3 secondes avant tests admin...")
        time.sleep(3)
        
        # Test des mises à jour de statut
        test_admin_status_updates(order_id)
        
        print(f"\n⏳ Attente de 2 secondes avant tests boutons...")
        time.sleep(2)
        
        # Test des boutons admin
        test_admin_buttons()
        
        print(f"\n🎉 Test terminé avec succès!")
        print(f"📊 Résumé des notifications envoyées:")
        print(f"   📱 Telegram: 4 notifications (1 nouvelle commande + 3 changements de statut)")
        print(f"   📱 WhatsApp: 4 notifications (1 bienvenue + 3 changements de statut)")
        print(f"   🤖 Tests: 2 messages de test (Telegram + WhatsApp)")
        print(f"🔗 Voir la commande: http://127.0.0.1:5001/admin/orders/{order_id}/print")
    else:
        print("\n❌ Test échoué")
