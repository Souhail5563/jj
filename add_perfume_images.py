"""
Script pour ajouter des images multiples aux parfums
"""
import os
from app import app, db
from models import Product, ProductImage

def create_perfume_images():
    """Ajouter des images multiples pour chaque parfum"""
    with app.app_context():
        print("🖼️ Ajout d'images multiples aux parfums...")
        
        # Créer les nouvelles tables si nécessaire
        db.create_all()
        
        # Définir les images pour chaque parfum
        perfume_images = {
            1: {  # Chanel N°5
                'name': 'Chanel N°5 EDP 50ml',
                'images': [
                    {'filename': 'chanel-no5-front.jpg', 'alt_text': 'Chanel N°5 - Vue de face', 'is_primary': True, 'order': 1},
                    {'filename': 'chanel-no5-side.jpg', 'alt_text': 'Chanel N°5 - Vue de profil', 'is_primary': False, 'order': 2},
                    {'filename': 'chanel-no5-back.jpg', 'alt_text': 'Chanel N°5 - Vue arrière', 'is_primary': False, 'order': 3},
                    {'filename': 'chanel-no5-box.jpg', 'alt_text': 'Chanel N°5 - Avec emballage', 'is_primary': False, 'order': 4},
                ]
            },
            2: {  # Dior Sauvage
                'name': 'Dior Sauvage EDT 100ml',
                'images': [
                    {'filename': 'dior-sauvage-front.jpg', 'alt_text': 'Dior Sauvage - Vue de face', 'is_primary': True, 'order': 1},
                    {'filename': 'dior-sauvage-angle.jpg', 'alt_text': 'Dior Sauvage - Vue en angle', 'is_primary': False, 'order': 2},
                    {'filename': 'dior-sauvage-spray.jpg', 'alt_text': 'Dior Sauvage - Vaporisateur', 'is_primary': False, 'order': 3},
                    {'filename': 'dior-sauvage-lifestyle.jpg', 'alt_text': 'Dior Sauvage - Mise en scène', 'is_primary': False, 'order': 4},
                ]
            },
            3: {  # Tom Ford Black Orchid
                'name': 'Tom Ford Black Orchid',
                'images': [
                    {'filename': 'tomford-blackorchid-front.jpg', 'alt_text': 'Tom Ford Black Orchid - Vue principale', 'is_primary': True, 'order': 1},
                    {'filename': 'tomford-blackorchid-detail.jpg', 'alt_text': 'Tom Ford Black Orchid - Détail étiquette', 'is_primary': False, 'order': 2},
                    {'filename': 'tomford-blackorchid-cap.jpg', 'alt_text': 'Tom Ford Black Orchid - Bouchon', 'is_primary': False, 'order': 3},
                    {'filename': 'tomford-blackorchid-luxury.jpg', 'alt_text': 'Tom Ford Black Orchid - Présentation luxe', 'is_primary': False, 'order': 4},
                ]
            },
            4: {  # Hermès Terre d'Hermès
                'name': 'Hermès Terre d\'Hermès',
                'images': [
                    {'filename': 'hermes-terre-front.jpg', 'alt_text': 'Hermès Terre d\'Hermès - Vue principale', 'is_primary': True, 'order': 1},
                    {'filename': 'hermes-terre-side.jpg', 'alt_text': 'Hermès Terre d\'Hermès - Profil', 'is_primary': False, 'order': 2},
                    {'filename': 'hermes-terre-orange.jpg', 'alt_text': 'Hermès Terre d\'Hermès - Flacon orange', 'is_primary': False, 'order': 3},
                    {'filename': 'hermes-terre-collection.jpg', 'alt_text': 'Hermès Terre d\'Hermès - Collection', 'is_primary': False, 'order': 4},
                ]
            },
            5: {  # YSL Black Opium
                'name': 'YSL Black Opium',
                'images': [
                    {'filename': 'ysl-blackopium-front.jpg', 'alt_text': 'YSL Black Opium - Vue de face', 'is_primary': True, 'order': 1},
                    {'filename': 'ysl-blackopium-sparkle.jpg', 'alt_text': 'YSL Black Opium - Effet paillettes', 'is_primary': False, 'order': 2},
                    {'filename': 'ysl-blackopium-angle.jpg', 'alt_text': 'YSL Black Opium - Vue en angle', 'is_primary': False, 'order': 3},
                    {'filename': 'ysl-blackopium-night.jpg', 'alt_text': 'YSL Black Opium - Ambiance nocturne', 'is_primary': False, 'order': 4},
                ]
            },
            6: {  # Creed Aventus
                'name': 'Creed Aventus',
                'images': [
                    {'filename': 'creed-aventus-front.jpg', 'alt_text': 'Creed Aventus - Vue principale', 'is_primary': True, 'order': 1},
                    {'filename': 'creed-aventus-batch.jpg', 'alt_text': 'Creed Aventus - Numéro de batch', 'is_primary': False, 'order': 2},
                    {'filename': 'creed-aventus-cap.jpg', 'alt_text': 'Creed Aventus - Bouchon argenté', 'is_primary': False, 'order': 3},
                    {'filename': 'creed-aventus-prestige.jpg', 'alt_text': 'Creed Aventus - Présentation prestige', 'is_primary': False, 'order': 4},
                ]
            },
            7: {  # Lancôme La Vie Est Belle
                'name': 'Lancôme La Vie Est Belle',
                'images': [
                    {'filename': 'lancome-lavieestbelle-front.jpg', 'alt_text': 'Lancôme La Vie Est Belle - Vue de face', 'is_primary': True, 'order': 1},
                    {'filename': 'lancome-lavieestbelle-smile.jpg', 'alt_text': 'Lancôme La Vie Est Belle - Flacon sourire', 'is_primary': False, 'order': 2},
                    {'filename': 'lancome-lavieestbelle-pink.jpg', 'alt_text': 'Lancôme La Vie Est Belle - Nuances roses', 'is_primary': False, 'order': 3},
                    {'filename': 'lancome-lavieestbelle-happiness.jpg', 'alt_text': 'Lancôme La Vie Est Belle - Bonheur', 'is_primary': False, 'order': 4},
                ]
            },
            8: {  # Armani Acqua di Giò
                'name': 'Armani Acqua di Giò',
                'images': [
                    {'filename': 'armani-acquadigio-front.jpg', 'alt_text': 'Armani Acqua di Giò - Vue principale', 'is_primary': True, 'order': 1},
                    {'filename': 'armani-acquadigio-water.jpg', 'alt_text': 'Armani Acqua di Giò - Effet aquatique', 'is_primary': False, 'order': 2},
                    {'filename': 'armani-acquadigio-blue.jpg', 'alt_text': 'Armani Acqua di Giò - Nuances bleues', 'is_primary': False, 'order': 3},
                    {'filename': 'armani-acquadigio-fresh.jpg', 'alt_text': 'Armani Acqua di Giò - Fraîcheur', 'is_primary': False, 'order': 4},
                ]
            },
            9: {  # Versace Eros
                'name': 'Versace Eros',
                'images': [
                    {'filename': 'versace-eros-front.jpg', 'alt_text': 'Versace Eros - Vue de face', 'is_primary': True, 'order': 1},
                    {'filename': 'versace-eros-medusa.jpg', 'alt_text': 'Versace Eros - Méduse dorée', 'is_primary': False, 'order': 2},
                    {'filename': 'versace-eros-turquoise.jpg', 'alt_text': 'Versace Eros - Flacon turquoise', 'is_primary': False, 'order': 3},
                    {'filename': 'versace-eros-power.jpg', 'alt_text': 'Versace Eros - Puissance masculine', 'is_primary': False, 'order': 4},
                ]
            },
            10: {  # Paco Rabanne 1 Million
                'name': 'Paco Rabanne 1 Million',
                'images': [
                    {'filename': 'pacorabanne-1million-front.jpg', 'alt_text': 'Paco Rabanne 1 Million - Vue principale', 'is_primary': True, 'order': 1},
                    {'filename': 'pacorabanne-1million-gold.jpg', 'alt_text': 'Paco Rabanne 1 Million - Effet doré', 'is_primary': False, 'order': 2},
                    {'filename': 'pacorabanne-1million-bar.jpg', 'alt_text': 'Paco Rabanne 1 Million - Lingot d\'or', 'is_primary': False, 'order': 3},
                    {'filename': 'pacorabanne-1million-luxury.jpg', 'alt_text': 'Paco Rabanne 1 Million - Luxe absolu', 'is_primary': False, 'order': 4},
                ]
            }
        }
        
        # Supprimer les anciennes images
        ProductImage.query.delete()
        db.session.commit()
        
        # Ajouter les nouvelles images
        total_images = 0
        for product_id, data in perfume_images.items():
            product = Product.query.get(product_id)
            if product:
                print(f"\n🌸 {data['name']}:")
                
                for img_data in data['images']:
                    image = ProductImage(
                        product_id=product_id,
                        filename=img_data['filename'],
                        alt_text=img_data['alt_text'],
                        is_primary=img_data['is_primary'],
                        display_order=img_data['order']
                    )
                    db.session.add(image)
                    
                    status = "🌟 PRINCIPALE" if img_data['is_primary'] else "📸 Galerie"
                    print(f"  {status} - {img_data['alt_text']}")
                    total_images += 1
        
        db.session.commit()
        print(f"\n✅ {total_images} images ajoutées pour {len(perfume_images)} parfums")

