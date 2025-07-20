"""
Script de migration pour convertir le site de bijoux en site de parfums
"""
from app import app, db
from models import Product, FooterSettings
from sqlalchemy import text

def migrate_database():
    """Migrer la base de données pour les parfums"""
    with app.app_context():
        print("🔄 Migration de la base de données vers les parfums...")
        
        try:
            # Ajouter les nouvelles colonnes pour les parfums
            print("\n1️⃣ Ajout des nouvelles colonnes...")
            
            # Vérifier si les colonnes existent déjà
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('product')]
            
            new_columns = [
                ('brand', 'VARCHAR(50)'),
                ('volume', 'INTEGER'),
                ('concentration', 'VARCHAR(30)'),
                ('fragrance_family', 'VARCHAR(50)'),
                ('top_notes', 'TEXT'),
                ('heart_notes', 'TEXT'),
                ('base_notes', 'TEXT'),
                ('gender', 'VARCHAR(20)')
            ]
            
            for col_name, col_type in new_columns:
                if col_name not in columns:
                    try:
                        db.engine.execute(text(f'ALTER TABLE product ADD COLUMN {col_name} {col_type}'))
                        print(f"✅ Colonne '{col_name}' ajoutée")
                    except Exception as e:
                        print(f"⚠️ Erreur ajout colonne '{col_name}': {e}")
                else:
                    print(f"✅ Colonne '{col_name}' existe déjà")
            
            # Supprimer l'ancienne colonne 'material' si elle existe
            if 'material' in columns:
                try:
                    # SQLite ne supporte pas DROP COLUMN, on va juste l'ignorer
                    print("⚠️ Colonne 'material' conservée (SQLite ne supporte pas DROP COLUMN)")
                except Exception as e:
                    print(f"⚠️ Erreur suppression colonne 'material': {e}")
            
            db.session.commit()
            print("✅ Migration des colonnes terminée")
            
        except Exception as e:
            print(f"❌ Erreur migration base de données: {e}")
            db.session.rollback()

def create_perfume_products():
    """Créer des produits parfums de démonstration"""
    with app.app_context():
        print("\n2️⃣ Création des produits parfums...")
        
        # Supprimer les anciens produits bijoux
        Product.query.delete()
        
        perfumes = [
            {
                'name': 'Chanel N°5 Eau de Parfum',
                'description': 'Le parfum le plus célèbre au monde. Un bouquet floral aldéhydé intemporel et mystérieux.',
                'price': 89.90,
                'category': 'Eau de Parfum',
                'brand': 'Chanel',
                'volume': 50,
                'concentration': 'EDP',
                'fragrance_family': 'Floral Aldéhydé',
                'top_notes': 'Aldéhydes, Ylang-ylang, Néroli',
                'heart_notes': 'Rose de mai, Jasmin, Muguet',
                'base_notes': 'Santal, Vétiver, Vanille',
                'gender': 'Femme',
                'stock_quantity': 25
            },
            {
                'name': 'Dior Sauvage Eau de Toilette',
                'description': 'Un parfum masculin frais et puissant inspiré des grands espaces.',
                'price': 79.90,
                'category': 'Eau de Toilette',
                'brand': 'Dior',
                'volume': 100,
                'concentration': 'EDT',
                'fragrance_family': 'Aromatique Boisé',
                'top_notes': 'Bergamote de Calabre, Poivre rose',
                'heart_notes': 'Géranium, Lavande, Elemi',
                'base_notes': 'Ambroxan, Cèdre, Labdanum',
                'gender': 'Homme',
                'stock_quantity': 30
            },
            {
                'name': 'Tom Ford Black Orchid',
                'description': 'Un parfum luxueux et mystérieux aux accords floraux noirs et épicés.',
                'price': 129.90,
                'category': 'Eau de Parfum',
                'brand': 'Tom Ford',
                'volume': 50,
                'concentration': 'EDP',
                'fragrance_family': 'Oriental Floral',
                'top_notes': 'Truffe, Ylang-ylang, Bergamote',
                'heart_notes': 'Orchidée noire, Épices, Fruits',
                'base_notes': 'Patchouli, Vanille, Santal',
                'gender': 'Mixte',
                'stock_quantity': 15
            },
            {
                'name': 'Hermès Terre d\'Hermès',
                'description': 'Un parfum qui raconte la relation de l\'homme à la terre.',
                'price': 94.90,
                'category': 'Eau de Toilette',
                'brand': 'Hermès',
                'volume': 100,
                'concentration': 'EDT',
                'fragrance_family': 'Boisé Minéral',
                'top_notes': 'Orange, Pamplemousse',
                'heart_notes': 'Poivre, Pélargonium, Silex',
                'base_notes': 'Vétiver, Cèdre, Benzoin',
                'gender': 'Homme',
                'stock_quantity': 20
            },
            {
                'name': 'Yves Saint Laurent Black Opium',
                'description': 'Un parfum féminin addictif aux notes de café et de vanille.',
                'price': 84.90,
                'category': 'Eau de Parfum',
                'brand': 'Yves Saint Laurent',
                'volume': 50,
                'concentration': 'EDP',
                'fragrance_family': 'Oriental Gourmand',
                'top_notes': 'Cassis, Poire',
                'heart_notes': 'Café, Jasmin, Fleur d\'oranger',
                'base_notes': 'Vanille, Patchouli, Cèdre',
                'gender': 'Femme',
                'stock_quantity': 22
            },
            {
                'name': 'Creed Aventus',
                'description': 'Un parfum masculin légendaire aux notes fruitées et boisées.',
                'price': 189.90,
                'category': 'Eau de Parfum',
                'brand': 'Creed',
                'volume': 50,
                'concentration': 'EDP',
                'fragrance_family': 'Fruité Boisé',
                'top_notes': 'Ananas, Cassis, Pomme, Bergamote',
                'heart_notes': 'Bouleau, Patchouli, Jasmin, Rose',
                'base_notes': 'Musc, Chêne, Ambre gris, Vanille',
                'gender': 'Homme',
                'stock_quantity': 10
            }
        ]
        
        for perfume_data in perfumes:
            perfume = Product(**perfume_data)
            db.session.add(perfume)
            print(f"✅ Parfum créé: {perfume_data['name']}")
        
        db.session.commit()
        print(f"✅ {len(perfumes)} parfums créés avec succès")

def update_footer_settings():
    """Mettre à jour les paramètres du footer"""
    with app.app_context():
        print("\n3️⃣ Mise à jour des paramètres du footer...")
        
        # Supprimer les anciens paramètres
        FooterSettings.query.delete()
        db.session.commit()
        
        # Les nouveaux paramètres seront créés automatiquement par get_settings()
        settings = FooterSettings.get_settings()
        print("✅ Paramètres du footer mis à jour pour les parfums")

def main():
    """Fonction principale de migration"""
    print("🌸 Migration du site Bijoux vers Parfums")
    print("=" * 50)
    
    # 1. Migrer la base de données
    migrate_database()
    
    # 2. Créer les produits parfums
    create_perfume_products()
    
    # 3. Mettre à jour les paramètres
    update_footer_settings()
    
    print("\n" + "=" * 50)
    print("🎉 Migration terminée avec succès!")
    print("🌸 Le site est maintenant configuré pour les parfums")
    print("🔗 Redémarrez le serveur Flask pour voir les changements")

if __name__ == '__main__':
    main()
