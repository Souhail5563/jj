"""
Test de création d'une commande avec notification Telegram
"""
from app import app, db
from models import User, Product, Order, OrderItem
from telegram_bot import send_order_notification, send_order_status_update
from datetime import datetime

def test_order_notification():
    with app.app_context():
        # Récupérer un utilisateur et des produits
        user = User.query.filter_by(is_admin=False).first()
        products = Product.query.limit(2).all()
        
        if not user or not products:
            print("❌ Pas assez de données de test. Exécutez d'abord create_test_orders.py")
            return
        
        print(f"👤 Utilisateur: {user.first_name} {user.last_name}")
        print(f"🛍️ Produits: {[p.name for p in products]}")
        
        # Créer une commande de test
        total_amount = sum(p.price for p in products)
        
        order = Order(
            user_id=user.id,
            total_amount=total_amount,
            shipping_address="123 Rue de Test, 75001 Paris",
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
        
        # Test notification nouvelle commande
        print("\n📱 Test notification nouvelle commande...")
        success = send_order_notification(order)
        if success:
            print("✅ Notification nouvelle commande envoyée!")
        else:
            print("❌ Échec notification nouvelle commande")
        
        # Test notification changement de statut
        print("\n📱 Test notification changement de statut...")
        old_status = order.status
        order.status = 'confirmed'
        db.session.commit()
        
        success = send_order_status_update(order, old_status, 'confirmed')
        if success:
            print("✅ Notification changement de statut envoyée!")
        else:
            print("❌ Échec notification changement de statut")
        
        print(f"\n🎯 Commande de test #{order.id} créée et notifications envoyées!")
        return order.id

if __name__ == '__main__':
    order_id = test_order_notification()
    print(f"\nVous pouvez voir la commande dans l'admin: http://127.0.0.1:5001/admin/orders/{order_id}/print")