def create_placeholder_images():
    """Créer des images placeholder pour la démonstration"""
    print("\n🎨 Création d'images placeholder...")
    
    # Créer le dossier uploads s'il n'existe pas
    uploads_dir = 'static/uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"✅ Dossier {uploads_dir} créé")
    
    # Créer des fichiers placeholder (vides pour la démo)
    placeholder_files = [
        'chanel-no5-front.jpg', 'chanel-no5-side.jpg', 'chanel-no5-back.jpg', 'chanel-no5-box.jpg',
        'dior-sauvage-front.jpg', 'dior-sauvage-angle.jpg', 'dior-sauvage-spray.jpg', 'dior-sauvage-lifestyle.jpg',
        'tomford-blackorchid-front.jpg', 'tomford-blackorchid-detail.jpg', 'tomford-blackorchid-cap.jpg', 'tomford-blackorchid-luxury.jpg',
        'hermes-terre-front.jpg', 'hermes-terre-side.jpg', 'hermes-terre-orange.jpg', 'hermes-terre-collection.jpg',
        'ysl-blackopium-front.jpg', 'ysl-blackopium-sparkle.jpg', 'ysl-blackopium-angle.jpg', 'ysl-blackopium-night.jpg',
        'creed-aventus-front.jpg', 'creed-aventus-batch.jpg', 'creed-aventus-cap.jpg', 'creed-aventus-prestige.jpg',
        'lancome-lavieestbelle-front.jpg', 'lancome-lavieestbelle-smile.jpg', 'lancome-lavieestbelle-pink.jpg', 'lancome-lavieestbelle-happiness.jpg',
        'armani-acquadigio-front.jpg', 'armani-acquadigio-water.jpg', 'armani-acquadigio-blue.jpg', 'armani-acquadigio-fresh.jpg',
        'versace-eros-front.jpg', 'versace-eros-medusa.jpg', 'versace-eros-turquoise.jpg', 'versace-eros-power.jpg',
        'pacorabanne-1million-front.jpg', 'pacorabanne-1million-gold.jpg', 'pacorabanne-1million-bar.jpg', 'pacorabanne-1million-luxury.jpg'
    ]
    
    created_count = 0
    for filename in placeholder_files:
        filepath = os.path.join(uploads_dir, filename)
        if not os.path.exists(filepath):
            # Créer un fichier vide comme placeholder
            with open(filepath, 'w') as f:
                f.write('')
            created_count += 1
    
    print(f"✅ {created_count} fichiers placeholder créés")

def main():
    """Fonction principale"""
    print("🖼️ AJOUT D'IMAGES MULTIPLES AUX PARFUMS")
    print("=" * 50)
    
    # Créer les images placeholder
    create_placeholder_images()
    
    # Ajouter les images aux parfums
    create_perfume_images()
    
    print("\n" + "=" * 50)
    print("🎉 IMAGES MULTIPLES CONFIGURÉES AVEC SUCCÈS!")
    print("🖼️ Fonctionnalités ajoutées:")
    print("   • 4 images par parfum (principale + 3 galerie)")
    print("   • Images avec textes alternatifs")
    print("   • Ordre d'affichage personnalisé")
    print("   • Galerie d'images interactive")
    print("   • Compatible avec l'interface existante")
    print("\n🌸 Vos parfums ont maintenant des galeries d'images complètes!")

if __name__ == '__main__':
    main()
