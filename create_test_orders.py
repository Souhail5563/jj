from app import app, db
from models import User, Product, Order, OrderItem
from datetime import datetime, timedelta
import random

def create_test_orders():
    with app.app_context():
        # Vérifier qu'on a des utilisateurs et des produits
        users = User.query.filter_by(is_admin=False).all()
        products = Product.query.all()
        
        if not users:
            print("Aucun utilisateur client trouvé. Création d'utilisateurs de test...")
            # Créer quelques utilisateurs de test
            test_users = [
                {
                    'first_name': 'Marie',
                    'last_name': 'Dupont',
                    'email': 'marie.dupont@test.com',
                    'phone': '0123456789'
                },
                {
                    'first_name': 'Pierre',
                    'last_name': 'Martin',
                    'email': 'pierre.martin@test.com',
                    'phone': '0987654321'
                },
                {
                    'first_name': 'Sophie',
                    'last_name': 'Bernard',
                    'email': 'sophie.bernard@test.com',
                    'phone': '0147258369'
                }
            ]
            
            for user_data in test_users:
                user = User(
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    password_hash='dummy_hash'  # Mot de passe factice
                )
                db.session.add(user)
            
            db.session.commit()
            users = User.query.filter_by(is_admin=False).all()
        
        if not products:
            print("Aucun produit trouvé. Veuillez d'abord exécuter init_data.py")
            return
        
        # Créer des commandes de test
        statuses = ['pending', 'confirmed', 'shipped', 'delivered']
        
        for i in range(10):  # Créer 10 commandes
            # Choisir un utilisateur aléatoire
            user = random.choice(users)
            
            # Créer la commande
            order = Order(
                user_id=user.id,
                status=random.choice(statuses),
                total_amount=0,  # Sera calculé après
                shipping_address=f"{random.randint(1, 999)} Rue de Test, {random.randint(10000, 99999)} Ville Test",
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(order)
            db.session.flush()  # Pour obtenir l'ID de la commande
            
            # Ajouter des articles à la commande
            num_items = random.randint(1, 4)
            total_amount = 0
            
            for _ in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                db.session.add(order_item)
                total_amount += product.price * quantity
            
            order.total_amount = total_amount
        
        db.session.commit()
        print("10 commandes de test créées avec succès!")
        
        # Afficher un résumé
        orders_count = Order.query.count()
        print(f"Total des commandes dans la base: {orders_count}")
        
        for status in statuses:
            count = Order.query.filter_by(status=status).count()
            print(f"- {status}: {count} commande(s)")

if __name__ == '__main__':
    create_test_orders()
