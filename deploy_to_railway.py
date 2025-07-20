"""
Script de déploiement automatique sur Railway pour Velours
"""
import os
import subprocess
import sys
import json
import secrets

def run_command(command, description=""):
    """Exécuter une commande et afficher le résultat"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            if result.stdout.strip():
                print(f"   📄 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Erreur")
            if result.stderr.strip():
                print(f"   ⚠️ {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        return False

def check_railway_cli():
    """Vérifier si Railway CLI est installé"""
    print("🔍 Vérification de Railway CLI...")
    result = subprocess.run("railway --version", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Railway CLI installé: {result.stdout.strip()}")
        return True
    else:
        print("❌ Railway CLI non installé")
        print("📦 Installation de Railway CLI...")
        if run_command("npm install -g @railway/cli", "Installation Railway CLI"):
            return True
        else:
            print("⚠️ Veuillez installer Railway CLI manuellement:")
            print("   npm install -g @railway/cli")
            return False

def check_git():
    """Vérifier si Git est configuré"""
    print("🔍 Vérification de Git...")
    result = subprocess.run("git status", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Repository Git détecté")
        return True
    else:
        print("📦 Initialisation du repository Git...")
        commands = [
            ("git init", "Initialisation Git"),
            ("git add .", "Ajout des fichiers"),
            ("git commit -m 'Initial commit - Velours parfums'", "Premier commit")
        ]
        
        for cmd, desc in commands:
            if not run_command(cmd, desc):
                return False
        return True

def generate_secret_key():
    """Générer une clé secrète sécurisée"""
    return secrets.token_urlsafe(32)

def deploy_to_railway():
    """Déploiement automatique sur Railway"""
    print("🚂 DÉPLOIEMENT AUTOMATIQUE SUR RAILWAY")
    print("=" * 55)
    
    # 1. Vérifications préliminaires
    if not check_railway_cli():
        return False
    
    if not check_git():
        return False
    
    # 2. Connexion à Railway
    print("\n🔐 Connexion à Railway...")
    print("   📝 Veuillez vous connecter dans le navigateur qui va s'ouvrir")
    if not run_command("railway login", "Connexion Railway"):
        print("⚠️ Veuillez vous connecter manuellement: railway login")
        input("Appuyez sur Entrée après vous être connecté...")
    
    # 3. Initialisation du projet
    print("\n🚀 Initialisation du projet Railway...")
    project_name = input("📝 Nom du projet (défaut: velours-parfums): ").strip()
    if not project_name:
        project_name = "velours-parfums"
    
    # Créer un nouveau projet
    if not run_command(f"railway init {project_name}", f"Création du projet {project_name}"):
        print("⚠️ Si le projet existe déjà, continuons...")
    
    # 4. Ajout de PostgreSQL
    print("\n🗄️ Ajout de la base de données PostgreSQL...")
    run_command("railway add postgresql", "Ajout PostgreSQL")
    
    # 5. Configuration des variables d'environnement
    print("\n🔧 Configuration des variables d'environnement...")
    
    secret_key = generate_secret_key()
    variables = [
        ("SECRET_KEY", secret_key),
        ("FLASK_ENV", "production"),
        ("PORT", "8000")
    ]
    
    for var_name, var_value in variables:
        run_command(f'railway variables set {var_name}="{var_value}"', f"Configuration {var_name}")
    
    # Variables optionnelles
    print("\n📱 Configuration Telegram (optionnel):")
    telegram_token = input("🤖 Token Telegram Bot (Entrée pour ignorer): ").strip()
    if telegram_token:
        run_command(f'railway variables set TELEGRAM_BOT_TOKEN="{telegram_token}"', "Token Telegram")
        
        telegram_chat = input("💬 Chat ID Telegram (Entrée pour ignorer): ").strip()
        if telegram_chat:
            run_command(f'railway variables set TELEGRAM_CHAT_ID="{telegram_chat}"', "Chat ID Telegram")
    
    # 6. Déploiement
    print("\n🚀 Déploiement de l'application...")
    
    # Commit des derniers changements
    run_command("git add .", "Ajout des fichiers modifiés")
    run_command("git commit -m 'Deploy Velours parfums to Railway'", "Commit de déploiement")
    
    # Déploiement
    if run_command("railway up", "Déploiement sur Railway"):
        print("\n🎉 DÉPLOIEMENT RÉUSSI!")
        
        # 7. Informations post-déploiement
        print("\n📊 Informations de déploiement:")
        run_command("railway status", "Statut du déploiement")
        
        # Obtenir l'URL
        print("\n🌐 Obtention de l'URL...")
        result = subprocess.run("railway domain", shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            url = result.stdout.strip()
            print(f"✅ URL de votre boutique: {url}")
        else:
            print("🔧 Génération d'un domaine...")
            run_command("railway domain", "Génération du domaine")
        
        # Instructions finales
        show_post_deployment_info()
        
        return True
    else:
        print("❌ Échec du déploiement")
        return False

def show_post_deployment_info():
    """Afficher les informations post-déploiement"""
    print("\n" + "=" * 60)
    print("🎉 DÉPLOIEMENT TERMINÉ - VELOURS EN LIGNE!")
    print("=" * 60)
    
    info = """
