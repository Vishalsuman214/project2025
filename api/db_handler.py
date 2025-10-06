from werkzeug.security import generate_password_hash, check_password_hash
from api.models import db, User, Reminder
import uuid
import datetime

def read_users():
    return User.query.all()

def write_users(users):
    # Not needed, as we use db.session.add/commit
    pass

def add_user(email, password):
    existing = User.query.filter_by(email=email).first()
    if existing:
        return None
    user_id = str(uuid.uuid4())
    password_hash = generate_password_hash(password)
    new_user = User(
        id=user_id,
        email=email,
        password_hash=password_hash,
        is_email_confirmed=True,  # Default to True
        verification_token='',
        reset_token='',
        reset_token_expiry=None,
        profile_picture='',
        bio='',
        email_credentials='',
        app_password=''
    )
    db.session.add(new_user)
    db.session.commit()
    return user_id

def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return {
            'id': user.id,
            'email': user.email,
            'password_hash': user.password_hash,
            'is_email_confirmed': user.is_email_confirmed,
            'verification_token': user.verification_token,
            'reset_token': user.reset_token,
            'reset_token_expiry': user.reset_token_expiry,
            'profile_picture': user.profile_picture,
            'bio': user.bio,
            'email_credentials': user.email_credentials,
            'app_password': user.app_password
        }
    return None

def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return {
            'id': user.id,
            'email': user.email,
            'password_hash': user.password_hash,
            'is_email_confirmed': user.is_email_confirmed,
            'verification_token': user.verification_token,
            'reset_token': user.reset_token,
            'reset_token_expiry': user.reset_token_expiry,
            'profile_picture': user.profile_picture,
            'bio': user.bio,
            'email_credentials': user.email_credentials,
            'app_password': user.app_password
        }
    return None

def update_user_password(user_id, new_password_hash):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.password_hash = new_password_hash
        db.session.commit()
        return True
    return False

def update_user_profile_picture(user_id, filename):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.profile_picture = filename
        db.session.commit()
        return True
    return False

def update_user_bio(user_id, bio):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.bio = bio
        db.session.commit()
        return True
    return False

def update_user_email_credentials(user_id, email, app_password):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.email_credentials = email
        user.app_password = app_password
        db.session.commit()
        return True
    return False

def update_user_reminder_email(user_id, email):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.email_credentials = email  # Assuming this is for reminders
        db.session.commit()
        return True
    return False

def update_user_reminder_app_password(user_id, app_password):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.app_password = app_password
        db.session.commit()
        return True
    return False

def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)

# Stub functions for removed email verification features
def generate_verification_token(email):
    return str(uuid.uuid4())

def set_verification_token(user_id, token):
    pass

def verify_email(token):
    return True

def generate_reset_token(email):
    return str(uuid.uuid4())

def set_reset_token(user_id, token, expiry):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.reset_token = token
        user.reset_token_expiry = expiry
        db.session.commit()
        return True
    return False

def reset_password(token, new_password):
    user = User.query.filter_by(reset_token=token).first()
    if user:
        user.password_hash = generate_password_hash(new_password)
        user.reset_token = ''
        user.reset_token_expiry = None
        db.session.commit()
        return True
    return False

# Reminder functions
def get_all_reminders():
    reminders = Reminder.query.all()
    return [
        {
            'id': r.id,
            'user_id': r.user_id,
            'title': r.title,
            'description': r.description,
            'reminder_time': r.reminder_time.strftime('%Y-%m-%d %H:%M:%S'),
            'recipient_email': r.recipient_email,
            'is_completed': r.is_completed
        }
        for r in reminders
    ]

def mark_reminder_completed(reminder_id):
    reminder = Reminder.query.filter_by(id=reminder_id).first()
    if reminder:
        reminder.is_completed = True
        db.session.commit()
        return True
    return False

def add_reminder(user_id, title, description, reminder_time, recipient_email):
    reminder_id = str(uuid.uuid4())
    new_reminder = Reminder(
        id=reminder_id,
        user_id=user_id,
        title=title,
        description=description,
        reminder_time=datetime.datetime.fromisoformat(reminder_time),
        recipient_email=recipient_email,
        is_completed=False
    )
    db.session.add(new_reminder)
    db.session.commit()
    return reminder_id

def get_reminders_by_user_id(user_id):
    reminders = Reminder.query.filter_by(user_id=user_id).all()
    return [
        {
            'id': r.id,
            'user_id': r.user_id,
            'title': r.title,
            'description': r.description,
            'reminder_time': r.reminder_time.strftime('%Y-%m-%d %H:%M:%S'),
            'recipient_email': r.recipient_email,
            'is_completed': r.is_completed
        }
        for r in reminders
    ]

def get_reminder_by_id(reminder_id):
    reminder = Reminder.query.filter_by(id=reminder_id).first()
    if reminder:
        return {
            'id': reminder.id,
            'user_id': reminder.user_id,
            'title': reminder.title,
            'description': reminder.description,
            'reminder_time': reminder.reminder_time.strftime('%Y-%m-%d %H:%M:%S'),
            'recipient_email': reminder.recipient_email,
            'is_completed': reminder.is_completed
        }
    return None

def update_reminder(reminder_id, title=None, description=None, reminder_time=None, recipient_email=None, is_completed=None):
    reminder = Reminder.query.filter_by(id=reminder_id).first()
    if reminder:
        if title is not None:
            reminder.title = title
        if description is not None:
            reminder.description = description
        if reminder_time is not None:
            reminder.reminder_time = datetime.datetime.fromisoformat(reminder_time)
        if recipient_email is not None:
            reminder.recipient_email = recipient_email
        if is_completed is not None:
            reminder.is_completed = is_completed
        db.session.commit()
        return True
    return False

def delete_reminder(reminder_id):
    reminder = Reminder.query.filter_by(id=reminder_id).first()
    if reminder:
        db.session.delete(reminder)
        db.session.commit()
        return True
    return False
