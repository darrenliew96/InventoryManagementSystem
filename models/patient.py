from ..extensions import db
from datetime import datetime

class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientName = db.Column(db.String(100))
    patientPassword = db.Column(db.String)
    patientEmail = db.Column(db.String(100), unique=True)
    patientJoinedDate = db.Column(db.Date, default=datetime.utcnow)