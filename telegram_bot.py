"""
Module pour gérer les notifications Telegram
"""
import requests
import json
from datetime import datetime
import logging

# Configuration du bot Telegram
TELEGRAM_BOT_TOKEN = "7584443487:AAGfjko-ecgh-XxFD72AjSWDvlyjPOuGUDY"
TELEGRAM_CHAT_ID = "7763623565"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_telegram_message(message, parse_mode='HTML'):
    """
    Envoie un message via Telegram
    """
    try:
        url = f"{TELEGRAM_API_URL}/sendMessage"
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': parse_mode
        }
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            logger.info("Message Telegram envoyé avec succès")
            return True
        else:
            logger.error(f"Erreur envoi Telegram: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur réseau Telegram: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Erreur inattendue Telegram: {str(e)}")
        return False

def format_order_message(order):
    """
    Formate un message de commande pour Telegram
    """
    try:
        # Émojis pour les statuts
        status_emojis = {
            'pending': '⏳',
            'confirmed': '✅',
            'shipped': '🚚',
            'delivered': '📦',
            'cancelled': '❌'
        }
        
        status_names = {
            'pending': 'En attente',
            'confirmed': 'Confirmée',
            'shipped': 'Expédiée',
            'delivered': 'Livrée',
            'cancelled': 'Annulée'
        }
        
        # En-tête du message
        message = f"🛍️ <b>NOUVELLE COMMANDE - Bijoux Store</b>\n\n"
        
        # Informations de base
        message += f"📋 <b>Commande #{order.id}</b>\n"
        message += f"📅 <b>Date:</b> {order.created_at.strftime('%d/%m/%Y à %H:%M')}\n"
        message += f"{status_emojis.get(order.status, '❓')} <b>Statut:</b> {status_names.get(order.status, order.status)}\n\n"
        
        # Informations client
        message += f"👤 <b>CLIENT</b>\n"
        message += f"• <b>Nom:</b> {order.user.first_name} {order.user.last_name}\n"
        message += f"• <b>Email:</b> {order.user.email}\n"
        if order.user.phone:
            message += f"• <b>Téléphone:</b> {order.user.phone}\n"
        message += "\n"
        
        # Articles commandés
        message += f"🛒 <b>ARTICLES ({len(order.items)})</b>\n"
        for item in order.items:
            message += f"• {item.product.name}\n"
            message += f"  └ Quantité: {item.quantity} × {item.price:.2f}€ = <b>{(item.quantity * item.price):.2f}€</b>\n"
        message += "\n"
        
        # Total
        message += f"💰 <b>TOTAL: {order.total_amount:.2f}€</b>\n\n"
        
        # Adresse de livraison
        if order.shipping_address:
            message += f"📍 <b>LIVRAISON</b>\n"
            message += f"{order.shipping_address}\n\n"
        
        # Actions rapides
        message += f"🔗 <b>ACTIONS</b>\n"
        message += f"• Voir détails: /order_{order.id}\n"
        message += f"• Dashboard: http://127.0.0.1:5001/admin/orders\n"
        
        return message
        
    except Exception as e:
        logger.error(f"Erreur formatage message: {str(e)}")
        return f"🛍️ Nouvelle commande #{order.id} reçue - Erreur de formatage"

def send_order_notification(order):
    """
    Envoie une notification de nouvelle commande
    """
    try:
        message = format_order_message(order)
        return send_telegram_message(message)
    except Exception as e:
        logger.error(f"Erreur notification commande: {str(e)}")
        return False

def send_order_status_update(order, old_status, new_status):
    """
    Envoie une notification de changement de statut
    """
    try:
        status_emojis = {
            'pending': '⏳',
            'confirmed': '✅',
            'shipped': '🚚',
            'delivered': '📦',
            'cancelled': '❌'
        }
        
        status_names = {
            'pending': 'En attente',
            'confirmed': 'Confirmée',
            'shipped': 'Expédiée',
            'delivered': 'Livrée',
            'cancelled': 'Annulée'
        }
        
        message = f"🔄 <b>MISE À JOUR COMMANDE</b>\n\n"
        message += f"📋 <b>Commande #{order.id}</b>\n"
        message += f"👤 <b>Client:</b> {order.user.first_name} {order.user.last_name}\n"
        message += f"💰 <b>Montant:</b> {order.total_amount:.2f}€\n\n"
        
        message += f"📊 <b>CHANGEMENT DE STATUT</b>\n"
        message += f"• <b>Ancien:</b> {status_emojis.get(old_status, '❓')} {status_names.get(old_status, old_status)}\n"
        message += f"• <b>Nouveau:</b> {status_emojis.get(new_status, '❓')} {status_names.get(new_status, new_status)}\n\n"
        
        message += f"🕒 <b>Mis à jour:</b> {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n"
        
        return send_telegram_message(message)
        
    except Exception as e:
        logger.error(f"Erreur notification statut: {str(e)}")
        return False

def send_daily_summary():
    """
    Envoie un résumé quotidien des commandes
    """
    try:
        from models import Order
        from datetime import date
        
        today = date.today()
        orders_today = Order.query.filter(
            Order.created_at >= today
        ).all()
        
        if not orders_today:
            message = f"📊 <b>RÉSUMÉ QUOTIDIEN</b>\n\n"
            message += f"📅 {today.strftime('%d/%m/%Y')}\n"
            message += f"🛍️ Aucune nouvelle commande aujourd'hui"
            return send_telegram_message(message)
        
        total_amount = sum(order.total_amount for order in orders_today)
        
        message = f"📊 <b>RÉSUMÉ QUOTIDIEN</b>\n\n"
        message += f"📅 {today.strftime('%d/%m/%Y')}\n"
        message += f"🛍️ <b>{len(orders_today)} nouvelle(s) commande(s)</b>\n"
        message += f"💰 <b>Chiffre d'affaires: {total_amount:.2f}€</b>\n\n"
        
        # Répartition par statut
        status_count = {}
        for order in orders_today:
            status_count[order.status] = status_count.get(order.status, 0) + 1
        
        if status_count:
            message += f"📈 <b>RÉPARTITION</b>\n"
            status_emojis = {
                'pending': '⏳',
                'confirmed': '✅',
                'shipped': '🚚',
                'delivered': '📦',
                'cancelled': '❌'
            }
            
            for status, count in status_count.items():
                emoji = status_emojis.get(status, '❓')
                message += f"• {emoji} {status}: {count}\n"
        
        return send_telegram_message(message)
        
    except Exception as e:
        logger.error(f"Erreur résumé quotidien: {str(e)}")
        return False

def test_telegram_connection():
    """
    Test la connexion au bot Telegram
    """
    try:
        message = f"🤖 <b>TEST CONNEXION</b>\n\n"
        message += f"✅ Bot Telegram connecté avec succès!\n"
        message += f"🕒 {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n"
        message += f"🛍️ Bijoux Store - Notifications activées"
        
        return send_telegram_message(message)
        
    except Exception as e:
        logger.error(f"Erreur test connexion: {str(e)}")
        return False

if __name__ == "__main__":
    # Test de la connexion
    print("Test de connexion au bot Telegram...")
    if test_telegram_connection():
        print("✅ Connexion réussie!")
    else:
        print("❌ Échec de la connexion")
