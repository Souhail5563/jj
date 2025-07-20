from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from dotenv import load_dotenv

# Import des modèles
from models import db, User, Product, ProductImage, Order, OrderItem, CartItem, Slider, FooterSettings

# Import du module Telegram
from telegram_bot import send_order_notification, send_order_status_update, test_telegram_connection

# Import du module WhatsApp
from whatsapp_bot import send_order_status_notification, send_welcome_message, test_whatsapp_connection

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///bijoux_store.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Créer le dossier uploads s'il n'existe pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)

# Extensions de fichiers autorisées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

def allowed_file(filename):
    """Vérifier si l'extension du fichier est autorisée"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialiser la base de données avec l'app
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context processor pour rendre les paramètres du footer disponibles partout
@app.context_processor
def inject_footer_settings():
    return dict(footer_settings=FooterSettings.get_settings())

# Routes principales
@app.route('/')
def index():
    products = Product.query.filter_by(active=True).limit(8).all()
    sliders = Slider.query.filter_by(active=True).order_by(Slider.order_position.asc()).all()
    return render_template('index.html', products=products, sliders=sliders)

@app.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    
    query = Product.query.filter_by(active=True)
    if category:
        query = query.filter_by(category=category)
    
    products = query.paginate(page=page, per_page=12, error_out=False)
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('catalog.html', products=products, categories=categories, current_category=category)

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

# Routes d'authentification
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Connexion réussie!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Email ou mot de passe incorrect.', 'error')

    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé.', 'error')
            return render_template('auth/register.html')

        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur est déjà pris.', 'error')
            return render_template('auth/register.html')

        # Créer le nouvel utilisateur
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(user)
        db.session.commit()

        # Envoyer message de bienvenue WhatsApp
        try:
            send_welcome_message(user)
        except Exception as e:
            print(f"Erreur message bienvenue WhatsApp: {e}")

        flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))

# Routes du panier et commandes
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))

    if product.stock_quantity < quantity:
        flash('Quantité demandée non disponible.', 'error')
        return redirect(url_for('product_detail', id=product_id))

    # Vérifier si le produit est déjà dans le panier
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    flash(f'{product.name} ajouté au panier!', 'success')
    return redirect(url_for('product_detail', id=product_id))

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        flash('Action non autorisée.', 'error')
        return redirect(url_for('cart'))

    db.session.delete(cart_item)
    db.session.commit()
    flash('Produit retiré du panier.', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash('Votre panier est vide.', 'error')
        return redirect(url_for('cart'))

    if request.method == 'POST':
        # Vérifier le stock
        for item in cart_items:
            if item.product.stock_quantity < item.quantity:
                flash(f'Stock insuffisant pour {item.product.name}', 'error')
                return redirect(url_for('cart'))

        # Créer la commande
        total = sum(item.product.price * item.quantity for item in cart_items)
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=request.form['address'],
            phone=request.form['phone'],
            notes=request.form.get('notes', '')
        )
        db.session.add(order)
        db.session.flush()  # Pour obtenir l'ID de la commande

        # Créer les items de commande et mettre à jour le stock
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)

            # Mettre à jour le stock
            item.product.stock_quantity -= item.quantity

        # Vider le panier
        CartItem.query.filter_by(user_id=current_user.id).delete()

        db.session.commit()

        # Envoyer notification Telegram
        try:
            send_order_notification(order)
        except Exception as e:
            # Ne pas faire échouer la commande si Telegram ne fonctionne pas
            print(f"Erreur notification Telegram: {e}")

        flash('Commande passée avec succès!', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))

    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/order_confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Commande non trouvée.', 'error')
        return redirect(url_for('index'))
    return render_template('order_confirmation.html', order=order)

@app.route('/my_orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        current_user.phone = request.form['phone']
        current_user.address = request.form['address']
        db.session.commit()
        flash('Profil mis à jour avec succès!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html')

# Routes administrateur
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès non autorisé.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    # Statistiques
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.filter_by(is_admin=False).count()
    low_stock_products = Product.query.filter(Product.stock_quantity <= Product.min_stock_alert).count()

    # Commandes récentes
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()

    # Statistiques des sliders
    total_sliders = Slider.query.count()
    active_sliders = Slider.query.filter_by(active=True).count()

    return render_template('admin/dashboard.html',
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         low_stock_products=low_stock_products,
                         recent_orders=recent_orders,
                         total_sliders=total_sliders,
                         active_sliders=active_sliders)

@app.route('/admin/products')
@login_required
@admin_required
def admin_products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_product():
    if request.method == 'POST':
        try:
            # Créer le produit parfum
            product = Product(
                name=request.form['name'],
                description=request.form['description'],
                price=float(request.form['price']),
                category=request.form['category'],
                material=request.form['material'],
                stock_quantity=int(request.form['stock_quantity']),
                min_stock_alert=int(request.form.get('min_stock_alert', 5))
            )
            db.session.add(product)
            db.session.flush()  # Pour obtenir l'ID du produit

            # Gestion des images multiples
            image_types = ['image_main', 'image_side', 'image_back', 'image_box']
            image_labels = ['Vue principale', 'Vue de côté', 'Vue arrière', 'Avec emballage']
            images_added = 0

            for i, (image_type, label) in enumerate(zip(image_types, image_labels)):
                if image_type in request.files:
                    file = request.files[image_type]
                    if file and file.filename != '':
                        # Validation du fichier
                        if not allowed_file(file.filename):
                            flash(f'Format de fichier non autorisé pour {label}.', 'error')
                            continue

                        # Sauvegarder le fichier
                        filename = secure_filename(file.filename)
                        import time
                        timestamp = int(time.time())
                        filename = f"perfume_{product.id}_{timestamp}_{i}_{filename}"
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(file_path)

                        # Créer l'enregistrement ProductImage
                        product_image = ProductImage(
                            product_id=product.id,
                            filename=filename,
                            alt_text=f"{product.name} - {label}",
                            is_primary=(i == 0),  # La première image est principale
                            display_order=i + 1
                        )
                        db.session.add(product_image)
                        images_added += 1

            db.session.commit()

            success_msg = f'Parfum "{product.name}" ajouté avec succès!'
            if images_added > 0:
                success_msg += f' ({images_added} image(s) ajoutée(s))'
            flash(success_msg, 'success')

            return redirect(url_for('admin_products'))

        except ValueError as e:
            flash(f'Erreur de validation: {str(e)}', 'error')
            db.session.rollback()
        except Exception as e:
            flash(f'Erreur lors de l\'ajout du parfum: {str(e)}', 'error')
            db.session.rollback()

    return render_template('admin/add_product.html')

@app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        # Gestion de l'upload d'image
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                # Supprimer l'ancienne image si elle existe
                if product.image_filename:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                filename = secure_filename(file.filename)
                import time
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                product.image_filename = filename

        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.category = request.form['category']
        product.material = request.form['material']
        product.stock_quantity = int(request.form['stock_quantity'])
        product.min_stock_alert = int(request.form.get('min_stock_alert', 5))
        product.active = 'active' in request.form

        db.session.commit()
        flash('Produit modifié avec succès!', 'success')
        return redirect(url_for('admin_products'))

    return render_template('admin/edit_product.html', product=product)

@app.route('/admin/products/delete/<int:id>')
@login_required
@admin_required
def admin_delete_product(id):
    product = Product.query.get_or_404(id)

    # Supprimer l'image si elle existe
    if product.image_filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()
    flash('Produit supprimé avec succès!', 'success')
    return redirect(url_for('admin_products'))

# Routes manquantes pour compléter l'application
@app.route('/admin/orders')
@login_required
@admin_required
def admin_orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/stock')
@login_required
@admin_required
def admin_stock():
    products = Product.query.filter(Product.stock_quantity <= Product.min_stock_alert).all()
    return render_template('admin/stock.html', products=products)

@app.route('/admin/orders/<int:order_id>')
@login_required
@admin_required
def admin_order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@app.route('/admin/orders/<int:order_id>/update_status', methods=['POST'])
@login_required
@admin_required
def admin_update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status') or request.json.get('status')

    if new_status in ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']:
        old_status = order.status
        order.status = new_status
        db.session.commit()

        # Envoyer notification Telegram pour changement de statut
        try:
            if old_status != new_status:
                send_order_status_update(order, old_status, new_status)
        except Exception as e:
            print(f"Erreur notification Telegram: {e}")

        # Envoyer notification WhatsApp au client
        try:
            if old_status != new_status:
                send_order_status_notification(order, old_status, new_status)
        except Exception as e:
            print(f"Erreur notification WhatsApp: {e}")

        if request.is_json:
            return jsonify({'success': True})
        else:
            flash('Statut de la commande mis à jour avec succès!', 'success')
            return redirect(url_for('admin_order_detail', order_id=order_id))

    if request.is_json:
        return jsonify({'success': False, 'error': 'Statut invalide'})
    else:
        flash('Statut invalide.', 'error')
        return redirect(url_for('admin_order_detail', order_id=order_id))

@app.route('/admin/products/<int:product_id>/update_stock', methods=['POST'])
@login_required
@admin_required
def admin_update_stock(product_id):
    product = Product.query.get_or_404(product_id)
    new_stock = int(request.form.get('new_stock', 0))

    product.stock_quantity = new_stock
    db.session.commit()

    return jsonify({'success': True})

@app.route('/admin/orders/<int:order_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_order(order_id):
    order = Order.query.get_or_404(order_id)

    try:
        # Supprimer d'abord les items de la commande
        OrderItem.query.filter_by(order_id=order_id).delete()

        # Puis supprimer la commande
        db.session.delete(order)
        db.session.commit()

        if request.is_json:
            return jsonify({'success': True, 'message': 'Commande supprimée avec succès'})
        else:
            flash('Commande supprimée avec succès!', 'success')
            return redirect(url_for('admin_orders'))

    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'error': 'Erreur lors de la suppression'})
        else:
            flash('Erreur lors de la suppression de la commande.', 'error')
            return redirect(url_for('admin_orders'))

@app.route('/admin/orders/delete_multiple', methods=['POST'])
@login_required
@admin_required
def admin_delete_multiple_orders():
    order_ids = request.json.get('order_ids', [])

    if not order_ids:
        return jsonify({'success': False, 'error': 'Aucune commande sélectionnée'})

    try:
        deleted_count = 0
        for order_id in order_ids:
            order = Order.query.get(order_id)
            if order:
                # Supprimer les items de la commande
                OrderItem.query.filter_by(order_id=order_id).delete()
                # Supprimer la commande
                db.session.delete(order)
                deleted_count += 1

        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'{deleted_count} commande(s) supprimée(s) avec succès'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Erreur lors de la suppression'})

@app.route('/admin/orders/<int:order_id>/print')
@login_required
@admin_required
def admin_print_order(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/print_order.html', order=order)

# Routes pour la gestion des sliders
@app.route('/admin/sliders')
@login_required
@admin_required
def admin_sliders():
    page = request.args.get('page', 1, type=int)
    sliders = Slider.query.order_by(Slider.order_position.asc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/sliders.html', sliders=sliders)

@app.route('/admin/sliders/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_slider():
    if request.method == 'POST':
        # Gestion de l'upload d'image
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                # Ajouter un timestamp pour éviter les conflits
                import time
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join('static/uploads/sliders', filename))
                image_filename = filename

        if not image_filename:
            flash('Une image est requise pour le slider.', 'error')
            return render_template('admin/add_slider.html')

        slider = Slider(
            title=request.form['title'],
            subtitle=request.form.get('subtitle', ''),
            description=request.form.get('description', ''),
            image_filename=image_filename,
            button_text=request.form.get('button_text', ''),
            button_link=request.form.get('button_link', ''),
            order_position=int(request.form.get('order_position', 0)),
            active='active' in request.form
        )
        db.session.add(slider)
        db.session.commit()
        flash('Slider ajouté avec succès!', 'success')
        return redirect(url_for('admin_sliders'))

    return render_template('admin/add_slider.html')

@app.route('/admin/sliders/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_slider(id):
    slider = Slider.query.get_or_404(id)

    if request.method == 'POST':
        # Gestion de l'upload d'image
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                # Supprimer l'ancienne image si elle existe
                if slider.image_filename:
                    old_path = os.path.join('static/uploads/sliders', slider.image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                filename = secure_filename(file.filename)
                import time
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join('static/uploads/sliders', filename))
                slider.image_filename = filename

        slider.title = request.form['title']
        slider.subtitle = request.form.get('subtitle', '')
        slider.description = request.form.get('description', '')
        slider.button_text = request.form.get('button_text', '')
        slider.button_link = request.form.get('button_link', '')
        slider.order_position = int(request.form.get('order_position', 0))
        slider.active = 'active' in request.form

        db.session.commit()
        flash('Slider modifié avec succès!', 'success')
        return redirect(url_for('admin_sliders'))

    return render_template('admin/edit_slider.html', slider=slider)

@app.route('/admin/sliders/delete/<int:id>')
@login_required
@admin_required
def admin_delete_slider(id):
    slider = Slider.query.get_or_404(id)

    # Supprimer l'image si elle existe
    if slider.image_filename:
        image_path = os.path.join('static/uploads/sliders', slider.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(slider)
    db.session.commit()
    flash('Slider supprimé avec succès!', 'success')
    return redirect(url_for('admin_sliders'))

@app.route('/admin/sliders/<int:slider_id>/move', methods=['POST'])
@login_required
@admin_required
def admin_move_slider(slider_id):
    slider = Slider.query.get_or_404(slider_id)
    direction = request.json.get('direction')

    if direction == 'up':
        # Trouver le slider précédent
        prev_slider = Slider.query.filter(Slider.order_position < slider.order_position).order_by(Slider.order_position.desc()).first()
        if prev_slider:
            # Échanger les positions
            slider.order_position, prev_slider.order_position = prev_slider.order_position, slider.order_position
            db.session.commit()
    elif direction == 'down':
        # Trouver le slider suivant
        next_slider = Slider.query.filter(Slider.order_position > slider.order_position).order_by(Slider.order_position.asc()).first()
        if next_slider:
            # Échanger les positions
            slider.order_position, next_slider.order_position = next_slider.order_position, slider.order_position
            db.session.commit()

    return jsonify({'success': True})

@app.route('/admin/sliders/<int:slider_id>/preview')
@login_required
@admin_required
def admin_preview_slider(slider_id):
    slider = Slider.query.get_or_404(slider_id)
    return jsonify({
        'success': True,
        'slider': {
            'id': slider.id,
            'title': slider.title,
            'subtitle': slider.subtitle,
            'description': slider.description,
            'image_url': slider.image_url,
            'button_text': slider.button_text,
            'button_link': slider.button_link
        }
    })

# Routes pour la gestion du footer
@app.route('/admin/footer', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_footer():
    settings = FooterSettings.get_settings()

    if request.method == 'POST':
        settings.company_name = request.form.get('company_name', '')
        settings.company_description = request.form.get('company_description', '')
        settings.address = request.form.get('address', '')
        settings.phone = request.form.get('phone', '')
        settings.email = request.form.get('email', '')
        settings.facebook_url = request.form.get('facebook_url', '')
        settings.instagram_url = request.form.get('instagram_url', '')
        settings.twitter_url = request.form.get('twitter_url', '')
        settings.linkedin_url = request.form.get('linkedin_url', '')
        settings.youtube_url = request.form.get('youtube_url', '')
        settings.opening_hours = request.form.get('opening_hours', '')
        settings.copyright_text = request.form.get('copyright_text', '')
        settings.show_newsletter = 'show_newsletter' in request.form
        settings.newsletter_title = request.form.get('newsletter_title', '')
        settings.newsletter_description = request.form.get('newsletter_description', '')

        db.session.commit()
        flash('Paramètres du footer mis à jour avec succès!', 'success')
        return redirect(url_for('admin_footer'))

    return render_template('admin/footer.html', settings=settings)

@app.route('/admin/telegram/test', methods=['POST'])
@login_required
@admin_required
def admin_test_telegram():
    """Test de la connexion Telegram"""
    try:
        success = test_telegram_connection()
        if success:
            return jsonify({'success': True, 'message': 'Message de test envoyé avec succès!'})
        else:
            return jsonify({'success': False, 'error': 'Échec de l\'envoi du message de test'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erreur: {str(e)}'})

@app.route('/admin/whatsapp/test', methods=['POST'])
@login_required
@admin_required
def admin_test_whatsapp():
    """Test de la connexion WhatsApp"""
    try:
        success = test_whatsapp_connection()
        if success:
            return jsonify({'success': True, 'message': 'Message de test WhatsApp envoyé avec succès!'})
        else:
            return jsonify({'success': False, 'error': 'Échec de l\'envoi du message de test WhatsApp'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erreur WhatsApp: {str(e)}'})

# Routes pour la gestion du logo
@app.route('/admin/logo', methods=['GET'])
@login_required
@admin_required
def admin_logo():
    """Page de gestion du logo"""
    return render_template('admin/logo.html')

@app.route('/admin/logo/upload', methods=['POST'])
@login_required
@admin_required
def admin_logo_upload():
    """Upload du nouveau logo"""
    try:
        import os
        from PIL import Image

        # Vérifier les fichiers uploadés
        logo_file = request.files.get('logo_file')
        favicon_file = request.files.get('favicon_file')

        if not logo_file:
            return jsonify({'success': False, 'error': 'Aucun fichier logo sélectionné'})

        # Créer les dossiers si nécessaire
        logo_dir = os.path.join('static', 'images', 'logo')
        favicon_dir = os.path.join('static', 'images', 'favicon')
        os.makedirs(logo_dir, exist_ok=True)
        os.makedirs(favicon_dir, exist_ok=True)

        # Traitement du logo principal
        if logo_file:
            # Vérifier l'extension
            filename = logo_file.filename.lower()
            if not filename.endswith(('.png', '.jpg', '.jpeg', '.svg')):
                return jsonify({'success': False, 'error': 'Format de fichier non supporté pour le logo'})

            # Sauvegarder le logo
            if filename.endswith('.svg'):
                logo_path = os.path.join(logo_dir, 'velours-logo.svg')
                logo_file.save(logo_path)
            else:
                # Convertir en PNG et redimensionner
                logo_path = os.path.join(logo_dir, 'velours-logo.png')

                # Ouvrir et traiter l'image
                img = Image.open(logo_file)

                # Convertir en RGBA si nécessaire
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                # Redimensionner en gardant les proportions
                img.thumbnail((400, 300), Image.Resampling.LANCZOS)

                # Sauvegarder
                img.save(logo_path, 'PNG', optimize=True)

        # Traitement du favicon
        if favicon_file and favicon_file.filename:
            filename = favicon_file.filename.lower()
            if filename.endswith(('.png', '.ico', '.jpg', '.jpeg')):
                favicon_path = os.path.join(favicon_dir, 'favicon.png')

                if filename.endswith('.ico'):
                    # Sauvegarder directement le ICO
                    ico_path = os.path.join(favicon_dir, 'favicon.ico')
                    favicon_file.save(ico_path)
                else:
                    # Traiter l'image
                    img = Image.open(favicon_file)

                    # Convertir en RGBA
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')

                    # Redimensionner à 64x64
                    img = img.resize((64, 64), Image.Resampling.LANCZOS)

                    # Sauvegarder
                    img.save(favicon_path, 'PNG', optimize=True)

                    # Créer aussi une version 32x32
                    img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
                    img_32.save(os.path.join(favicon_dir, 'favicon-32x32.png'), 'PNG', optimize=True)

                    # Créer une version 16x16
                    img_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
                    img_16.save(os.path.join(favicon_dir, 'favicon-16x16.png'), 'PNG', optimize=True)

        return jsonify({'success': True, 'message': 'Logo mis à jour avec succès!'})

    except Exception as e:
        return jsonify({'success': False, 'error': f'Erreur lors du téléchargement: {str(e)}'})

@app.route('/demo-3d')
def demo_3d():
    """Page de démonstration des effets 3D"""
    return render_template('demo_3d.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Créer un admin par défaut
        admin = User.query.filter_by(email='admin@bijoux.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@bijoux.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
    
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
