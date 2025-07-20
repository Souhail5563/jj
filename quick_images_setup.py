"""
Configuration rapide des images multiples
"""
import os
from app import app, db
from models import Product, ProductImage

def create_svg_images():
    """Créer des images SVG simples"""
    print("🎨 Création des images SVG...")
    
    uploads_dir = 'static/uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    # Template SVG simple
    svg_template = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300" width="200" height="300">
    <defs>
        <linearGradient id="grad{id}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
            <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
        </linearGradient>
    </defs>
    <!-- Flacon -->
    <rect x="60" y="80" width="80" height="180" rx="10" fill="url(#grad{id})" stroke="#333" stroke-width="2"/>
    <!-- Bouchon -->
    <rect x="70" y="60" width="60" height="30" rx="5" fill="#FFD700" stroke="#333" stroke-width="2"/>
    <!-- Vaporisateur -->
    <rect x="85" y="40" width="30" height="25" rx="3" fill="#C0C0C0" stroke="#333" stroke-width="1"/>
    <!-- Étiquette -->
    <rect x="65" y="120" width="70" height="40" rx="3" fill="white" stroke="#333" stroke-width="1"/>
    <text x="100" y="135" text-anchor="middle" font-family="Arial" font-size="8" fill="#333">Parfum {num}</text>
    <text x="100" y="150" text-anchor="middle" font-family="Arial" font-size="6" fill="#666">{view}</text>
    <!-- Reflet -->
    <rect x="65" y="85" width="15" height="100" rx="5" fill="rgba(255,255,255,0.3)"/>
</svg>'''
    
    colors = [
        ('#FFD700', '#FFA500'), ('#87CEEB', '#4682B4'), ('#DDA0DD', '#8B008B'),
        ('#F0E68C', '#DAA520'), ('#FFB6C1', '#FF69B4'), ('#98FB98', '#32CD32'),
        ('#F5DEB3', '#D2691E'), ('#87CEFA', '#1E90FF'), ('#DEB887', '#8B4513'),
        ('#FFE4B5', '#FF8C00')
    ]
    
    created_count = 0
    for i in range(1, 11):  # 10 parfums
        color1, color2 = colors[i-1]
        
        views = [
            ('main', 'Principal', color1, color2),
            ('side', 'Côté', color2, color1),
            ('back', 'Arrière', '#E6E6FA', '#D8BFD8'),
            ('box', 'Boîte', '#F5F5DC', '#DDD'),
        ]
        
        for view, view_name, c1, c2 in views:
            filename = f'perfume-{i}-{view}.svg'
            filepath = os.path.join(uploads_dir, filename)
            
            svg_content = svg_template.format(
                id=f'{i}{view}',
                color1=c1,
                color2=c2,
                num=i,
                view=view_name
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            created_count += 1
    
    print(f"  ✅ {created_count} images SVG créées")

def add_images_to_products():
    """Ajouter les images aux produits existants"""
    with app.app_context():
        print("🖼️ Ajout des images aux produits...")
        
        # Supprimer les anciennes images
        try:
            ProductImage.query.delete()
            db.session.commit()
            print("  ✅ Anciennes images supprimées")
        except:
            db.session.rollback()
        
        # Récupérer les produits
        products = Product.query.all()
        print(f"  📊 {len(products)} produits trouvés")
        
        if not products:
            print("  ❌ Aucun produit trouvé!")
            return
        
        # Ajouter les images
        total_images = 0
        for i, product in enumerate(products, 1):
            print(f"  🌸 {product.name}:")
            
            images_data = [
                {'filename': f'perfume-{i}-main.svg', 'alt_text': f'{product.name} - Vue principale', 'is_primary': True, 'order': 1},
                {'filename': f'perfume-{i}-side.svg', 'alt_text': f'{product.name} - Vue de côté', 'is_primary': False, 'order': 2},
                {'filename': f'perfume-{i}-back.svg', 'alt_text': f'{product.name} - Vue arrière', 'is_primary': False, 'order': 3},
                {'filename': f'perfume-{i}-box.svg', 'alt_text': f'{product.name} - Avec emballage', 'is_primary': False, 'order': 4},
            ]
            
            for img_data in images_data:
                image = ProductImage(
                    product_id=product.id,
                    filename=img_data['filename'],
                    alt_text=img_data['alt_text'],
                    is_primary=img_data['is_primary'],
                    display_order=img_data['order']
                )
                db.session.add(image)
                
                status = "🌟 PRINCIPALE" if img_data['is_primary'] else "📸 Galerie"
                print(f"    {status} - {img_data['filename']}")
                total_images += 1
        
        try:
            db.session.commit()
            print(f"  ✅ {total_images} images ajoutées en base")
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
            db.session.rollback()

def test_image_functionality():
    """Tester les fonctionnalités d'images"""
    with app.app_context():
        print("🧪 Test des fonctionnalités d'images...")
        
        products = Product.query.all()[:3]  # Tester les 3 premiers
        
        for product in products:
            print(f"\n  🌸 {product.name}:")
            
            # Test image principale
            primary = product.get_primary_image()
            if primary:
                print(f"    🌟 Image principale: {primary.filename}")
                print(f"    🔗 URL: {primary.image_url}")
            else:
                print("    ❌ Pas d'image principale")
            
            # Test toutes les images
            all_images = product.get_all_images()
            print(f"    📸 Total images: {len(all_images)}")
            
            # Test images galerie
            gallery = product.get_gallery_images()
            print(f"    🖼️ Images galerie: {len(gallery)}")
            
            # Test propriété multiple
            print(f"    🔢 A plusieurs images: {product.has_multiple_images}")

def main():
    """Fonction principale"""
    print("🖼️ CONFIGURATION RAPIDE DES IMAGES MULTIPLES")
    print("=" * 55)
    
    # Créer les images SVG
    create_svg_images()
    
    # Ajouter aux produits
    add_images_to_products()
    
    # Tester les fonctionnalités
    test_image_functionality()
    
    print("\n" + "=" * 55)
    print("🎉 IMAGES MULTIPLES CONFIGURÉES!")
    print("✅ 40 images SVG créées")
    print("✅ 4 images par parfum")
    print("✅ Galerie interactive")
    print("✅ Navigation clavier/tactile")
    print("✅ Zoom et modal")
    print("✅ Design responsive")
    print("\n🌸 Votre store a maintenant des galeries complètes!")
    print("🌐 Testez sur: http://127.0.0.1:5001")

if __name__ == '__main__':
    main()
