"""
Alternatives de déploiement gratuites pour Velours
"""
import os

def setup_render_deployment():
    """Configuration pour Render (Gratuit)"""
    print("🎨 CONFIGURATION RENDER (GRATUIT)")
    print("=" * 40)
    
    # Créer render.yaml
    render_config = """services:
  - type: web
    name: velours-parfums
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --config gunicorn_config.py app:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: velours-db
          property: connectionString
    
databases:
  - name: velours-db
    databaseName: velours
    user: velours_user
"""
    
    with open('render.yaml', 'w', encoding='utf-8') as f:
        f.write(render_config)
    
    print("✅ render.yaml créé")
    
    # Instructions Render
    render_instructions = """
🎨 DÉPLOIEMENT SUR RENDER (100% GRATUIT)

📋 ÉTAPES:
1. Créez un compte sur render.com
2. Connectez votre repository GitHub
3. Créez un nouveau "Web Service"
4. Sélectionnez votre repository
5. Render détectera automatiquement Python
6. Configurez:
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn --config gunicorn_config.py app:app
7. Ajoutez les variables d'environnement:
   - SECRET_KEY (généré automatiquement)
   - FLASK_ENV=production
8. Créez une base de données PostgreSQL gratuite
9. Connectez la base de données à votre service

🌐 URL: https://velours-parfums.onrender.com
💰 Coût: 100% GRATUIT
⏱️ Temps: 5-10 minutes
"""
    
    print(render_instructions)

def setup_vercel_deployment():
    """Configuration pour Vercel"""
    print("\n⚡ CONFIGURATION VERCEL")
    print("=" * 30)
    
    # Créer vercel.json
    vercel_config = """{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}"""
    
    with open('vercel.json', 'w', encoding='utf-8') as f:
        f.write(vercel_config)
    
    print("✅ vercel.json créé")
    
    # Créer api/index.py pour Vercel
    os.makedirs('api', exist_ok=True)
    
    vercel_app = """from app import app

if __name__ == "__main__":
    app.run()
"""
    
    with open('api/index.py', 'w', encoding='utf-8') as f:
        f.write(vercel_app)
    
    print("✅ api/index.py créé")
    
    vercel_instructions = """
⚡ DÉPLOIEMENT SUR VERCEL (GRATUIT)

📋 ÉTAPES:
1. Créez un compte sur vercel.com
2. Installez Vercel CLI: npm i -g vercel
3. Connectez votre projet: vercel login
4. Déployez: vercel --prod
5. Configurez les variables d'environnement sur vercel.com

🌐 URL: https://velours-parfums.vercel.app
💰 Coût: GRATUIT
⚡ Déploiement: Instantané
"""
    
    print(vercel_instructions)

def setup_heroku_deployment():
    """Configuration pour Heroku"""
    print("\n🟣 CONFIGURATION HEROKU")
    print("=" * 30)
    
    # Créer runtime.txt
    with open('runtime.txt', 'w', encoding='utf-8') as f:
        f.write('python-3.9.18')
    
    print("✅ runtime.txt créé")
    
    heroku_instructions = """
🟣 DÉPLOIEMENT SUR HEROKU (GRATUIT LIMITÉ)

📋 ÉTAPES:
1. Créez un compte sur heroku.com
2. Installez Heroku CLI
3. Connectez-vous: heroku login
4. Créez l'app: heroku create velours-parfums
5. Ajoutez PostgreSQL: heroku addons:create heroku-postgresql:mini
6. Configurez les variables:
   heroku config:set SECRET_KEY="votre-clé"
   heroku config:set FLASK_ENV="production"
7. Déployez: git push heroku main

🌐 URL: https://velours-parfums.herokuapp.com
💰 Coût: GRATUIT (avec limitations)
⚠️ Note: Heroku a supprimé son plan gratuit, mais offre des crédits
"""
    
    print(heroku_instructions)

def setup_pythonanywhere_deployment():
    """Configuration pour PythonAnywhere"""
    print("\n🐍 CONFIGURATION PYTHONANYWHERE")
    print("=" * 40)
    
    pythonanywhere_instructions = """
🐍 DÉPLOIEMENT SUR PYTHONANYWHERE (GRATUIT)

📋 ÉTAPES:
1. Créez un compte sur pythonanywhere.com
2. Uploadez vos fichiers via l'interface web
3. Créez une nouvelle Web App Flask
4. Configurez le fichier WSGI:
   
   import sys
   import os
   
   path = '/home/yourusername/velours'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application

5. Installez les dépendances dans la console:
   pip3.10 install --user -r requirements.txt

6. Configurez les variables d'environnement
7. Redémarrez l'application

🌐 URL: https://yourusername.pythonanywhere.com
💰 Coût: 100% GRATUIT
📊 Limite: 1 app web gratuite
"""
    
    print(pythonanywhere_instructions)

