"""
Module pour gérer les notifications WhatsApp aux clients
"""
import requests
import json
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration WhatsApp Business API (Twilio)
TWILIO_ACCOUNT_SID = "AC56484b4b53bbbff7ade8fafb03fc688d"
TWILIO_AUTH_TOKEN = "5a0bf65add2887281d1733421d13a3ca"
WHATSAPP_FROM = "whatsapp:+14155238886"  # Numéro Twilio Sandbox

# Template de contenu pour les notifications
TWILIO_CONTENT_SID = "HXb5b62575e6e4ff6129ad7c8efe1f983e"  # Votre template existant

# Alternative: API WhatsApp Business directe
WHATSAPP_API_URL = "https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages"
WHATSAPP_ACCESS_TOKEN = "your_whatsapp_access_token"

def send_whatsapp_message_twilio(to_number, message):
    """
    Envoie un message WhatsApp via Twilio (message simple)
    """
    try:
        from twilio.rest import Client

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=message,
            from_=WHATSAPP_FROM,
            to=f'whatsapp:{to_number}'
        )

        logger.info(f"Message WhatsApp envoyé avec succès via Twilio: {message.sid}")
        return True

    except Exception as e:
        logger.error(f"Erreur envoi WhatsApp Twilio: {str(e)}")
        return False

def send_whatsapp_template_twilio(to_number, content_sid, variables=None):
    """
    Envoie un message WhatsApp via Twilio avec template de contenu
    """
    try:
        from twilio.rest import Client

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message_params = {
            'from_': WHATSAPP_FROM,
            'content_sid': content_sid,
            'to': f'whatsapp:{to_number}'
        }

        if variables:
            message_params['content_variables'] = variables

        message = client.messages.create(**message_params)

        logger.info(f"Template WhatsApp envoyé avec succès via Twilio: {message.sid}")
        return True

    except Exception as e:
        logger.error(f"Erreur envoi template WhatsApp Twilio: {str(e)}")
        return False

