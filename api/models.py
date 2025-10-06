from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_email_confirmed = db.Column(db.Boolean, default=True)
    verification_token = db.Column(db.String(128))
    reset_token = db.Column(db.String(128))
    reset_token_expiry = db.Column(db.DateTime)
    profile_picture = db.Column(db.String(256))
    bio = db.Column(db.Text)
    email_credentials = db.Column(db.String(256))
    app_password = db.Column(db.String(256))

class Reminder(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    reminder_time = db.Column(db.DateTime, nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
