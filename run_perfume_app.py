"""
Script pour lancer l'application Flask de parfums
"""
from app import app

if __name__ == '__main__':
    print("🌸 Démarrage de l'application Parfum Store...")
    print("🔗 URL: http://127.0.0.1:5001")
    print("👤 Admin: admin@bijoux.com / admin123")
    print("📱 Test WhatsApp: test@parfum.com / admin123")
    app.run(debug=True, port=5001)
