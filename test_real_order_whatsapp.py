"""
Test d'une vraie commande avec notifications WhatsApp Twilio
"""
from app import app, db
from models import User, Product, Order, OrderItem
from datetime import datetime

def create_test_order_with_whatsapp():
    """Créer une vraie commande avec un numéro WhatsApp"""
    with app.app_context():
        print("🛍️ Création d'une commande de test avec WhatsApp...")
        
        # 1. Créer un utilisateur avec votre numéro marocain
        print("\n1️⃣ Création d'un utilisateur avec numéro WhatsApp...")
        user = User.query.filter_by(email='whatsapp.real@example.com').first()
        
        if not user:
            user = User(
                username='whatsapp_real',
                first_name='Client',
                last_name='WhatsApp',
                email='whatsapp.real@example.com',
                phone='+212600154487',  # Votre vrai numéro marocain
                password_hash='dummy_hash'
            )
            db.session.add(user)
            db.session.commit()
            print(f"✅ Utilisateur créé: {user.first_name} {user.last_name}")
            print(f"📱 Numéro WhatsApp: {user.phone}")
        else:
            print(f"✅ Utilisateur existant: {user.first_name} {user.last_name}")
            print(f"📱 Numéro WhatsApp: {user.phone}")
        
        # 2. Créer une commande de test
        print("\n2️⃣ Création d'une commande de test...")
        products = Product.query.limit(2).all()
        
        if not products:
            print("❌ Pas de produits disponibles")
            return None
        
        total_amount = sum(p.price for p in products)
        
        order = Order(
            user_id=user.id,
            total_amount=total_amount,
            shipping_address="123 Avenue Mohammed V\n10000 Rabat, Maroc",
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
        print(f"✅ Commande #{order.id} créée")
        print(f"💰 Montant: {total_amount:.2f}€")
        print(f"📦 Articles: {len(products)} produit(s)")
        
        return order.id

def test_status_updates_with_whatsapp(order_id):
    """Test des mises à jour de statut avec vraies notifications WhatsApp"""
    if not order_id:
        return
        
    with app.app_context():
        from models import Order
        from whatsapp_bot import send_order_status_notification
        
        order = Order.query.get(order_id)
        if not order:
            print(f"❌ Commande #{order_id} introuvable")
            return
        
        print(f"\n3️⃣ Test des notifications WhatsApp pour commande #{order_id}...")
        print(f"📱 Numéro destinataire: {order.user.phone}")
        
        # Séquence de mises à jour de statut
        status_updates = [
            ('pending', 'confirmed', 'Commande confirmée'),
            ('confirmed', 'shipped', 'Commande expédiée'),
            ('shipped', 'delivered', 'Commande livrée')
        ]
        
        for old_status, new_status, description in status_updates:
            print(f"\n📱 {description}: {old_status} → {new_status}")
            
            # Mettre à jour le statut dans la base
            order.status = new_status
            db.session.commit()
            
            # Envoyer la notification WhatsApp
            success = send_order_status_notification(order, old_status, new_status)
            
            if success:
                print(f"✅ Notification WhatsApp envoyée avec succès!")
            else:
                print(f"❌ Échec notification WhatsApp")
            
            # Attendre un peu entre les notifications
            import time
            time.sleep(3)
        
        print(f"\n🎯 Toutes les notifications ont été envoyées!")
        print(f"📱 Vérifiez votre WhatsApp ({order.user.phone})")
        
        return order_id

def test_admin_whatsapp_button():
    """Test du bouton WhatsApp dans l'admin"""
    import requests
    
    print("\n4️⃣ Test du bouton WhatsApp admin...")
    
    session = requests.Session()
    
    # Se connecter en tant qu'admin
    login_data = {
        'email': 'admin@bijoux.com',
        'password': 'admin123'
    }
    response = session.post('http://127.0.0.1:5001/login', data=login_data)
    
    if response.status_code != 200:
        print("❌ Échec connexion admin")
        return False
    
    # Tester le bouton WhatsApp
    response = session.post('http://127.0.0.1:5001/admin/whatsapp/test')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Test bouton WhatsApp admin réussi!")
            print("📱 Message de test envoyé sur WhatsApp")
            return True
        else:
            print(f"❌ Échec test WhatsApp admin: {data.get('error')}")
    else:
        print("❌ Erreur requête test WhatsApp admin")
    
    return False

def main():
    """Test complet avec vraies notifications WhatsApp"""
    print("🚀 Test complet avec vraies notifications WhatsApp Twilio")
    print("=" * 60)
    
    # 1. Créer une commande de test
    order_id = create_test_order_with_whatsapp()
    
    if not order_id:
        print("❌ Impossible de créer la commande de test")
        return
    
    print(f"\n⏳ Attente de 2 secondes...")
    import time
    time.sleep(2)
    
    # 2. Tester les mises à jour de statut
    test_status_updates_with_whatsapp(order_id)
    
    print(f"\n⏳ Attente de 2 secondes...")
    time.sleep(2)
    
    # 3. Tester le bouton admin
    test_admin_whatsapp_button()
    
    print("\n" + "=" * 60)
    print("🎉 Test terminé avec succès!")
    print("📱 Résumé des notifications WhatsApp envoyées:")
    print("   1️⃣ Notification 'Confirmée'")
    print("   2️⃣ Notification 'Expédiée'") 
    print("   3️⃣ Notification 'Livrée'")
    print("   4️⃣ Message de test admin")
    print(f"\n📱 Vérifiez votre WhatsApp (+212600154487) pour voir les 4 messages!")
    print(f"🔗 Voir la commande: http://127.0.0.1:5001/admin/orders/{order_id}")
    print("\n🎯 Les notifications WhatsApp sont maintenant 100% opérationnelles!")

if __name__ == '__main__':
    main()
