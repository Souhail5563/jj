# 🌸 Velours - Boutique de Parfums de Luxe

## 🚂 Déploiement sur Railway

Votre boutique de parfums Velours avec thème noir mat et or, prête pour le déploiement sur Railway.

### ✨ Fonctionnalités

- 🌸 **Boutique de parfums** avec design élégant noir mat et or
- 🛍️ **Système de commandes** complet avec panier
- 👨‍💼 **Interface d'administration** complète
- 📱 **Notifications Telegram** pour les nouvelles commandes
- 🎨 **Gestion du logo** Velours personnalisable
- 📊 **Dashboard administrateur** avec statistiques
- 🔐 **Système d'authentification** sécurisé
- 📱 **Design responsive** pour tous les appareils

### 🚀 Déploiement Automatique

#### Option 1: Script Automatique (Recommandé)
```bash
python deploy_to_railway.py
```

#### Option 2: Déploiement Manuel

1. **Préparation**
   ```bash
   # Installer Railway CLI
   npm install -g @railway/cli
   
   # Se connecter
   railway login
   ```

2. **Initialisation**
   ```bash
   # Créer le projet
   railway init velours-parfums
   
   # Ajouter PostgreSQL
   railway add postgresql
   ```

3. **Variables d'environnement**
   ```bash
   # Variables obligatoires
   railway variables set SECRET_KEY="votre-clé-secrète-très-longue"
   railway variables set FLASK_ENV="production"
   
   # Variables optionnelles (Telegram)
   railway variables set TELEGRAM_BOT_TOKEN="votre-token"
   railway variables set TELEGRAM_CHAT_ID="votre-chat-id"
   ```

4. **Déploiement**
   ```bash
   git add .
   git commit -m "Deploy Velours to Railway"
   railway up
   ```

### 🌐 Accès à votre boutique

- **URL**: `https://votre-projet.railway.app`
- **Admin**: `/admin`
- **Identifiants par défaut**: 
  - Email: `admin@parfum.com`
  - Mot de passe: `admin123`

⚠️ **Important**: Changez ces identifiants après le premier déploiement!

### 📊 Gestion et Monitoring

```bash
# Voir les logs
railway logs

# Ouvrir le dashboard
railway open

# Redémarrer l'application
railway restart

# Voir les variables
railway variables

# Statut du déploiement
railway status
```

### 🔧 Configuration Post-Déploiement

1. **Sécurité**
   - Changez le mot de passe administrateur
   - Configurez une clé secrète forte
   - Activez HTTPS (automatique sur Railway)

2. **Personnalisation**
   - Uploadez votre logo Velours via `/admin/logo`
   - Ajoutez vos produits de parfums
   - Configurez les paramètres du footer
   - Personnalisez les sliders

3. **Notifications**
   - Configurez votre bot Telegram
   - Testez les notifications de commandes
   - Configurez WhatsApp (optionnel)

### 📁 Structure du Projet

```
velours-parfums/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── Procfile              # Configuration Railway
├── railway.json          # Configuration avancée
├── gunicorn_config.py    # Configuration serveur
├── templates/            # Templates HTML
├── static/               # Fichiers statiques (CSS, JS, images)
├── models.py            # Modèles de base de données
└── deploy_to_railway.py # Script de déploiement
```

### 🎨 Thème et Design

- **Couleurs**: Noir mat (#0a0a0a) et Or (#FFD700)
- **Typographie**: Playfair Display pour l'élégance
- **Animations**: Effets de lueur dorée
- **Responsive**: Adaptatif mobile et desktop

### 🛍️ Fonctionnalités E-commerce

- Catalogue de produits avec filtres
- Panier d'achat persistant
- Système de commandes complet
- Gestion des stocks
- Interface d'administration
- Notifications automatiques

### 📱 Intégrations

- **Telegram**: Notifications de commandes
- **WhatsApp**: Support client (optionnel)
- **PostgreSQL**: Base de données robuste
- **Gunicorn**: Serveur de production

### 🔐 Sécurité

- Authentification sécurisée
- Protection CSRF
- Hashage des mots de passe
- Variables d'environnement sécurisées
- HTTPS automatique sur Railway

### 💡 Conseils de Production

1. **Performance**
   - Utilisez un CDN pour les images
   - Optimisez les images de produits
   - Activez la compression gzip

2. **SEO**
   - Configurez les meta descriptions
   - Ajoutez un sitemap
   - Optimisez les URLs

3. **Analytics**
   - Intégrez Google Analytics
   - Surveillez les conversions
   - Analysez le comportement utilisateur

### 🆘 Dépannage

#### Erreurs communes

1. **Erreur de base de données**
   ```bash
   railway logs
   # Vérifiez la variable DATABASE_URL
   ```

2. **Erreur de démarrage**
   ```bash
   railway restart
   # Vérifiez les logs pour plus de détails
   ```

3. **Variables manquantes**
   ```bash
   railway variables
   # Ajoutez les variables manquantes
   ```

### 📞 Support

- **Logs**: `railway logs` pour diagnostiquer
- **Dashboard**: `railway open` pour le monitoring
- **Documentation**: [Railway Docs](https://docs.railway.app)

### 🌸 À Propos de Velours

Velours est une boutique de parfums de luxe avec un design élégant noir mat et or. 
Créée pour offrir une expérience d'achat premium avec une interface moderne et intuitive.

**Fonctionnalités principales:**
- Catalogue de parfums avec descriptions détaillées
- Système de commandes sécurisé
- Interface d'administration complète
- Notifications en temps réel
- Design responsive et élégant

---

🚂 **Déployé avec Railway** | 🌸 **Velours Parfums** | ✨ **Thème Noir Mat & Or**
