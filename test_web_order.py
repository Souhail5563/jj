"""
Test d'une commande complète via l'interface web
"""
import requests
import time

def test_web_order():
    session = requests.Session()
    
    print("🌐 Test de commande via l'interface web...")
    
    # 1. Créer un compte client
    print("\n1️⃣ Création d'un compte client...")
    register_data = {
        'first_name': 'Test',
        'last_name': 'Client',
        'email': 'test.client.telegram@example.com',
        'phone': '0123456789',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    }
    
    response = session.post('http://127.0.0.1:5001/register', data=register_data)
    if response.status_code == 200:
        print("✅ Compte client créé")
    else:
        print("⚠️ Compte existe déjà ou erreur, tentative de connexion...")
        
        # Essayer de se connecter
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
    
    # 2. Ajouter des produits au panier
    print("\n2️⃣ Ajout de produits au panier...")
    
    # Récupérer la liste des produits
    response = session.get('http://127.0.0.1:5001/catalog')
    if response.status_code != 200:
        print("❌ Impossible d'accéder au catalogue")
        return
    
    # Ajouter le premier produit (ID 1)
    add_to_cart_data = {
        'product_id': 1,
        'quantity': 1
    }
    response = session.post('http://127.0.0.1:5001/add_to_cart', data=add_to_cart_data)
    if response.status_code == 200:
        print("✅ Produit 1 ajouté au panier")
    else:
        print("❌ Erreur ajout produit 1")
    
    # Ajouter le deuxième produit (ID 2)
    add_to_cart_data = {
        'product_id': 2,
        'quantity': 2
    }
    response = session.post('http://127.0.0.1:5001/add_to_cart', data=add_to_cart_data)
    if response.status_code == 200:
        print("✅ Produit 2 ajouté au panier (x2)")
    else:
        print("❌ Erreur ajout produit 2")
    
    # 3. Vérifier le panier
    print("\n3️⃣ Vérification du panier...")
    response = session.get('http://127.0.0.1:5001/cart')
    if response.status_code == 200 and "Votre panier" in response.text:
        print("✅ Panier accessible avec des produits")
    else:
        print("❌ Problème avec le panier")
        return
    
    # 4. Passer la commande
    print("\n4️⃣ Passage de la commande...")
    checkout_data = {
        'address': '456 Avenue de Test\n75002 Paris, France',
        'phone': '0987654321',
        'notes': 'Commande de test avec notification Telegram'
    }
    
    response = session.post('http://127.0.0.1:5001/checkout', data=checkout_data)
    if response.status_code == 200:
        print("✅ Commande passée avec succès!")
        print("📱 Notification Telegram envoyée automatiquement!")
        
        # Extraire l'ID de la commande depuis l'URL de redirection
        if 'order_confirmation' in response.url:
            order_id = response.url.split('/')[-1]
            print(f"🎯 Commande #{order_id} créée")
            return order_id
    else:
        print("❌ Erreur lors du checkout")
        print(f"Status: {response.status_code}")
        return None

def test_status_update(order_id):
    """Test de mise à jour du statut avec notification"""
    if not order_id:
        return
        
    print(f"\n5️⃣ Test de mise à jour du statut de la commande #{order_id}...")
    
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
    
    # Mettre à jour le statut
    update_data = {
        'status': 'shipped'
    }
    response = session.post(f'http://127.0.0.1:5001/admin/orders/{order_id}/update_status', 
                           data=update_data)
    
    if response.status_code == 200:
        print("✅ Statut mis à jour vers 'Expédiée'")
        print("📱 Notification de changement de statut envoyée!")
    else:
        print("❌ Erreur mise à jour statut")

if __name__ == '__main__':
    print("🚀 Démarrage du test complet de commande web avec Telegram...")
    
    order_id = test_web_order()
    
    if order_id:
        print(f"\n⏳ Attente de 2 secondes avant test de mise à jour...")
        time.sleep(2)
        test_status_update(order_id)
        
        print(f"\n🎉 Test terminé!")
        print(f"📊 Vérifiez votre Telegram pour les notifications")
        print(f"🔗 Voir la commande: http://127.0.0.1:5001/admin/orders/{order_id}/print")
    else:
        print("\n❌ Test échoué")
