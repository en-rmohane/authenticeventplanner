from extensions import db
from flask_login import UserMixin
from datetime import datetime
import json

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    events = db.relationship('Event', backref='category', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    budget = db.Column(db.String(100))
    event_date = db.Column(db.Date)
    client_name = db.Column(db.String(100))
    featured_image = db.Column(db.String(255))
    gallery_images = db.Column(db.Text)  # JSON string
    video_link = db.Column(db.String(255))
    show_on_homepage = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_gallery(self):
        return json.loads(self.gallery_images) if self.gallery_images else []

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    is_video = db.Column(db.Boolean, default=False)
    caption = db.Column(db.String(200))

class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    event_type = db.Column(db.String(100))
    event_date = db.Column(db.Date)
    guest_count = db.Column(db.Integer)
    budget = db.Column(db.String(100))
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending') # Pending, Confirmed, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    event_name = db.Column(db.String(100))
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    image = db.Column(db.String(255))
