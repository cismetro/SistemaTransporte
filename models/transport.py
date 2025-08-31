from datetime import datetime
from models import db

class Transport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    
    # Dados da viagem
    origin = db.Column(db.String(200), default='UBS - Unidade Básica de Saúde')
    destination = db.Column(db.String(200), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)
    return_time = db.Column(db.Time)
    
    # Dados médicos
    medical_guide = db.Column(db.String(50))  # número da guia
    specialty = db.Column(db.String(100))  # consulta, exame, outro
    treatment_type = db.Column(db.String(50))  # radioterapia, quimioterapia, etc.
    treatment_sessions = db.Column(db.Integer)  # para tratamentos longos
    
    # Controle
    status = db.Column(db.String(20), default='agendado')  # agendado, em_andamento, concluido, cancelado
    km_start = db.Column(db.Integer)
    km_end = db.Column(db.Integer)
    observations = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Transport {self.id} - {self.patient.name}>'