🌸 VOTRE BOUTIQUE VELOURS EST MAINTENANT EN LIGNE!

🌐 ACCÈS:
   • URL: Voir ci-dessus ou tapez 'railway domain'
   • Admin: /admin
   • Identifiants: admin@parfum.com / admin123

🔧 COMMANDES UTILES:
   • railway logs        - Voir les logs en temps réel
   • railway open        - Ouvrir le dashboard Railway
   • railway restart     - Redémarrer l'application
   • railway variables   - Voir les variables d'environnement

📊 MONITORING:
   • Dashboard Railway pour les métriques
   • Logs automatiques des erreurs
   • Surveillance de la performance

🔐 SÉCURITÉ:
   ⚠️ IMPORTANT: Changez le mot de passe admin après le premier accès!
   • Connectez-vous à /admin
   • Changez admin@parfum.com / admin123
   • Configurez vos paramètres Telegram si nécessaire

🌸 FÉLICITATIONS!
Votre boutique de parfums Velours est maintenant accessible
dans le monde entier, 24h/24 et 7j/7!

💡 Prochaines étapes:
   1. Testez votre boutique en ligne
   2. Ajoutez vos vrais produits
   3. Configurez votre logo Velours
   4. Personnalisez les paramètres
   5. Partagez votre boutique!
"""
    
    print(info)

def main():
    """Fonction principale"""
    print("🌸 DÉPLOIEMENT VELOURS SUR RAILWAY")
    print("=" * 40)
    
    # Vérifier si nous sommes dans le bon dossier
    if not os.path.exists('app.py'):
        print("❌ Fichier app.py non trouvé!")
        print("   Assurez-vous d'être dans le dossier de votre projet")
        return
    
    if not os.path.exists('requirements.txt'):
        print("❌ Fichier requirements.txt non trouvé!")
        print("   Exécutez d'abord: python railway_deploy.py")
        return
    
    print("✅ Fichiers de projet détectés")
    
    # Demander confirmation
    print("\n🚀 Prêt à déployer Velours sur Railway?")
    print("   • Votre boutique sera accessible publiquement")
    print("   • Une base de données PostgreSQL sera créée")
    print("   • Les variables d'environnement seront configurées")
    
    confirm = input("\n📝 Continuer? (o/N): ").strip().lower()
    if confirm not in ['o', 'oui', 'y', 'yes']:
        print("❌ Déploiement annulé")
        return
    
    # Lancer le déploiement
    if deploy_to_railway():
        print("\n🎉 Déploiement terminé avec succès!")
    else:
        print("\n❌ Échec du déploiement")
        print("💡 Consultez les messages d'erreur ci-dessus")
        print("🔧 Vous pouvez réessayer ou déployer manuellement")

if __name__ == '__main__':
    main()
