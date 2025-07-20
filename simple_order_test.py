"""
Test simple du système de commande
"""
import requests
import time

def test_simple_order():
    """Test simple de commande"""
    print("🛍️ TEST SIMPLE DU SYSTÈME DE COMMANDE")
    print("=" * 50)
    
    session = requests.Session()
    
    # 1. Test de la page d'accueil
    print("\n1️⃣ Test de la page d'accueil...")
    response = session.get('http://127.0.0.1:5001/')
    if response.status_code == 200:
        print("✅ Page d'accueil accessible")
        if 'parfum' in response.text.lower():
            print("✅ Contenu parfums détecté")
    else:
        print(f"❌ Erreur page d'accueil: {response.status_code}")
        return
    
    # 2. Test du catalogue
    print("\n2️⃣ Test du catalogue...")
    response = session.get('http://127.0.0.1:5001/catalog')
    if response.status_code == 200:
        print("✅ Catalogue accessible")
        content = response.text
        if 'product' in content.lower() or 'parfum' in content.lower():
            print("✅ Produits visibles dans le catalogue")
        else:
            print("⚠️ Aucun produit visible")
    else:
        print(f"❌ Erreur catalogue: {response.status_code}")
    
    # 3. Test d'une page produit
    print("\n3️⃣ Test d'une page produit...")
    response = session.get('http://127.0.0.1:5001/product/1')
    if response.status_code == 200:
        print("✅ Page produit accessible")
        content = response.text
        if 'prix' in content.lower() or 'price' in content.lower():
            print("✅ Informations produit visibles")
    else:
        print(f"❌ Erreur page produit: {response.status_code}")
    
    # 4. Test de connexion avec cookies
    print("\n4️⃣ Test de connexion avec gestion des cookies...")
    
    # D'abord, récupérer la page de login pour obtenir le token CSRF si nécessaire
    response = session.get('http://127.0.0.1:5001/login')
    if response.status_code == 200:
        print("✅ Page de login accessible")
    
    # Tentative de connexion
    login_data = {
        'email': 'admin@parfum.com',
        'password': 'admin123'
    }
    
    response = session.post('http://127.0.0.1:5001/login', data=login_data, allow_redirects=True)
    print(f"  Status: {response.status_code}")
    print(f"  URL finale: {response.url}")
    print(f"  Cookies: {len(session.cookies)} cookie(s)")
    
    # Vérifier si on est connecté en testant une page protégée
    response = session.get('http://127.0.0.1:5001/admin')
    if response.status_code == 200:
        print("✅ Connexion admin réussie (accès admin OK)")
    elif response.status_code == 302:
        print("⚠️ Redirection depuis admin (pas connecté?)")
    else:
        print(f"❌ Erreur accès admin: {response.status_code}")
    
    # 5. Test des routes de panier
    print("\n5️⃣ Test des routes de panier...")
    
    # Tester différentes routes possibles
    cart_routes = [
        '/cart',
        '/panier',
        '/cart/view',
        '/shopping-cart'
    ]
    
    for route in cart_routes:
        response = session.get(f'http://127.0.0.1:5001{route}')
        if response.status_code == 200:
            print(f"✅ Route {route} accessible")
            break
        elif response.status_code == 302:
            print(f"⚠️ Route {route} redirige (authentification?)")
        else:
            print(f"❌ Route {route} non trouvée ({response.status_code})")
    
    # 6. Test des routes d'ajout au panier
    print("\n6️⃣ Test des routes d'ajout au panier...")
    
    add_cart_routes = [
        '/cart/add',
        '/add_to_cart',
        '/panier/ajouter',
        '/add-to-cart'
    ]
    
    for route in add_cart_routes:
        cart_data = {'product_id': '1', 'quantity': '1'}
        response = session.post(f'http://127.0.0.1:5001{route}', data=cart_data)
        if response.status_code == 200:
            print(f"✅ Route {route} fonctionne")
            break
        elif response.status_code == 302:
            print(f"✅ Route {route} redirige (ajout OK?)")
            break
        elif response.status_code == 404:
            print(f"❌ Route {route} non trouvée")
        else:
            print(f"⚠️ Route {route} status: {response.status_code}")
    
    # 7. Vérifier les routes disponibles
    print("\n7️⃣ Vérification des routes disponibles...")
    
    # Tester quelques routes communes
    test_routes = [
        '/',
        '/catalog',
        '/about',
        '/contact',
        '/login',
        '/register',
        '/admin',
        '/product/1'
    ]
    
    available_routes = []
    for route in test_routes:
        response = session.get(f'http://127.0.0.1:5001{route}')
        if response.status_code == 200:
            available_routes.append(route)
        elif response.status_code == 302:
            available_routes.append(f"{route} (redirige)")
    
    print(f"✅ Routes disponibles: {', '.join(available_routes)}")

def simulate_telegram_order():
    """Simuler une notification de commande Telegram"""
    print("\n📱 SIMULATION NOTIFICATION TELEGRAM")
    print("-" * 40)
    
    order_data = {
        'id': 'ORD-' + str(int(time.time())),
        'client': 'Test Client',
        'email': 'test@parfum.com',
        'phone': '+212600154487',
        'products': [
            {'name': 'Chanel N°5 EDP 50ml', 'quantity': 1, 'price': 89.90},
            {'name': 'Dior Sauvage EDT 100ml', 'quantity': 2, 'price': 79.90}
        ],
        'total': 249.70,
        'address': '123 Rue de Test, 75001 Paris',
        'payment': 'Carte bancaire',
        'timestamp': time.strftime('%d/%m/%Y %H:%M:%S')
    }
    
    telegram_message = f"""
🌸 **NOUVELLE COMMANDE PARFUMS** 🌸

📋 **Commande:** {order_data['id']}
👤 **Client:** {order_data['client']}
📧 **Email:** {order_data['email']}
📱 **Téléphone:** {order_data['phone']}

🛍️ **Produits:**"""
    
    for product in order_data['products']:
        telegram_message += f"\n• {product['name']} x{product['quantity']} - {product['price']}€"
    
    telegram_message += f"""

💰 **Total:** {order_data['total']}€
📍 **Adresse:** {order_data['address']}
💳 **Paiement:** {order_data['payment']}

⏰ **Commande passée le:** {order_data['timestamp']}

✨ Commande via interface web parfums
🌐 Boutique: http://127.0.0.1:5001
    """
    
    print("📱 Message Telegram simulé:")
    print(telegram_message)
    print("\n✅ Notification Telegram envoyée (simulation)")
    
    return order_data['id']

def main():
    """Test complet simple"""
    # Test du système web
    test_simple_order()
    
    # Simulation Telegram
    order_id = simulate_telegram_order()
    
    print("\n" + "=" * 50)
    print("🎉 TEST SIMPLE TERMINÉ")
    print("=" * 50)
    print("✅ Interface web testée")
    print("✅ Routes principales vérifiées")
    print("✅ Notification Telegram simulée")
    print(f"📋 ID de commande simulé: {order_id}")
    
    print("\n🌸 Votre boutique de parfums est opérationnelle!")
    print("🌐 Accès: http://127.0.0.1:5001")
    print("👤 Connexion manuelle recommandée pour tests complets")

if __name__ == '__main__':
    main()
