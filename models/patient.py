from datetime import datetime
from models import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(15))
    special_needs = db.Column(db.Text)  # wheelchair, oxygen, etc.
    priority_type = db.Column(db.String(20))  # idoso, gestante, criança_autista
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    transports = db.relationship('Transport', backref='patient', lazy=True)
    
    def __repr__(self):
        return f'<Patient {self.name}>'