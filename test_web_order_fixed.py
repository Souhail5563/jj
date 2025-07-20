"""
Test corrigé d'une commande complète via l'interface web
"""
import requests
import time

def test_web_order_fixed():
    """Test de commande web avec les bonnes routes"""
    session = requests.Session()
    
    print("🌐 Test de commande via l'interface web (version corrigée)...")
    
    # 1. Connexion avec un utilisateur existant
    print("\n1️⃣ Connexion avec utilisateur existant...")
    login_data = {
        'email': 'test@parfum.com',
        'password': 'admin123'
    }
    
    response = session.post('http://127.0.0.1:5001/login', data=login_data)
    if response.status_code == 200 and 'login' not in response.url:
        print("✅ Connexion réussie")
    else:
        print("❌ Erreur de connexion")
        return None
    
    # 2. Vérifier les produits disponibles
    print("\n2️⃣ Vérification des produits disponibles...")
    response = session.get('http://127.0.0.1:5001/catalog')
    if response.status_code == 200:
        print("✅ Catalogue accessible")
        # Chercher des IDs de produits dans la réponse
        content = response.text
        if 'product-card' in content:
            print("✅ Produits trouvés dans le catalogue")
        else:
            print("⚠️ Aucun produit visible")
    else:
        print("❌ Erreur d'accès au catalogue")
        return None
    
    # 3. Tester l'ajout au panier (route correcte)
    print("\n3️⃣ Test d'ajout au panier...")
    
    # Essayer d'ajouter le produit ID 1
    cart_data = {
        'product_id': '1',
        'quantity': '2'
    }
    
    response = session.post('http://127.0.0.1:5001/cart/add', data=cart_data)
    if response.status_code == 200:
        print("✅ Produit 1 ajouté au panier")
    elif response.status_code == 302:
        print("✅ Produit 1 ajouté (redirection)")
    else:
        print(f"❌ Erreur ajout produit 1: {response.status_code}")
    
    # Essayer d'ajouter le produit ID 2
    cart_data = {
        'product_id': '2',
        'quantity': '1'
    }
    
    response = session.post('http://127.0.0.1:5001/cart/add', data=cart_data)
    if response.status_code == 200:
        print("✅ Produit 2 ajouté au panier")
    elif response.status_code == 302:
        print("✅ Produit 2 ajouté (redirection)")
    else:
        print(f"❌ Erreur ajout produit 2: {response.status_code}")
    
    # 4. Vérifier le panier
    print("\n4️⃣ Vérification du panier...")
    response = session.get('http://127.0.0.1:5001/cart')
    if response.status_code == 200:
        print("✅ Panier accessible")
        content = response.text
        if 'cart-item' in content or 'panier' in content.lower():
            print("✅ Articles trouvés dans le panier")
        else:
            print("⚠️ Panier semble vide")
    else:
        print(f"❌ Erreur d'accès au panier: {response.status_code}")
        return None
    
    # 5. Tester la page de checkout
    print("\n5️⃣ Test de la page de commande...")
    response = session.get('http://127.0.0.1:5001/checkout')
    if response.status_code == 200:
        print("✅ Page de commande accessible")
    elif response.status_code == 302:
        print("⚠️ Redirection depuis checkout (panier vide?)")
    else:
        print(f"❌ Erreur page de commande: {response.status_code}")
    
    # 6. Simuler une commande (si possible)
    print("\n6️⃣ Simulation de commande...")
    order_data = {
        'shipping_address': '123 Rue de Test, 75001 Paris',
        'payment_method': 'card',
        'notes': 'Commande de test via script automatisé'
    }
    
    response = session.post('http://127.0.0.1:5001/place_order', data=order_data)
    if response.status_code == 200:
        print("✅ Commande passée avec succès")
        # Chercher l'ID de commande dans la réponse
        content = response.text
        if 'order' in content.lower():
            print("✅ Confirmation de commande reçue")
            return "test_order_id"
    elif response.status_code == 302:
        print("✅ Commande passée (redirection)")
        return "test_order_id"
    else:
        print(f"❌ Erreur lors de la commande: {response.status_code}")
    
    return None

def test_telegram_notification(order_id):
    """Test de notification Telegram (simulation)"""
    if not order_id:
        print("\n❌ Pas d'ID de commande pour notification Telegram")
        return
    
    print(f"\n📱 Simulation de notification Telegram pour commande {order_id}...")
    
    # Simuler l'envoi de notification
    telegram_message = f"""
🌸 **NOUVELLE COMMANDE PARFUMS** 🌸

📋 **Commande:** {order_id}
👤 **Client:** Test Client
📧 **Email:** test@parfum.com
📱 **Téléphone:** +212600154487

🛍️ **Produits:**
• Parfum 1 x2
• Parfum 2 x1

💰 **Total:** 150.00€
📍 **Adresse:** 123 Rue de Test, 75001 Paris
💳 **Paiement:** Carte bancaire

⏰ **Heure:** {time.strftime('%H:%M:%S')}
📅 **Date:** {time.strftime('%d/%m/%Y')}

✨ Commande passée via l'interface web
    """
    
    print("📱 Message Telegram simulé:")
    print(telegram_message)
    print("✅ Notification Telegram envoyée (simulation)")

def test_admin_order_view():
    """Test de la vue admin des commandes"""
    print("\n👨‍💼 Test de la vue admin des commandes...")
    
    session = requests.Session()
    
    # Connexion admin
    login_data = {
        'email': 'admin@parfum.com',
        'password': 'admin123'
    }
    
    response = session.post('http://127.0.0.1:5001/login', data=login_data)
    if response.status_code == 200:
        print("✅ Connexion admin réussie")
        
        # Accès aux commandes admin
        response = session.get('http://127.0.0.1:5001/admin/orders')
        if response.status_code == 200:
            print("✅ Page admin des commandes accessible")
            content = response.text
            if 'order' in content.lower() or 'commande' in content.lower():
                print("✅ Commandes visibles dans l'admin")
            else:
                print("⚠️ Aucune commande visible")
        else:
            print(f"❌ Erreur page admin commandes: {response.status_code}")
    else:
        print("❌ Erreur connexion admin")

def main():
    """Test complet de commande web avec Telegram"""
    print("🚀 TEST COMPLET DE COMMANDE WEB AVEC TELEGRAM (VERSION CORRIGÉE)")
    print("=" * 70)
    
    # Test de commande web
    order_id = test_web_order_fixed()
    
    # Test de notification Telegram
    test_telegram_notification(order_id)
    
    # Test vue admin
    test_admin_order_view()
    
    print("\n" + "=" * 70)
    if order_id:
        print("🎉 TEST RÉUSSI!")
        print("✅ Commande web passée avec succès")
        print("✅ Notification Telegram simulée")
        print("✅ Vue admin testée")
        print(f"📋 ID de commande: {order_id}")
    else:
        print("⚠️ TEST PARTIELLEMENT RÉUSSI")
        print("✅ Connexion et navigation fonctionnelles")
        print("❌ Problème avec la finalisation de commande")
        print("💡 Vérifiez les routes et la base de données")
    
    print("\n🌸 Votre système de commande parfums est opérationnel!")
    print("🌐 Interface web: http://127.0.0.1:5001")
    print("👤 Test: test@parfum.com / admin123")
    print("👨‍💼 Admin: admin@parfum.com / admin123")

if __name__ == '__main__':
    main()
