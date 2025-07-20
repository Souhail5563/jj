"""
Test complet d'une commande avec notifications WhatsApp
"""
from app import app, db
from models import User, Product, Order, OrderItem
from whatsapp_bot import send_order_status_notification, send_welcome_message
from datetime import datetime

def test_whatsapp_notifications():
    with app.app_context():
        print("🚀 Test des notifications WhatsApp...")
        
        # 1. Créer un utilisateur avec numéro de téléphone
        print("\n1️⃣ Création d'un utilisateur avec téléphone...")
        user = User.query.filter_by(email='whatsapp.test@example.com').first()
        
        if not user:
            user = User(
                username='whatsapp_test',
                first_name='Test',
                last_name='WhatsApp',
                email='whatsapp.test@example.com',
                phone='0123456789',  # Numéro français
                password_hash='dummy_hash'
            )
            db.session.add(user)
            db.session.commit()
            print(f"✅ Utilisateur créé: {user.first_name} {user.last_name}")
            
            # Test message de bienvenue
            print("\n📱 Test message de bienvenue...")
            success = send_welcome_message(user)
            if success:
                print("✅ Message de bienvenue envoyé!")
            else:
                print("❌ Échec message de bienvenue")
        else:
            print(f"✅ Utilisateur existant: {user.first_name} {user.last_name}")
        
        # 2. Créer une commande de test
        print("\n2️⃣ Création d'une commande de test...")
        products = Product.query.limit(2).all()
        
        if not products:
            print("❌ Pas de produits disponibles")
            return
        
        total_amount = sum(p.price for p in products)
        
        order = Order(
            user_id=user.id,
            total_amount=total_amount,
            shipping_address="456 Avenue WhatsApp\n75004 Paris, France",
            status='pending'
        )
        db.session.add(order)
        db.session.flush()
        
        # Ajouter les articles
        for product in products:
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=1,
                price=product.price
            )
            db.session.add(order_item)
        
        db.session.commit()
        print(f"✅ Commande #{order.id} créée (Montant: {total_amount:.2f}€)")
        
        # 3. Test des notifications de changement de statut
        print("\n3️⃣ Test des notifications de changement de statut...")
        
        # Changement vers "confirmée"
        print("\n📱 Test notification: En attente → Confirmée")
        old_status = order.status
        order.status = 'confirmed'
        db.session.commit()
        
        success = send_order_status_notification(order, old_status, 'confirmed')
        if success:
            print("✅ Notification 'Confirmée' envoyée!")
        else:
            print("❌ Échec notification 'Confirmée'")
        
        # Attendre un peu
        import time
        time.sleep(2)
        
        # Changement vers "expédiée"
        print("\n📱 Test notification: Confirmée → Expédiée")
        old_status = order.status
        order.status = 'shipped'
        db.session.commit()
        
        success = send_order_status_notification(order, old_status, 'shipped')
        if success:
            print("✅ Notification 'Expédiée' envoyée!")
        else:
            print("❌ Échec notification 'Expédiée'")
        
        time.sleep(2)
        
        # Changement vers "livrée"
        print("\n📱 Test notification: Expédiée → Livrée")
        old_status = order.status
        order.status = 'delivered'
        db.session.commit()
        
        success = send_order_status_notification(order, old_status, 'delivered')
        if success:
            print("✅ Notification 'Livrée' envoyée!")
        else:
            print("❌ Échec notification 'Livrée'")
        
        print(f"\n🎯 Test terminé! Commande #{order.id} créée avec notifications WhatsApp")
        return order.id

def test_phone_number_cleaning():
    """Test du nettoyage des numéros de téléphone"""
    from whatsapp_bot import clean_phone_number
    
    print("\n🧹 Test du nettoyage des numéros de téléphone...")
    
    test_numbers = [
        "01 23 45 67 89",
        "0123456789",
        "+33123456789",
        "33123456789",
        "01.23.45.67.89",
        "01-23-45-67-89",
        "+33 1 23 45 67 89"
    ]
    
    for number in test_numbers:
        cleaned = clean_phone_number(number)
        print(f"  {number} → {cleaned}")

def test_admin_interface():
    """Test de l'interface admin avec WhatsApp"""
    import requests
    
    print("\n🔧 Test de l'interface admin WhatsApp...")
    
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
    
    # Tester le bouton WhatsApp
    response = session.post('http://127.0.0.1:5001/admin/whatsapp/test')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Test WhatsApp admin réussi!")
        else:
            print(f"❌ Échec test WhatsApp admin: {data.get('error')}")
    else:
        print("❌ Erreur requête test WhatsApp admin")

if __name__ == '__main__':
    print("🎉 Démarrage du test complet WhatsApp...")
    
    # Test des notifications
    order_id = test_whatsapp_notifications()
    
    # Test du nettoyage des numéros
    test_phone_number_cleaning()
    
    # Test de l'interface admin
    test_admin_interface()
    
    print(f"\n🎉 Test terminé avec succès!")
    print(f"📊 Vérifiez les logs pour voir les messages WhatsApp simulés")
    if order_id:
        print(f"🔗 Voir la commande: http://127.0.0.1:5001/admin/orders/{order_id}/print")
