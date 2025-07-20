"""
Configuration et déploiement Railway pour la boutique Velours
"""
import os
import json

def setup_railway_deployment():
    """Configuration complète pour le déploiement Railway"""
    print("🚂 CONFIGURATION RAILWAY POUR VELOURS")
    print("=" * 50)
    
    # 1. Créer requirements.txt
    create_requirements()
    
    # 2. Créer Procfile
    create_procfile()
    
    # 3. Créer railway.json
    create_railway_config()
    
    # 4. Créer .env.example
    create_env_example()
    
    # 5. Créer gunicorn_config.py
    create_gunicorn_config()
    
    # 6. Modifier app.py pour la production
    modify_app_for_production()
    
    # 7. Instructions de déploiement
    show_deployment_instructions()

def create_requirements():
    """Créer le fichier requirements.txt"""
    print("\n📦 Création de requirements.txt...")
    
    requirements = """Flask==2.3.3
Flask-Login==0.6.3
Flask-SQLAlchemy==3.0.5
Werkzeug==2.3.7
python-dotenv==1.0.0
Pillow==10.0.1
gunicorn==21.2.0
requests==2.31.0
psycopg2-binary==2.9.7
"""
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print("✅ requirements.txt créé")

def create_procfile():
    """Créer le Procfile pour Railway"""
    print("\n🔧 Création du Procfile...")
    
    procfile_content = """web: gunicorn --config gunicorn_config.py app:app
"""
    
    with open('Procfile', 'w', encoding='utf-8') as f:
        f.write(procfile_content)
    
    print("✅ Procfile créé")

