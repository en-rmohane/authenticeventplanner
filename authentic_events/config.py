import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration."""

    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///authentic_events.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for debugging SQL queries

    # File Upload Configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Session Configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Email Configuration (for contact form)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@authenticevents.com'

    # Company Information
    COMPANY_NAME = "Authentic Event Decoration and Planner"
    COMPANY_SLOGAN = "Creating Memorable Events Across India"
    COMPANY_EMAIL = "authenticeventplanner2410@gmail.com"
    COMPANY_PHONE = "+91 88151 57953"
    COMPANY_WHATSAPP = "+918815157953"
    COMPANY_ADDRESS = "Shop No. 9, Indraprasth Colony, Hinotiya Chanbad, Bhopal - 462010"
    COMPANY_WORKING_HOURS = "Mon-Sun: 9:00 AM - 9:00 PM"
    COMPANY_EMERGENCY_CONTACT = "+91 88151 57953 (24/7)"

    # Social Media Links
    SOCIAL_MEDIA = {
        'facebook': 'https://facebook.com/authenticevents',
        'instagram': 'https://instagram.com/authentic_events',
        'twitter': 'https://twitter.com/authenticevents',
        'pinterest': 'https://pinterest.com/authenticevents',
        'youtube': 'https://youtube.com/authenticevents'
    }

    # Pricing Configuration
    PRICING_CONFIG = {
        'city_multipliers': {
            'metro': 1.5,
            'tier2': 1.2,
            'tier3': 1.0,
            'local': 0.7
        },
        'base_prices': {
            'wedding': {
                'basic': 50000,
                'standard': 80000,
                'premium': 150000
            },
            'corporate': {
                'basic': 30000,
                'standard': 50000,
                'premium': 100000
            },
            'birthday': {
                'basic': 20000,
                'standard': 35000,
                'premium': 60000
            },
            'festival': {
                'basic': 15000,
                'standard': 25000,
                'premium': 40000
            },
            'home': {
                'basic': 10000,
                'standard': 20000,
                'premium': 35000
            }
        },
        'material_grades': {
            'premium': {
                'multiplier': 1.5,
                'description': 'Imported/High-end materials, intricate designs'
            },
            'standard': {
                'multiplier': 1.0,
                'description': 'Good quality materials, beautiful designs'
            },
            'economy': {
                'multiplier': 0.7,
                'description': 'Budget-friendly materials, decent quality'
            }
        }
    }

    # Service Categories
    SERVICE_CATEGORIES = {
        'wedding': 'Wedding Decoration',
        'corporate': 'Corporate Events',
        'birthday': 'Birthday Parties',
        'festival': 'Festival Decor',
        'home': 'Home Decorations'
    }

    # City Classification
    CITIES = {
        'metro': [
            'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai',
            'Kolkata', 'Pune', 'Ahmedabad', 'Surat', 'Jaipur'
        ],
        'tier2': [
            'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane',
            'Bhopal', 'Visakhapatnam', 'Pimpri-Chinchwad', 'Patna', 'Vadodara'
        ],
        'tier3': [
            'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik', 'Faridabad',
            'Meerut', 'Rajkot', 'Kalyan-Dombivli', 'Vasai-Virar', 'Varanasi'
        ]
    }

    # Event Types
    EVENT_TYPES = [
        ('wedding', 'Wedding Ceremony'),
        ('reception', 'Wedding Reception'),
        ('engagement', 'Engagement'),
        ('birthday', 'Birthday Party'),
        ('corporate', 'Corporate Event'),
        ('festival', 'Festival Celebration'),
        ('home', 'Home/Private Party'),
        ('other', 'Other')
    ]

    # Budget Ranges
    BUDGET_RANGES = [
        ('25-50', '₹25,000 - ₹50,000'),
        ('50-75', '₹50,000 - ₹75,000'),
        ('75-100', '₹75,000 - ₹1,00,000'),
        ('100-150', '₹1,00,000 - ₹1,50,000'),
        ('150-200', '₹1,50,000 - ₹2,00,000'),
        ('200+', '₹2,00,000+')
    ]

    # Default Pagination
    ITEMS_PER_PAGE = 12
    PORTFOLIO_PER_PAGE = 9
    BLOG_PER_PAGE = 6

    # Cache Configuration
    CACHE_TYPE = 'simple'  # Use 'redis' or 'memcached' in production
    CACHE_DEFAULT_TIMEOUT = 300

    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block'
    }

    # SEO Configuration
    SITE_TITLE = "Authentic Event Decoration and Planner - Premium Event Services Across India"
    SITE_DESCRIPTION = "Professional event decoration services for weddings, corporate events, birthday parties, festivals across India. City-appropriate pricing."
    SITE_KEYWORDS = "event decoration, wedding planner, corporate events, birthday decoration, festival decor, authentic events"
    SITE_AUTHOR = "Authentic Event Decoration and Planner"

    # Google Analytics (Add your tracking ID)
    GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', '')

    # Google Maps API (for contact page)
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    TESTING = False

    # Development database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

    # Enable SQL query logging
    SQLALCHEMY_ECHO = True

    # Disable cache in development
    CACHE_TYPE = 'null'

    # Allow less secure settings for development
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    """Testing configuration."""

    DEBUG = False
    TESTING = True

    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Disable CSRF protection in testing
    WTF_CSRF_ENABLED = False

    # Disable mail sending
    MAIL_SUPPRESS_SEND = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False

    # Production database (PostgreSQL recommended)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/authentic_events'

    # Secure session cookies (requires HTTPS)
    SESSION_COOKIE_SECURE = True

    # Production cache (Redis recommended)
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

    # Strict security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
    }

    # Logging configuration
    LOG_LEVEL = 'WARNING'
    LOG_FILE = 'logs/authentic_events.log'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


# Helper functions
def get_city_type(city_name):
    """Determine city type based on city name."""
    city_lower = city_name.lower().strip()

    metro_cities = [city.lower() for city in Config.CITIES['metro']]
    tier2_cities = [city.lower() for city in Config.CITIES['tier2']]
    tier3_cities = [city.lower() for city in Config.CITIES['tier3']]

    if city_lower in metro_cities:
        return 'metro'
    elif city_lower in tier2_cities:
        return 'tier2'
    elif city_lower in tier3_cities:
        return 'tier3'
    else:
        return 'local'


def calculate_quote(city_type, event_type, package_level='standard', material_grade='standard'):
    """Calculate estimated quote based on parameters."""
    if event_type not in Config.PRICING_CONFIG['base_prices']:
        event_type = 'wedding'  # Default

    if package_level not in ['basic', 'standard', 'premium']:
        package_level = 'standard'

    if material_grade not in ['economy', 'standard', 'premium']:
        material_grade = 'standard'

    if city_type not in Config.PRICING_CONFIG['city_multipliers']:
        city_type = 'local'

    base_price = Config.PRICING_CONFIG['base_prices'][event_type][package_level]
    city_multiplier = Config.PRICING_CONFIG['city_multipliers'][city_type]
    material_multiplier = Config.PRICING_CONFIG['material_grades'][material_grade]['multiplier']

    estimated_price = base_price * city_multiplier * material_multiplier

    # Round to nearest 1000
    return round(estimated_price / 1000) * 1000


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def format_currency(amount):
    """Format amount as Indian currency."""
    return f"₹{amount:,.0f}"


def get_social_links():
    """Get social media links for templates."""
    return {platform: url for platform, url in Config.SOCIAL_MEDIA.items() if url}


# Export commonly used configurations
COMPANY_NAME = Config.COMPANY_NAME
COMPANY_SLOGAN = Config.COMPANY_SLOGAN
COMPANY_PHONE = Config.COMPANY_PHONE
COMPANY_WHATSAPP = Config.COMPANY_WHATSAPP
COMPANY_EMAIL = Config.COMPANY_EMAIL
SITE_TITLE = Config.SITE_TITLE
SITE_DESCRIPTION = Config.SITE_DESCRIPTION