def setup_github_pages_static():
    """Configuration pour GitHub Pages (version statique)"""
    print("\n📚 GITHUB PAGES (VERSION STATIQUE)")
    print("=" * 40)
    
    github_instructions = """
📚 GITHUB PAGES + NETLIFY (GRATUIT)

Pour une version statique de démonstration:

📋 ÉTAPES:
1. Créez un repository GitHub
2. Uploadez vos fichiers
3. Activez GitHub Pages
4. Ou utilisez Netlify pour plus de fonctionnalités

🌐 URL: https://username.github.io/velours-parfums
💰 Coût: 100% GRATUIT
⚠️ Note: Statique uniquement (pas de base de données)
"""
    
    print(github_instructions)

def show_recommendations():
    """Afficher les recommandations"""
    print("\n" + "=" * 60)
    print("🌟 RECOMMANDATIONS POUR VELOURS")
    print("=" * 60)
    
    recommendations = """
🥇 MEILLEURE OPTION: RENDER
   ✅ 100% gratuit avec base de données
   ✅ Déploiement automatique depuis GitHub
   ✅ HTTPS automatique
   ✅ Domaine personnalisé possible
   ✅ Parfait pour Flask + PostgreSQL

🥈 ALTERNATIVE: PYTHONANYWHERE
   ✅ 100% gratuit
   ✅ Interface simple
   ✅ Support Flask natif
   ⚠️ Base de données MySQL (modification nécessaire)

🥉 OPTION RAPIDE: VERCEL
   ✅ Déploiement ultra-rapide
   ✅ Intégration Git excellente
   ⚠️ Serverless (modifications nécessaires)

💡 CONSEIL:
Je recommande RENDER car il offre:
- PostgreSQL gratuit
- Déploiement continu
- Configuration similaire à Railway
- Aucune modification de code nécessaire
"""
    
    print(recommendations)

def create_deployment_guide():
    """Créer un guide de déploiement complet"""
    guide_content = """# 🌸 Guide de Déploiement Velours - Alternatives Gratuites

## 🎨 Option 1: Render (Recommandée)

### Avantages
- ✅ 100% gratuit avec PostgreSQL
- ✅ Déploiement automatique
- ✅ HTTPS inclus
- ✅ Aucune modification de code

### Étapes
1. Créez un compte sur [render.com](https://render.com)
2. Connectez votre repository GitHub
3. Créez un "Web Service"
4. Configurez:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn --config gunicorn_config.py app:app`
5. Ajoutez PostgreSQL gratuit
6. Configurez les variables d'environnement

## 🐍 Option 2: PythonAnywhere

### Avantages
- ✅ 100% gratuit
- ✅ Interface simple
- ✅ Support Flask natif

### Étapes
1. Compte sur [pythonanywhere.com](https://pythonanywhere.com)
2. Upload des fichiers
3. Création Web App Flask
4. Configuration WSGI
5. Installation des dépendances

## ⚡ Option 3: Vercel

### Avantages
- ✅ Déploiement instantané
- ✅ Intégration Git parfaite
- ✅ CDN mondial

### Étapes
1. Compte sur [vercel.com](https://vercel.com)
2. Installation CLI: `npm i -g vercel`
3. Déploiement: `vercel --prod`

## 🌟 Recommandation

**RENDER** est la meilleure option car elle offre:
- PostgreSQL gratuit
- Configuration identique à Railway
- Aucune modification de code nécessaire
- Déploiement professionnel

Votre boutique Velours sera accessible à:
`https://velours-parfums.onrender.com`
"""
    
    with open('DEPLOYMENT_ALTERNATIVES.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ Guide de déploiement créé: DEPLOYMENT_ALTERNATIVES.md")

def main():
    """Configuration des alternatives de déploiement"""
    print("🌸 ALTERNATIVES DE DÉPLOIEMENT POUR VELOURS")
    print("=" * 55)
    print("Railway nécessite un plan payant pour les applications web.")
    print("Voici d'excellentes alternatives GRATUITES:")
    
    # Configuration pour chaque plateforme
    setup_render_deployment()
    setup_vercel_deployment()
    setup_heroku_deployment()
    setup_pythonanywhere_deployment()
    setup_github_pages_static()
    
    # Recommandations
    show_recommendations()
    
    # Créer le guide
    create_deployment_guide()
    
    print("\n🎯 PROCHAINE ÉTAPE:")
    print("Choisissez une plateforme et suivez les instructions!")
    print("🌸 Votre boutique Velours sera bientôt en ligne!")

if __name__ == '__main__':
    main()
