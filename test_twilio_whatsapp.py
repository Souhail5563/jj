"""
Test des notifications WhatsApp avec les vraies informations Twilio
"""
from whatsapp_bot import (
    send_whatsapp_message_twilio, 
    send_whatsapp_template_twilio, 
    test_whatsapp_connection,
    clean_phone_number,
    TWILIO_CONTENT_SID
)
from datetime import datetime

def test_twilio_connection():
    """Test de base de la connexion Twilio"""
    print("🚀 Test de connexion Twilio WhatsApp...")
    
    try:
        from twilio.rest import Client
        from whatsapp_bot import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Vérifier que le client peut se connecter
        account = client.api.accounts(TWILIO_ACCOUNT_SID).fetch()
        print(f"✅ Connexion Twilio réussie!")
        print(f"   Account SID: {account.sid}")
        print(f"   Account Name: {account.friendly_name}")
        print(f"   Status: {account.status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur connexion Twilio: {str(e)}")
        return False

def test_simple_message():
    """Test d'envoi d'un message simple"""
    print("\n📱 Test d'envoi de message simple...")
    
    test_number = "+212600154487"  # Votre numéro marocain
    test_message = f"🎉 Test Bijoux Store\n\n"
    test_message += f"✅ Message de test envoyé avec succès!\n"
    test_message += f"🕒 {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n"
    test_message += f"🛍️ Système de notifications WhatsApp opérationnel"
    
    success = send_whatsapp_message_twilio(test_number, test_message)
    
    if success:
        print("✅ Message simple envoyé avec succès!")
    else:
        print("❌ Échec envoi message simple")
    
    return success

def test_template_message():
    """Test d'envoi avec template de contenu"""
    print("\n📋 Test d'envoi avec template de contenu...")
    
    test_number = "+212600154487"  # Votre numéro marocain
    
    # Variables pour votre template existant
    variables = '{"1":"#TEST123","2":"Confirmée"}'
    
    success = send_whatsapp_template_twilio(test_number, TWILIO_CONTENT_SID, variables)
    
    if success:
        print("✅ Template envoyé avec succès!")
    else:
        print("❌ Échec envoi template")
    
    return success

def test_phone_number_cleaning():
    """Test du nettoyage des numéros de téléphone"""
    print("\n🧹 Test du nettoyage des numéros de téléphone...")
    
    test_numbers = [
        "0123456789",           # Français
        "600154487",            # Marocain sans préfixe
        "+212600154487",        # Marocain complet
        "+33123456789",         # Français complet
        "06 12 34 56 78",       # Français avec espaces
        "06.12.34.56.78",       # Français avec points
        "06-12-34-56-78",       # Français avec tirets
    ]
    
    for number in test_numbers:
        cleaned = clean_phone_number(number)
        print(f"  {number:20} → {cleaned}")

def test_order_simulation():
    """Simulation d'une commande avec notifications"""
    print("\n🛍️ Simulation d'une commande avec notifications...")
    
    # Simuler une commande
    class MockUser:
        def __init__(self, phone):
            self.id = 1
            self.phone = phone
            self.first_name = "Test"
            self.last_name = "Client"
    
    class MockOrder:
        def __init__(self, user):
            self.id = 123
            self.user = user
            self.total_amount = 299.99
            self.shipping_address = "123 Rue Test\n10000 Rabat, Maroc"
    
    # Créer une commande de test
    user = MockUser("+212600154487")
    order = MockOrder(user)
    
    # Test des différents statuts
    statuses = [
        ('pending', 'confirmed'),
        ('confirmed', 'shipped'),
        ('shipped', 'delivered')
    ]
    
    from whatsapp_bot import send_order_status_notification
    
    for old_status, new_status in statuses:
        print(f"\n📱 Test notification: {old_status} → {new_status}")
        success = send_order_status_notification(order, old_status, new_status)
        
        if success:
            print(f"✅ Notification '{new_status}' envoyée!")
        else:
            print(f"❌ Échec notification '{new_status}'")
        
        # Attendre un peu entre les envois
        import time
        time.sleep(2)

def test_admin_button():
    """Test du bouton admin"""
    print("\n🔧 Test du bouton admin...")
    
    success = test_whatsapp_connection()
    
    if success:
        print("✅ Test bouton admin réussi!")
    else:
        print("❌ Échec test bouton admin")
    
    return success

def main():
    """Fonction principale de test"""
    print("🎉 Démarrage des tests WhatsApp Twilio...")
    print("=" * 50)
    
    # 1. Test de connexion de base
    if not test_twilio_connection():
        print("\n❌ Échec de connexion Twilio. Vérifiez vos identifiants.")
        return
    
    # 2. Test du nettoyage des numéros
    test_phone_number_cleaning()
    
    # 3. Test message simple
    print("\n" + "=" * 50)
    test_simple_message()
    
    # Attendre un peu
    import time
    time.sleep(3)
    
    # 4. Test template
    print("\n" + "=" * 50)
    test_template_message()
    
    time.sleep(3)
    
    # 5. Test bouton admin
    print("\n" + "=" * 50)
    test_admin_button()
    
    time.sleep(3)
    
    # 6. Simulation complète de commande
    print("\n" + "=" * 50)
    test_order_simulation()
    
    print("\n" + "=" * 50)
    print("🎉 Tests terminés!")
    print("📱 Vérifiez votre WhatsApp pour voir les messages reçus")
    print("🔗 Si tout fonctionne, les notifications sont prêtes pour la production!")

if __name__ == '__main__':
    main()
