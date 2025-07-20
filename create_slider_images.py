"""
Script pour créer des images de slider de démonstration
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_slider_image(width, height, bg_color, text, filename):
    """Créer une image de slider simple avec du texte"""
    # Créer une nouvelle image
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Essayer d'utiliser une police système
    try:
        font = ImageFont.truetype("arial.ttf", 60)
        small_font = ImageFont.truetype("arial.ttf", 30)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 60)
            small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 30)
        except:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
    
    # Ajouter un gradient simple
    for y in range(height):
        alpha = int(255 * (1 - y / height * 0.3))
        for x in range(width):
            r, g, b = bg_color
            new_color = (min(255, r + alpha//4), min(255, g + alpha//4), min(255, b + alpha//4))
            img.putpixel((x, y), new_color)
    
    # Ajouter le texte
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Ombre du texte
    draw.text((x+3, y+3), text, font=font, fill=(0, 0, 0, 128))
    # Texte principal
    draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    # Ajouter "Bijoux Store" en petit
    store_text = "BIJOUX STORE"
    store_bbox = draw.textbbox((0, 0), store_text, font=small_font)
    store_width = store_bbox[2] - store_bbox[0]
    store_x = (width - store_width) // 2
    store_y = y + text_height + 20
    
    draw.text((store_x+2, store_y+2), store_text, font=small_font, fill=(0, 0, 0, 128))
    draw.text((store_x, store_y), store_text, font=small_font, fill=(255, 215, 0))
    
    # Sauvegarder l'image
    img.save(filename, 'JPEG', quality=85)
    print(f"Image créée: {filename}")

def main():
    # Créer le dossier s'il n'existe pas
    os.makedirs('static/uploads/sliders', exist_ok=True)
    
    # Créer les images de slider
    sliders = [
        {
            'filename': 'static/uploads/sliders/slider1.jpg',
            'bg_color': (139, 69, 19),  # Marron bijoux
            'text': 'Collection 2024'
        },
        {
            'filename': 'static/uploads/sliders/slider2.jpg',
            'bg_color': (75, 0, 130),   # Violet royal
            'text': 'Bagues de Fiançailles'
        },
        {
            'filename': 'static/uploads/sliders/slider3.jpg',
            'bg_color': (220, 20, 60),  # Rouge promotion
            'text': 'Offre Spéciale -20%'
        }
    ]
    
    for slider in sliders:
        create_slider_image(
            width=1920,
            height=600,
            bg_color=slider['bg_color'],
            text=slider['text'],
            filename=slider['filename']
        )
    
    print("Toutes les images de slider ont été créées avec succès!")

if __name__ == '__main__':
    main()
