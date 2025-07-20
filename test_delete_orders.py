import requests

# Test de suppression des commandes
session = requests.Session()

# Connexion en tant qu'admin
login_data = {
    'email': 'admin@bijoux.com',
    'password': 'admin123'
}

# Se connecter
response = session.post('http://127.0.0.1:5001/login', data=login_data)
print(f"Login status: {response.status_code}")

# Tester l'accès à la page des commandes
response = session.get('http://127.0.0.1:5001/admin/orders')
print(f"Admin orders status: {response.status_code}")
if response.status_code == 200:
    print("✅ Page admin/orders accessible")
    # Vérifier si les boutons de suppression sont présents
    if "deleteOrder" in response.text and "deleteSelectedOrders" in response.text:
        print("✅ Fonctionnalités de suppression trouvées")
    else:
        print("❌ Fonctionnalités de suppression non trouvées")
else:
    print("❌ Erreur page admin/orders")

# Tester la route de suppression (sans vraiment supprimer)
print("\n--- Test des routes de suppression ---")

# Test de suppression d'une commande inexistante
response = session.post('http://127.0.0.1:5001/admin/orders/999/delete', 
                       headers={'Content-Type': 'application/json'})
print(f"Delete non-existent order status: {response.status_code}")

# Test de suppression multiple avec liste vide
response = session.post('http://127.0.0.1:5001/admin/orders/delete_multiple',
                       json={'order_ids': []},
                       headers={'Content-Type': 'application/json'})
print(f"Delete multiple empty list status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Response: {data}")

# Test de la route d'impression
response = session.get('http://127.0.0.1:5001/admin/orders/1/print')
print(f"Print order status: {response.status_code}")
if response.status_code == 200:
    print("✅ Page d'impression accessible")
elif response.status_code == 404:
    print("⚠️ Commande #1 non trouvée (normal si pas de commandes)")
else:
    print("❌ Erreur page d'impression")

print("\nTest terminé!")
