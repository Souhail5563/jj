import requests

# Test de connexion admin et accès aux pages
session = requests.Session()

# Connexion en tant qu'admin
login_data = {
    'email': 'admin@bijoux.com',
    'password': 'admin123'
}

# Se connecter
response = session.post('http://127.0.0.1:5001/login', data=login_data)
print(f"Login status: {response.status_code}")

# Tester l'accès au dashboard admin
response = session.get('http://127.0.0.1:5001/admin')
print(f"Admin dashboard status: {response.status_code}")

# Tester l'accès aux commandes
response = session.get('http://127.0.0.1:5001/admin/orders')
print(f"Admin orders status: {response.status_code}")
if response.status_code == 200:
    print("✅ Page admin/orders accessible")
else:
    print("❌ Erreur page admin/orders")

# Tester l'accès au stock
response = session.get('http://127.0.0.1:5001/admin/stock')
print(f"Admin stock status: {response.status_code}")
if response.status_code == 200:
    print("✅ Page admin/stock accessible")
else:
    print("❌ Erreur page admin/stock")

# Tester l'accès aux produits
response = session.get('http://127.0.0.1:5001/admin/products')
print(f"Admin products status: {response.status_code}")
if response.status_code == 200:
    print("✅ Page admin/products accessible")
else:
    print("❌ Erreur page admin/products")
