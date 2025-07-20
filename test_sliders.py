import requests

# Test de connexion admin et accès aux sliders
session = requests.Session()

# Connexion en tant qu'admin
login_data = {
    'email': 'admin@bijoux.com',
    'password': 'admin123'
}

# Se connecter
response = session.post('http://127.0.0.1:5001/login', data=login_data)
print(f"Login status: {response.status_code}")

# Tester l'accès aux sliders
response = session.get('http://127.0.0.1:5001/admin/sliders')
print(f"Admin sliders status: {response.status_code}")
if response.status_code == 200:
    print("✅ Page admin/sliders accessible")
    # Vérifier si les sliders sont listés
    if "Collection Exclusive 2024" in response.text:
        print("✅ Sliders de démonstration trouvés")
    else:
        print("❌ Sliders de démonstration non trouvés")
else:
    print("❌ Erreur page admin/sliders")

# Tester l'accès à la page d'ajout de slider
response = session.get('http://127.0.0.1:5001/admin/sliders/add')
print(f"Add slider status: {response.status_code}")
if response.status_code == 200:
    print("✅ Page d'ajout de slider accessible")
else:
    print("❌ Erreur page d'ajout de slider")

print("\nTest terminé!")