def send_whatsapp_message_api(to_number, message):
    """
    Envoie un message WhatsApp via l'API WhatsApp Business
    """
    try:
        headers = {
            'Authorization': f'Bearer {WHATSAPP_ACCESS_TOKEN}',
            'Content-Type': 'application/json',
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            logger.info("Message WhatsApp envoyé avec succès via API")
            return True
        else:
            logger.error(f"Erreur API WhatsApp: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur réseau WhatsApp: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Erreur inattendue WhatsApp: {str(e)}")
        return False

def send_whatsapp_message_demo(to_number, message):
    """
    Version de démonstration qui simule l'envoi WhatsApp
    """
    try:
        logger.info(f"[DEMO] Message WhatsApp simulé vers {to_number}")
        logger.info(f"[DEMO] Contenu: {message}")
        
        # Simuler un délai d'envoi
        import time
        time.sleep(1)
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur simulation WhatsApp: {str(e)}")
        return False

def format_order_status_message(order, old_status, new_status):
    """
    Formate un message de changement de statut pour WhatsApp
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
        
        # Message personnalisé selon le statut
        if new_status == 'confirmed':
            message = f"🎉 *Bonne nouvelle !*\n\n"
            message += f"Votre commande #{order.id} a été confirmée !\n\n"
            message += f"📋 *Détails de votre commande :*\n"
            message += f"• Montant : {order.total_amount:.2f}€\n"
            message += f"• Articles : {len(order.items)} produit(s)\n\n"
            message += f"⏰ Votre commande est en cours de préparation.\n"
            message += f"Vous recevrez une nouvelle notification dès l'expédition.\n\n"
            message += f"Merci de votre confiance ! 🌸\n"
            message += f"*Parfum Store*"
            
        elif new_status == 'shipped':
            message = f"🚚 *Votre commande est en route !*\n\n"
            message += f"Votre commande #{order.id} a été expédiée !\n\n"
            message += f"📋 *Détails :*\n"
            message += f"• Montant : {order.total_amount:.2f}€\n"
            message += f"• Date d'expédition : {datetime.now().strftime('%d/%m/%Y')}\n\n"
            if order.shipping_address:
                message += f"📍 *Adresse de livraison :*\n{order.shipping_address}\n\n"
            message += f"📦 Vous devriez recevoir votre commande sous 2-3 jours ouvrés.\n\n"
            message += f"Merci pour votre achat ! 💎\n"
            message += f"*Bijoux Store*"
            
        elif new_status == 'delivered':
            message = f"🎉 *Livraison effectuée !*\n\n"
            message += f"Votre commande #{order.id} a été livrée avec succès !\n\n"
            message += f"📋 *Récapitulatif :*\n"
            message += f"• Montant : {order.total_amount:.2f}€\n"
            message += f"• Date de livraison : {datetime.now().strftime('%d/%m/%Y')}\n\n"
            message += f"💎 Nous espérons que vos bijoux vous plaisent !\n\n"
            message += f"⭐ N'hésitez pas à nous laisser un avis.\n"
            message += f"🔄 Retour possible sous 30 jours.\n\n"
            message += f"Merci de votre confiance !\n"
            message += f"*Bijoux Store*"
            
        elif new_status == 'cancelled':
            message = f"❌ *Commande annulée*\n\n"
            message += f"Votre commande #{order.id} a été annulée.\n\n"
            message += f"💰 Le remboursement de {order.total_amount:.2f}€ sera effectué sous 3-5 jours ouvrés.\n\n"
            message += f"📞 Pour toute question, contactez-nous :\n"
            message += f"• Email : contact@bijoux-store.com\n"
            message += f"• Téléphone : +33 1 23 45 67 89\n\n"
            message += f"Nous nous excusons pour la gêne occasionnée.\n"
            message += f"*Bijoux Store*"
            
        else:
            # Message générique
            message = f"{status_emojis.get(new_status, '📋')} *Mise à jour de commande*\n\n"
            message += f"Le statut de votre commande #{order.id} a été mis à jour :\n\n"
            message += f"• Ancien statut : {status_names.get(old_status, old_status)}\n"
            message += f"• Nouveau statut : {status_names.get(new_status, new_status)}\n\n"
            message += f"Montant : {order.total_amount:.2f}€\n\n"
            message += f"Merci de votre confiance !\n"
            message += f"*Bijoux Store*"
        
        return message
        
    except Exception as e:
        logger.error(f"Erreur formatage message WhatsApp: {str(e)}")
        return f"Mise à jour de votre commande #{order.id} : {status_names.get(new_status, new_status)}"

def send_order_status_notification(order, old_status, new_status):
    """
    Envoie une notification WhatsApp de changement de statut au client
    """
    try:
        # Vérifier que le client a un numéro de téléphone
        if not order.user.phone:
            logger.warning(f"Pas de numéro de téléphone pour l'utilisateur {order.user.id}")
            return False

        # Nettoyer le numéro de téléphone
        phone_number = clean_phone_number(order.user.phone)
        if not phone_number:
            logger.warning(f"Numéro de téléphone invalide: {order.user.phone}")
            return False

        # Formater le message
        message = format_order_status_message(order, old_status, new_status)

        # Choisir la méthode d'envoi
        # Option 1: Template Twilio (recommandé pour la production)
        try:
            # Variables pour le template (adaptez selon votre template)
            variables = f'{{"1":"#{order.id}","2":"{get_status_name(new_status)}"}}'
            success = send_whatsapp_template_twilio(phone_number, TWILIO_CONTENT_SID, variables)
        except:
            # Fallback: Message simple Twilio
            success = send_whatsapp_message_twilio(phone_number, message)

        # Option 3: Mode démo (pour les tests - décommentez pour utiliser)
        # success = send_whatsapp_message_demo(phone_number, message)

        if success:
            logger.info(f"Notification WhatsApp envoyée pour commande #{order.id}")
        else:
            logger.error(f"Échec notification WhatsApp pour commande #{order.id}")

        return success

    except Exception as e:
        logger.error(f"Erreur notification WhatsApp: {str(e)}")
        return False

def get_status_name(status):
    """
    Retourne le nom français du statut
    """
    status_names = {
        'pending': 'En attente',
        'confirmed': 'Confirmée',
        'shipped': 'Expédiée',
        'delivered': 'Livrée',
        'cancelled': 'Annulée'
    }
    return status_names.get(status, status)

def clean_phone_number(phone):
    """
    Nettoie et formate un numéro de téléphone
    """
    try:
        if not phone:
            return None
        
        # Supprimer tous les caractères non numériques sauf le +
        import re
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Gestion des numéros français et marocains
        if cleaned.startswith('0'):
            # Numéro français commençant par 0
            cleaned = '+33' + cleaned[1:]
        elif cleaned.startswith('6') and len(cleaned) == 9:
            # Numéro marocain mobile (6xxxxxxxx)
            cleaned = '+212' + cleaned
        elif not cleaned.startswith('+'):
            # Par défaut, ajouter +33 pour la France
            cleaned = '+33' + cleaned
        
        # Vérifier que le numéro a une longueur raisonnable
        if len(cleaned) < 10 or len(cleaned) > 15:
            return None
        
        return cleaned
        
    except Exception as e:
        logger.error(f"Erreur nettoyage numéro: {str(e)}")
        return None

def send_welcome_message(user):
    """
    Envoie un message de bienvenue WhatsApp après inscription
    """
    try:
        if not user.phone:
            return False
        
        phone_number = clean_phone_number(user.phone)
        if not phone_number:
            return False
        
        message = f"� *Bienvenue chez Parfum Store !*\n\n"
        message += f"Bonjour {user.first_name} !\n\n"
        message += f"Merci de vous être inscrit(e) sur notre boutique en ligne.\n\n"
        message += f"🌸 Découvrez notre collection exclusive de parfums de luxe\n"
        message += f"🚚 Livraison gratuite en France\n"
        message += f"🔄 Retour sous 30 jours\n"
        message += f"⭐ Parfums authentiques garantis\n\n"
        message += f"Vous recevrez des notifications WhatsApp pour vos commandes.\n\n"
        message += f"Bonne découverte !\n"
        message += f"*L'équipe Parfum Store*"
        
        return send_whatsapp_message_demo(phone_number, message)
        
    except Exception as e:
        logger.error(f"Erreur message bienvenue WhatsApp: {str(e)}")
        return False

def test_whatsapp_connection():
    """
    Test la connexion WhatsApp
    """
    try:
        test_message = f"🤖 *Test WhatsApp*\n\n"
        test_message += f"✅ Connexion WhatsApp fonctionnelle !\n"
        test_message += f"🕒 {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n"
        test_message += f"🌸 Parfum Store - Notifications activées"

        # Utiliser votre numéro marocain pour les tests
        test_number = "+212600154487"

        # Essayer d'abord avec le template Twilio
        try:
            variables = f'{{"1":"Test","2":"Connexion réussie"}}'
            return send_whatsapp_template_twilio(test_number, TWILIO_CONTENT_SID, variables)
        except:
            # Fallback: message simple
            return send_whatsapp_message_twilio(test_number, test_message)

    except Exception as e:
        logger.error(f"Erreur test WhatsApp: {str(e)}")
        return False

if __name__ == "__main__":
    # Test de la connexion
    print("Test de connexion WhatsApp...")
    if test_whatsapp_connection():
        print("✅ Connexion réussie!")
    else:
        print("❌ Échec de la connexion")
