"""
Vérification de la préparation pour le déploiement Railway
"""
import os
import json

def check_file_exists(filename, description):
    """Vérifier si un fichier existe"""
    if os.path.exists(filename):
        print(f"✅ {description}: {filename}")
        return True
    else:
        print(f"❌ {description}: {filename} - MANQUANT")
        return False

def check_file_content(filename, required_content, description):
    """Vérifier le contenu d'un fichier"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            if required_content in content:
                print(f"✅ {description}: Configuration OK")
                return True
            else:
                print(f"⚠️ {description}: Configuration à vérifier")
                return False
    except FileNotFoundError:
        print(f"❌ {description}: Fichier {filename} non trouvé")
        return False

def check_railway_readiness():
    """Vérifier si le projet est prêt pour Railway"""
    print("🚂 VÉRIFICATION DE LA PRÉPARATION RAILWAY")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 0
    
    # 1. Fichiers essentiels
    print("\n📁 FICHIERS ESSENTIELS:")
    essential_files = [
        ("app.py", "Application Flask principale"),
        ("requirements.txt", "Dépendances Python"),
        ("Procfile", "Configuration de démarrage"),
        ("gunicorn_config.py", "Configuration serveur"),
        ("railway.json", "Configuration Railway")
    ]
    
    for filename, description in essential_files:
        if check_file_exists(filename, description):
            checks_passed += 1
        total_checks += 1
    
    # 2. Fichiers optionnels mais recommandés
    print("\n📋 FICHIERS RECOMMANDÉS:")
    optional_files = [
        (".gitignore", "Fichiers à ignorer par Git"),
        (".env.example", "Exemple de variables d'environnement"),
        ("README_RAILWAY.md", "Documentation de déploiement")
    ]
    
    for filename, description in optional_files:
        check_file_exists(filename, description)
    
    # 3. Vérification du contenu
    print("\n🔧 VÉRIFICATION DU CONTENU:")
    
    # Vérifier requirements.txt
    if check_file_content("requirements.txt", "Flask", "Requirements.txt contient Flask"):
        checks_passed += 1
    total_checks += 1
    
    if check_file_content("requirements.txt", "gunicorn", "Requirements.txt contient Gunicorn"):
        checks_passed += 1
    total_checks += 1
    
    # Vérifier Procfile
    if check_file_content("Procfile", "gunicorn", "Procfile configuré pour Gunicorn"):
        checks_passed += 1
    total_checks += 1
    
    # Vérifier app.py pour la production
    if check_file_content("app.py", "load_dotenv", "App.py configuré pour la production"):
        checks_passed += 1
    total_checks += 1
    
    # 4. Structure des dossiers
    print("\n📂 STRUCTURE DES DOSSIERS:")
    required_dirs = [
        ("templates", "Templates HTML"),
        ("static", "Fichiers statiques"),
        ("static/css", "Feuilles de style"),
        ("static/js", "Scripts JavaScript"),
        ("static/images", "Images"),
        ("static/uploads", "Uploads utilisateur")
    ]
    
    for dirname, description in required_dirs:
        if os.path.exists(dirname) and os.path.isdir(dirname):
            print(f"✅ {description}: {dirname}")
            checks_passed += 1
        else:
            print(f"⚠️ {description}: {dirname} - Manquant ou non-dossier")
        total_checks += 1
    
    # 5. Vérification des templates essentiels
    print("\n🎨 TEMPLATES ESSENTIELS:")
    essential_templates = [
        ("templates/base.html", "Template de base"),
        ("templates/index.html", "Page d'accueil"),
        ("templates/admin/dashboard.html", "Dashboard admin"),
        ("templates/admin/logo.html", "Gestion du logo")
    ]
    
    for template_path, description in essential_templates:
        if check_file_exists(template_path, description):
            checks_passed += 1
        total_checks += 1
    
    # 6. Vérification des fichiers statiques
    print("\n🎨 FICHIERS STATIQUES:")
    static_files = [
        ("static/css/style.css", "Feuille de style principale"),
        ("static/js/main.js", "Script JavaScript principal"),
        ("static/images/logo/velours-logo.svg", "Logo Velours")
    ]
    
    for static_path, description in static_files:
        if check_file_exists(static_path, description):
            checks_passed += 1
        total_checks += 1
    
    # 7. Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 50)
    
    percentage = (checks_passed / total_checks) * 100
    print(f"✅ Vérifications réussies: {checks_passed}/{total_checks} ({percentage:.1f}%)")
    
    if percentage >= 90:
        print("🎉 EXCELLENT! Votre projet est prêt pour Railway!")
        print("🚀 Vous pouvez lancer: python deploy_to_railway.py")
        return True
    elif percentage >= 75:
        print("👍 BON! Quelques ajustements mineurs recommandés")
        print("🔧 Corrigez les éléments manquants puis déployez")
        return True
    elif percentage >= 50:
        print("⚠️ ATTENTION! Plusieurs éléments manquent")
        print("🔧 Corrigez les problèmes avant de déployer")
        return False
    else:
        print("❌ CRITIQUE! Trop d'éléments manquent")
        print("🔧 Exécutez d'abord: python railway_deploy.py")
        return False

def show_next_steps():
    """Afficher les prochaines étapes"""
    print("\n🚀 PROCHAINES ÉTAPES:")
    print("=" * 30)
    
    steps = [
        "1. Corrigez les éléments manquants si nécessaire",
        "2. Créez un compte sur railway.app",
        "3. Installez Railway CLI: npm install -g @railway/cli",
        "4. Lancez le déploiement: python deploy_to_railway.py",
        "5. Ou déployez manuellement selon README_RAILWAY.md"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🌸 Votre boutique Velours sera bientôt en ligne!")

def main():
    """Fonction principale"""
    print("🌸 VÉRIFICATION RAILWAY - VELOURS PARFUMS")
    print("=" * 45)
    
    if not os.path.exists('app.py'):
        print("❌ Erreur: Fichier app.py non trouvé!")
        print("   Assurez-vous d'être dans le bon dossier")
        return
    
    ready = check_railway_readiness()
    show_next_steps()
    
    if ready:
        print("\n🎯 STATUT: PRÊT POUR LE DÉPLOIEMENT!")
    else:
        print("\n⚠️ STATUT: PRÉPARATION NÉCESSAIRE")

if __name__ == '__main__':
    main()
