import requests

# Test de connexion admin et accès au footer
session = requests.Session()

# Connexion en tant qu'admin
login_data = {
    'email': 'admin@bijoux.com',
    'password': 'admin123'
}

# Se connecter
response = session.post('http://127.0.0.1:5001/login', data=login_data)
print(f"Login status: {response.status_code}")

# Tester l'accès au footer
response = session.get('http://127.0.0.1:5001/admin/footer')
print(f"Admin footer status: {response.status_code}")
if response.status_code == 200:
    print("✅ Page admin/footer accessible")
    # Vérifier si les paramètres sont chargés
    if "Bijoux Store" in response.text:
        print("✅ Paramètres du footer trouvés")
    else:
        print("❌ Paramètres du footer non trouvés")
else:
    print("❌ Erreur page admin/footer")

# Tester la page d'accueil pour voir le nouveau footer
response = session.get('http://127.0.0.1:5001/')
print(f"Homepage status: {response.status_code}")
if response.status_code == 200:
    print("✅ Page d'accueil accessible")
    # Vérifier si le nouveau footer est affiché
    if "Newsletter" in response.text and "contact@bijoux-store.com" in response.text:
        print("✅ Nouveau footer affiché sur la page d'accueil")
    else:
        print("❌ Nouveau footer non trouvé sur la page d'accueil")
else:
    print("❌ Erreur page d'accueil")

print("\nTest terminé!")