def create_railway_config():
    """Créer railway.json pour la configuration"""
    print("\n🚂 Création de railway.json...")
    
    railway_config = {
        "$schema": "https://railway.app/railway.schema.json",
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "gunicorn --config gunicorn_config.py app:app",
            "healthcheckPath": "/",
            "healthcheckTimeout": 100,
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open('railway.json', 'w', encoding='utf-8') as f:
        json.dump(railway_config, f, indent=2)
    
    print("✅ railway.json créé")

def create_env_example():
    """Créer .env.example"""
    print("\n🔐 Création de .env.example...")
    
    env_example = """# Configuration de base
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here

# Base de données (Railway PostgreSQL)
DATABASE_URL=postgresql://username:password@host:port/database

# Telegram Bot (optionnel)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id

# WhatsApp (optionnel)
WHATSAPP_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_ID=your-whatsapp-phone-id

# Configuration serveur
PORT=8000
HOST=0.0.0.0
"""
    
    with open('.env.example', 'w', encoding='utf-8') as f:
        f.write(env_example)
    
    print("✅ .env.example créé")

def create_gunicorn_config():
    """Créer la configuration Gunicorn"""
    print("\n⚙️ Création de gunicorn_config.py...")
    
    gunicorn_config = """import os

# Configuration Gunicorn pour Railway
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
workers = int(os.environ.get('WEB_CONCURRENCY', 2))
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "velours-parfums"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL (Railway gère le SSL)
keyfile = None
certfile = None
"""
    
    with open('gunicorn_config.py', 'w', encoding='utf-8') as f:
        f.write(gunicorn_config)
    
    print("✅ gunicorn_config.py créé")

def modify_app_for_production():
    """Modifier app.py pour la production"""
    print("\n🔧 Modification d'app.py pour la production...")
    
    # Lire le fichier app.py actuel
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ajouter la configuration de production au début
        production_config = '''import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

'''
        
        # Vérifier si la configuration n'est pas déjà présente
        if 'load_dotenv()' not in content:
            # Trouver la première ligne d'import et insérer après
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith('from flask import'):
                    insert_index = i
                    break
            
            # Insérer la configuration de production
            lines.insert(insert_index, production_config)
            content = '\n'.join(lines)
        
        # Modifier la configuration de la base de données
        if "app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bijoux_store.db'" in content:
            content = content.replace(
                "app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bijoux_store.db'",
                """# Configuration base de données
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///bijoux_store.db'"""
            )
        
        # Modifier la clé secrète
        if "app.secret_key = 'your-secret-key-here'" in content:
            content = content.replace(
                "app.secret_key = 'your-secret-key-here'",
                "app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')"
            )
        
        # Modifier la section de démarrage
        if "if __name__ == '__main__':" in content:
            content = content.replace(
                "app.run(debug=True, port=5001)",
                """port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)"""
            )
        
        # Sauvegarder les modifications
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ app.py modifié pour la production")
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la modification d'app.py: {e}")

def show_deployment_instructions():
    """Afficher les instructions de déploiement"""
    print("\n" + "=" * 60)
    print("🚂 INSTRUCTIONS DE DÉPLOIEMENT RAILWAY")
    print("=" * 60)
    
    instructions = """
🌸 DÉPLOIEMENT DE VELOURS SUR RAILWAY

📋 ÉTAPES DE DÉPLOIEMENT:

1️⃣ PRÉPARATION:
   • Créez un compte sur railway.app
   • Installez Railway CLI: npm install -g @railway/cli
   • Connectez votre compte: railway login

2️⃣ INITIALISATION DU PROJET:
   • Dans votre dossier: railway init
   • Sélectionnez "Empty Project"
   • Nommez votre projet: "velours-parfums"

3️⃣ AJOUT DE LA BASE DE DONNÉES:
   • railway add postgresql
   • La variable DATABASE_URL sera automatiquement configurée

4️⃣ CONFIGURATION DES VARIABLES:
   • railway variables set SECRET_KEY="votre-clé-secrète-super-longue"
   • railway variables set FLASK_ENV="production"
   
   Optionnel (Telegram):
   • railway variables set TELEGRAM_BOT_TOKEN="votre-token"
   • railway variables set TELEGRAM_CHAT_ID="votre-chat-id"

5️⃣ DÉPLOIEMENT:
   • git add .
   • git commit -m "Deploy Velours parfums to Railway"
   • railway up

6️⃣ DOMAINE PERSONNALISÉ (optionnel):
   • railway domain
   • Ou configurez un domaine personnalisé dans le dashboard

🌐 ACCÈS À VOTRE BOUTIQUE:
   • URL Railway: https://votre-projet.railway.app
   • Admin: /admin (admin@parfum.com / admin123)

📊 MONITORING:
   • Dashboard Railway: railway open
   • Logs: railway logs
   • Variables: railway variables

🔧 COMMANDES UTILES:
   • railway status    - Statut du déploiement
   • railway logs      - Voir les logs
   • railway shell     - Accès shell au conteneur
   • railway restart   - Redémarrer l'application

💡 CONSEILS:
   • Changez le mot de passe admin après le premier déploiement
   • Configurez un domaine personnalisé pour plus de professionnalisme
   • Activez les sauvegardes automatiques de la base de données
   • Surveillez les métriques dans le dashboard Railway

🌸 Votre boutique Velours sera accessible 24/7 dans le monde entier!
"""
    
    print(instructions)
    
    print("\n📁 FICHIERS CRÉÉS POUR RAILWAY:")
    files = [
        "requirements.txt - Dépendances Python",
        "Procfile - Commande de démarrage",
        "railway.json - Configuration Railway",
        "gunicorn_config.py - Configuration serveur",
        ".env.example - Variables d'environnement",
        "app.py - Modifié pour la production"
    ]
    
    for file in files:
        print(f"   ✅ {file}")
    
    print(f"\n🚀 PRÊT POUR LE DÉPLOIEMENT!")
    print("🌐 Votre boutique Velours sera bientôt en ligne!")

def main():
    """Configuration complète Railway"""
    setup_railway_deployment()

if __name__ == '__main__':
    main()
