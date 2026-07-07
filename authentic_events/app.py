from flask import Flask, render_template
from extensions import db, bcrypt, login_manager, mail
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Use database URL from environment (e.g. Postgres) or fall back to SQLite
    if os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        # Detect if running in Vercel serverless environment
        if os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV'):
            db_path = '/tmp/site.db'
        else:
            basedir = os.path.abspath(os.path.dirname(__file__))
            db_path = os.path.join(basedir, 'instance', 'site.db')
            
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    
    # Ensure database path directory exists if SQLite
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if db_uri.startswith('sqlite:///'):
        db_file = db_uri.replace('sqlite:///', '')
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        
    # Ensure uploads path directories exist locally (only if not on Vercel)
    if not (os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV')):
        basedir = os.path.abspath(os.path.dirname(__file__))
        os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
        os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)
        os.makedirs(os.path.join(app.root_path, 'static', 'images'), exist_ok=True)

    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from routes import main
    app.register_blueprint(main)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    # Run auto-initialization and seeding of the database
    initialize_database(app)

    return app

def initialize_database(app):
    with app.app_context():
        from models import Admin, Category, Testimonial, Gallery
        db.create_all()
        
        # Create default admin if not exists
        if not Admin.query.filter_by(username='admin').first():
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = Admin(username='admin', password_hash=hashed_password)
            db.session.add(admin)
            
        # Create default categories if none exist
        if not Category.query.first():
            categories_data = [
                ('Weddings', 'wedding', 'Elegant and royal setups for your dream day.'),
                ('Birthdays', 'birthday', 'Vibrant and fun theme-based party decorations.'),
                ('Corporate Events', 'corporate', 'Professional planning and decor for corporate functions.'),
                ('Engagements', 'engagement', 'Romantic settings for your ring ceremony.'),
                ('Baby Showers', 'babyshower', 'Sweet, pastel setups for welcoming your little bundle of joy.'),
                ('Anniversaries', 'anniversary', 'Intimate and timeless setups celebrating years of togetherness.'),
                ('Festivals', 'festival', 'Traditional and festive decorations for special occasions.')
            ]
            for name, slug, desc in categories_data:
                cat = Category(name=name, slug=slug, description=desc)
                db.session.add(cat)
                
        # Add default testimonials if empty
        if Testimonial.query.count() == 0:
            testimonials = [
                Testimonial(
                    name="Aishwarya Sharma", 
                    city="Delhi", 
                    event_name="Wedding Decor", 
                    text="The decoration was absolutely royal! Everyone was mesmerized by the beautiful floral entry and stage decor. Thank you Authentic Events!", 
                    rating=5
                ),
                Testimonial(
                    name="Rohan Gupta", 
                    city="Mumbai", 
                    event_name="1st Birthday Party", 
                    text="Wonderful jungle theme decoration for my son's birthday. The kids loved the photo booth and balloon arches. Meticulous planning!", 
                    rating=5
                ),
                Testimonial(
                    name="Priya Patel", 
                    city="Bangalore", 
                    event_name="Corporate Gala", 
                    text="Authentic Event Planner handles our corporate award show decor every year. Professional, punctual, and highly creative layouts.", 
                    rating=4
                )
            ]
            for t in testimonials:
                db.session.add(t)

        # Add default gallery items if empty
        if Gallery.query.count() == 0:
            gallery_items = [
                Gallery(image_path="https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&q=80&w=800", category_id=1, caption="Luxury Floral Wedding Stage Setup"),
                Gallery(image_path="https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&q=80&w=800", category_id=2, caption="Jungle Theme Birthday Party Decor"),
                Gallery(image_path="https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&q=80&w=800", category_id=3, caption="Corporate Conference Grand Stage"),
                Gallery(image_path="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=800", category_id=1, caption="Royal Mandap Backdrop"),
                Gallery(image_path="https://images.unsplash.com/photo-1502635385003-ee1e6a1a742d?auto=format&fit=crop&q=80&w=800", category_id=4, caption="Elegant Ring Ceremony Stage"),
                Gallery(image_path="https://images.unsplash.com/photo-1530103862676-de8c9debad1d?auto=format&fit=crop&q=80&w=800", category_id=5, caption="Pastel Themed Baby Shower")
            ]
            for item in gallery_items:
                db.session.add(item)
                
        db.session.commit()

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.query.get(int(user_id))

# Database initialization command
@app.cli.command("init-db")
def init_db():
    initialize_database(app)
    print("Database initialized successfully!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)