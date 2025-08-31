from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os

# Configuração básica
app = Flask(__name__)
app.config['SECRET_KEY'] = 'transport-health-system-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/transport_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Criar diretório data se não existir
os.makedirs('data', exist_ok=True)

# Definir modelos diretamente aqui para evitar problemas de import
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(15))
    special_needs = db.Column(db.Text)
    priority_type = db.Column(db.String(20))

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

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(8), unique=True, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(30), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    ownership = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, default=4)
    has_wheelchair_access = db.Column(db.Boolean, default=False)
    has_stretcher = db.Column(db.Boolean, default=False)
    has_oxygen = db.Column(db.Boolean, default=False)
    current_km = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

class Transport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    origin = db.Column(db.String(200), default='UBS - Unidade Básica de Saúde')
    destination = db.Column(db.String(200), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)
    medical_guide = db.Column(db.String(50))
    specialty = db.Column(db.String(100))
    status = db.Column(db.String(20), default='agendado')
    observations = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

if __name__ == '__main__':
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        print("✅ Tabelas criadas!")
        
        # Criar usuário admin se não existir
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@transporte.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário admin criado!")
            print("   Login: admin")
            print("   Senha: admin123")
        else:
            print("ℹ️  Usuário admin já existe")
        
        print("🎉 Banco de dados configurado com sucesso!")