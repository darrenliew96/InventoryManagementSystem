from ..extensions import db
from datetime import datetime

class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String)
    url = db.Column(db.String)
    path = db.Column(db)
    type = db.Column(db.String)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    modified_at= db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at= db.Column(db.DateTime)
