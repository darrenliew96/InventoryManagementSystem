from ..extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String, nullable=False)
    password_last_changed = db.Column(db.Date, default=datetime.utcnow)
    email = db.Column(db.String(100), unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    user_type = db.Column(db.String, default="administrator")
    is_deleted = db.Column(db.Boolean, default=False)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    modified_at= db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at= db.Column(db.DateTime)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String)
    password_last_changed = db.Column(db.Date, default=datetime.utcnow)
    sex = db.Column(db.String)
    age = db.Column(db.Integer)
    new_ic = db.Column(db.String)
    old_ic = db.Column(db.String)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    email = db.Column(db.String(100), unique=True)
    underlying_issue = db.Column(db.String)
    current_issue = db.Column(db.String)
    diagnosis = db.Column(db.String)
    user_type = db.Column(db.String, default="patient")
    is_deleted = db.Column(db.Boolean, default=False)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    modified_at= db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at= db.Column(db.DateTime)


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String)
    sex = db.Column(db.String)
    age = db.Column(db.Integer)
    new_ic = db.Column(db.String)
    old_ic = db.Column(db.String)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"))
    shop_name = db.Column(db.String)
    shop_location = db.Column(db.String)
    email = db.Column(db.String(100), unique=True)
    password_last_changed = db.Column(db.Date, default=datetime.utcnow)
    user_type = db.Column(db.String, default="agent")
    is_deleted = db.Column(db.Boolean, default=False)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    modified_at= db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at= db.Column(db.DateTime)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_line1 = db.Column(db.String)
    address_line2 = db.Column(db.String)
    postal_code = db.Column(db.String)
    country = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    phone_number = db.Column(db.String)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    modified_at= db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at= db.Column(db.DateTime)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String)
    mobile_number = db.Column(db.String)
    whatsapp_number = db.Column(db.String)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    modified_at= db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at= db.Column(db.DateTime)
