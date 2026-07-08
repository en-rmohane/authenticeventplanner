from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app, session
from extensions import db, bcrypt, mail
from models import Admin, Category, Event, Gallery, Enquiry, Testimonial
from forms import LoginForm, EnquiryForm, ContactForm, TestimonialForm, GalleryForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import os
import random
from werkzeug.utils import secure_filename
from datetime import datetime
import base64

main = Blueprint('main', __name__)

# Helper to convert upload file to base64 data url
def save_picture_base64(form_picture):
    file_data = form_picture.read()
    mime_type = form_picture.content_type or 'image/jpeg'
    base64_data = base64.b64encode(file_data).decode('utf-8')
    return f"data:{mime_type};base64,{base64_data}"

# Helper function for file uploads
def save_picture(form_picture, folder='uploads'):
    # Detect Vercel/serverless environments to directly use base64
    if os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV'):
        return save_picture_base64(form_picture)
        
    try:
        filename = secure_filename(form_picture.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{filename}"
        picture_path = os.path.join(current_app.root_path, 'static', folder, filename)
        os.makedirs(os.path.dirname(picture_path), exist_ok=True)
        form_picture.save(picture_path)
        return url_for('static', filename=folder + '/' + filename)
    except Exception as e:
        # Fallback to base64 if directory creation or file writing fails locally
        print(f"Local file write failed, falling back to base64 encoding: {e}")
        # Reset file stream position to start just in case it was partially read
        form_picture.seek(0)
        return save_picture_base64(form_picture)

# Helper function to send email notification
def send_enquiry_email(enquiry):
    try:
        msg = Message(
            subject=f"New Event Enquiry: {enquiry.event_type} - {enquiry.name}",
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@authenticevents.com'),
            recipients=[current_app.config.get('COMPANY_EMAIL', 'authenticeventplanner2410@gmail.com')],
            body=f"""
Dear Admin,

A new event booking enquiry has been submitted on the website.

--- ENQUIRY DETAILS ---
Name: {enquiry.name}
Email: {enquiry.email}
Phone: {enquiry.phone}
Event Type: {enquiry.event_type}
Event Date: {enquiry.event_date.strftime('%Y-%m-%d') if enquiry.event_date else 'Not Specified'}
Number of Guests: {enquiry.guest_count if enquiry.guest_count else 'Not Specified'}
Budget Range: {enquiry.budget if enquiry.budget else 'Not Specified'}

Message:
{enquiry.message}

-----------------------
Log in to the Admin Panel to change the status of this enquiry.

Best regards,
Authentic Event Planner Automated System
"""
        )
        mail.send(msg)
    except Exception as e:
        # Keep app running even if mail server is not configured in local environment
        print(f"Mail notification failed: {e}")

# Helper to generate/regenerate math captcha
def generate_captcha():
    n1 = random.randint(1, 9)
    n2 = random.randint(1, 9)
    session['captcha_n1'] = n1
    session['captcha_n2'] = n2
    session['captcha_sum'] = n1 + n2

# --- Frontend Routes ---

@main.route("/")
@main.route("/home")
def home():
    categories = Category.query.all()
    # Featured events from gallery/portfolio
    featured_events = Gallery.query.limit(6).all()
    testimonials = Testimonial.query.order_by(Testimonial.id.desc()).limit(3).all()
    
    # Stats counter static inputs (dynamically passed to template)
    stats = {
        'events_completed': 850,
        'happy_clients': 820,
        'experience_years': 12
    }
    
    return render_template('index.html', categories=categories, featured_events=featured_events, testimonials=testimonials, stats=stats)

@main.route("/about")
def about():
    return render_template('about.html', title='About Us')

@main.route("/services")
def services():
    categories = Category.query.all()
    return render_template('services.html', title='Our Services', categories=categories)

@main.route("/gallery")
def gallery():
    media = Gallery.query.all()
    categories = Category.query.all()
    return render_template('gallery.html', title='Gallery', media=media, categories=categories)

@main.route("/booking", methods=['GET', 'POST'])
def booking():
    form = EnquiryForm()
    
    # Generate captcha question if not post or failed validation
    if request.method == 'GET':
        generate_captcha()
        
    if form.validate_on_submit():
        # Validate captcha
        if form.captcha.data != session.get('captcha_sum'):
            form.captcha.errors.append("Incorrect verification answer. Try again.")
            generate_captcha()
            return render_template('booking.html', title='Book Now', form=form)
            
        enquiry = Enquiry(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            event_type=form.event_type.data,
            event_date=form.event_date.data,
            guest_count=form.guest_count.data,
            budget=form.budget.data,
            message=form.message.data,
            status='Pending'
        )
        db.session.add(enquiry)
        db.session.commit()
        
        # Send Email notification
        send_enquiry_email(enquiry)
        
        flash('Thank you! Your event booking enquiry has been submitted. We will contact you shortly.', 'success')
        return redirect(url_for('main.booking'))
        
    return render_template('booking.html', title='Book Now', form=form)

@main.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if request.method == 'GET':
        generate_captcha()
        
    if form.validate_on_submit():
        if form.captcha.data != session.get('captcha_sum'):
            form.captcha.errors.append("Incorrect verification answer. Try again.")
            generate_captcha()
            return render_template('contact.html', title='Contact Us', form=form)
            
        # Create a booking/enquiry structure for contact submission
        enquiry = Enquiry(
            name=form.name.data,
            email=form.email.data,
            phone="Not Provided",
            event_type="General Enquiry",
            message=f"Subject: {form.subject.data}\n\n{form.message.data}",
            status='Pending'
        )
        db.session.add(enquiry)
        db.session.commit()
        
        # Send mail notification
        send_enquiry_email(enquiry)
        
        flash('Your message has been sent successfully! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
        
    return render_template('contact.html', title='Contact Us', form=form)

@main.route("/testimonials")
def testimonials():
    reviews = Testimonial.query.order_by(Testimonial.id.desc()).all()
    return render_template('testimonials.html', title='Client Testimonials', reviews=reviews)

# --- Admin Panel Routes ---

@main.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('admin/login.html', title='Admin Login', form=form)

@main.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route("/admin/dashboard")
@login_required
def admin_dashboard():
    enquiries_count = Enquiry.query.count()
    gallery_count = Gallery.query.count()
    testimonials_count = Testimonial.query.count()
    recent_enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', title='Admin Dashboard', 
                           enquiries_count=enquiries_count, gallery_count=gallery_count, 
                           testimonials_count=testimonials_count, recent_enquiries=recent_enquiries)

@main.route("/admin/enquiries")
@login_required
def admin_enquiries():
    enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).all()
    return render_template('admin/enquiries.html', title='Manage Enquiries', enquiries=enquiries)

