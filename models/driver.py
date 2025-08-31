from datetime import datetime
from models import db

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    cnh = db.Column(db.String(20), unique=True, nullable=False)
    cnh_category = db.Column(db.String(5), nullable=False)
    cnh_expiry = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    hire_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    transports = db.relationship('Transport', backref='driver', lazy=True)
    
    def __repr__(self):
        return f'<Driver {self.name}>'