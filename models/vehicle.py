from datetime import datetime
from models import db

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(8), unique=True, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(30), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    ownership = db.Column(db.String(20), nullable=False)  # proprio, alugado
    capacity = db.Column(db.Integer, default=4)
    has_wheelchair_access = db.Column(db.Boolean, default=False)
    has_stretcher = db.Column(db.Boolean, default=False)
    has_oxygen = db.Column(db.Boolean, default=False)
    current_km = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    transports = db.relationship('Transport', backref='vehicle', lazy=True)
    
    def __repr__(self):
        return f'<Vehicle {self.plate}>'