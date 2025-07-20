"""
Test simple d'une commande avec notification Telegram
"""
import requests
import time

def test_simple_order():
    session = requests.Session()
    
    print("🚀 Test simple de commande avec notification Telegram...")
    
    # 1. Se connecter avec un compte existant
    print("\n1️⃣ Connexion avec compte existant...")
    login_data = {
        'email': 'test.client.telegram@example.com',
        'password': 'testpass123'
    }
    
    response = session.post('http://127.0.0.1:5001/login', data=login_data)
    if response.status_code == 200:
        print("✅ Connexion réussie")
    else:
        print("❌ Échec de connexion")
        return
    
    # 2. Vérifier les produits disponibles
    print("\n2️⃣ Vérification des produits...")
    response = session.get('http://127.0.0.1:5001/catalog')
    if response.status_code == 200:
        print("✅ Catalogue accessible")
    else:
        print("❌ Problème avec le catalogue")
        return
    
    # 3. Ajouter un produit au panier (utiliser l'URL correcte)
    print("\n3️⃣ Ajout au panier...")
    response = session.post('http://127.0.0.1:5001/add_to_cart/2', data={'quantity': 1})
    if response.status_code == 200 or response.status_code == 302:
        print("✅ Produit ajouté au panier")
    else:
        print(f"❌ Erreur ajout panier: {response.status_code}")
        return
    
    # 4. Vérifier le panier
    print("\n4️⃣ Vérification du panier...")
    response = session.get('http://127.0.0.1:5001/cart')
    if response.status_code == 200:
        print("✅ Panier accessible")
    else:
        print("❌ Problème avec le panier")
        return
    
    # 5. Passer la commande
    print("\n5️⃣ Passage de la commande...")
    checkout_data = {
        'address': '789 Boulevard Test\n75003 Paris, France',
        'phone': '0123456789',
        'notes': 'Commande de test avec notification Telegram automatique'
    }
    
    response = session.post('http://127.0.0.1:5001/checkout', data=checkout_data)
    if response.status_code == 200 or response.status_code == 302:
        print("✅ Commande passée avec succès!")
        print("📱 Notification Telegram envoyée automatiquement!")
        
        # Extraire l'ID de la commande
        if 'order_confirmation' in response.url:
            order_id = response.url.split('/')[-1]
            print(f"🎯 Commande #{order_id} créée")
            return order_id
    else:
        print(f"❌ Erreur lors du checkout: {response.status_code}")
        return None

def test_admin_status_update(order_id):
    """Test de mise à jour du statut avec notification"""
    if not order_id:
        return
        
    print(f"\n6️⃣ Test de mise à jour du statut de la commande #{order_id}...")
    
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
    
    # Mettre à jour le statut vers "confirmée"
    update_data = {
        'status': 'confirmed'
    }
    response = session.post(f'http://127.0.0.1:5001/admin/orders/{order_id}/update_status', 
                           data=update_data)
    
    if response.status_code == 200:
        print("✅ Statut mis à jour vers 'Confirmée'")
        print("📱 Notification de changement de statut envoyée!")
        
        # Attendre un peu puis mettre à jour vers "expédiée"
        time.sleep(2)
        
        update_data = {
            'status': 'shipped'
        }
        response = session.post(f'http://127.0.0.1:5001/admin/orders/{order_id}/update_status', 
                               data=update_data)
        
        if response.status_code == 200:
            print("✅ Statut mis à jour vers 'Expédiée'")
            print("📱 Deuxième notification de changement de statut envoyée!")
        else:
            print("❌ Erreur deuxième mise à jour statut")
    else:
        print("❌ Erreur première mise à jour statut")

def test_telegram_button():
    """Test du bouton Telegram dans l'admin"""
    print("\n7️⃣ Test du bouton Telegram dans l'admin...")
    
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
    
    # Tester le bouton Telegram
    response = session.post('http://127.0.0.1:5001/admin/telegram/test')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Test Telegram réussi!")
            print("📱 Message de test envoyé!")
        else:
            print(f"❌ Échec test Telegram: {data.get('error')}")
    else:
        print("❌ Erreur requête test Telegram")

if __name__ == '__main__':
    print("🎉 Démarrage du test complet Telegram...")
    
    # Test de commande
    order_id = test_simple_order()
    
    if order_id:
        print(f"\n⏳ Attente de 3 secondes avant tests admin...")
        time.sleep(3)
        
        # Test de mise à jour de statut
        test_admin_status_update(order_id)
        
        print(f"\n⏳ Attente de 2 secondes avant test bouton...")
        time.sleep(2)
        
        # Test du bouton Telegram
        test_telegram_button()
        
        print(f"\n🎉 Test terminé avec succès!")
        print(f"📊 Vérifiez votre Telegram pour voir toutes les notifications:")
        print(f"   1. Notification de nouvelle commande")
        print(f"   2. Notification de changement vers 'Confirmée'")
        print(f"   3. Notification de changement vers 'Expédiée'")
        print(f"   4. Message de test de connexion")
        print(f"🔗 Voir la commande: http://127.0.0.1:5001/admin/orders/{order_id}/print")
    else:
        print("\n❌ Test échoué")
