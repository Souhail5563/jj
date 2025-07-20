"""
Script pour démarrer le serveur Flask
"""
from app import app

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Flask...")
    print("🌐 Serveur disponible sur: http://127.0.0.1:5001")
    app.run(host='127.0.0.1', port=5001, debug=True)