@main.route("/admin/enquiry/<int:enquiry_id>/status/<string:status>")
@login_required
def update_enquiry_status(enquiry_id, status):
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    if status in ['Pending', 'Confirmed', 'Completed']:
        enquiry.status = status
        db.session.commit()
        flash(f'Enquiry status updated to {status}', 'success')
    else:
        flash('Invalid status action.', 'danger')
    return redirect(url_for('main.admin_enquiries'))

@main.route("/admin/enquiry/<int:enquiry_id>/delete")
@login_required
def delete_enquiry(enquiry_id):
    enquiry = Enquiry.query.get_or_404(enquiry_id)
    db.session.delete(enquiry)
    db.session.commit()
    flash('Enquiry deleted successfully.', 'success')
    return redirect(url_for('main.admin_enquiries'))

@main.route("/admin/gallery", methods=['GET', 'POST'])
@login_required
def admin_gallery():
    form = GalleryForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        if form.image.data:
            img_path = save_picture(form.image.data)
            media = Gallery(
                image_path=img_path,
                category_id=form.category_id.data,
                is_video=form.is_video.data,
                caption=form.caption.data
            )
            db.session.add(media)
            db.session.commit()
            flash('Gallery media item added successfully!', 'success')
            return redirect(url_for('main.admin_gallery'))
    
    media = Gallery.query.order_by(Gallery.id.desc()).all()
    return render_template('admin/gallery.html', title='Manage Gallery', form=form, media=media)

@main.route("/admin/gallery/<int:item_id>/delete")
@login_required
def delete_gallery_item(item_id):
    item = Gallery.query.get_or_404(item_id)
    # If the image was uploaded locally, delete the file too
    if 'uploads/' in item.image_path:
        filename = item.image_path.split('/')[-1]
        file_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing local gallery file: {e}")
    db.session.delete(item)
    db.session.commit()
    flash('Gallery item has been deleted.', 'success')
    return redirect(url_for('main.admin_gallery'))

@main.route("/admin/testimonials", methods=['GET', 'POST'])
@login_required
def admin_testimonials():
    form = TestimonialForm()
    if form.validate_on_submit():
        img_file = None
        if form.image.data:
            img_file = save_picture(form.image.data)
            
        testimonial = Testimonial(
            name=form.name.data,
            city=form.city.data,
            event_name=form.event_name.data,
            text=form.text.data,
            rating=form.rating.data,
            image=url_for('static', filename='uploads/' + img_file) if img_file else None
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial added successfully!', 'success')
        return redirect(url_for('main.admin_testimonials'))
        
    testimonials = Testimonial.query.order_by(Testimonial.id.desc()).all()
    return render_template('admin/testimonials.html', title='Manage Testimonials', form=form, testimonials=testimonials)

@main.route("/admin/testimonials/<int:item_id>/delete")
@login_required
def delete_testimonial(item_id):
    item = Testimonial.query.get_or_404(item_id)
    if item.image and 'uploads/' in item.image:
        filename = item.image.split('/')[-1]
        file_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing testimonial image file: {e}")
    db.session.delete(item)
    db.session.commit()
    flash('Testimonial has been deleted.', 'success')
    return redirect(url_for('main.admin_testimonials'))
