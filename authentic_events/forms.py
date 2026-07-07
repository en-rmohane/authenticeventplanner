from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, DateField, FileField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class EnquiryForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    event_type = SelectField('Event Type', choices=[
        ('Wedding', 'Wedding Decoration & Planning'),
        ('Birthday', 'Birthday Party Decoration'),
        ('Corporate', 'Corporate Event Management'),
        ('Engagement', 'Engagement Event Planning'),
        ('Baby Shower', 'Baby Shower Decoration'),
        ('Anniversary', 'Anniversary Celebration'),
        ('Festival', 'Festival Decoration'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    event_date = DateField('Event Date', validators=[Optional()])
    guest_count = IntegerField('Number of Guests', validators=[DataRequired()])
    budget = StringField('Budget Range', validators=[Optional()])
    message = TextAreaField('Your Message', validators=[DataRequired()])
    captcha = IntegerField('Verification Answer', validators=[DataRequired()])

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(max=200)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    budget = StringField('Budget', validators=[Optional()])
    event_date = DateField('Event Date', validators=[Optional()])
    client_name = StringField('Client Name', validators=[Optional()])
    featured_image = FileField('Featured Image')
    gallery_images = FileField('Gallery Images (Multiple)', render_kw={'multiple': True})
    video_link = StringField('Video Link (YouTube)', validators=[Optional()])
    show_on_homepage = BooleanField('Show on Homepage')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    image = FileField('Category Image')

class TestimonialForm(FlaskForm):
    name = StringField('Client Name', validators=[DataRequired()])
    city = StringField('City', validators=[Optional()])
    event_name = StringField('Event Name', validators=[Optional()])
    text = TextAreaField('Testimonial Text', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], coerce=int)
    image = FileField('Client Photo')

class GalleryForm(FlaskForm):
    image = FileField('Media File', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    is_video = BooleanField('Is this a Video?')
    caption = StringField('Caption', validators=[Optional()])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=100)])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired()])
    captcha = IntegerField('Verification Answer', validators=[DataRequired()])
