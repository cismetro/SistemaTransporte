import os
import sqlite3
from werkzeug.security import generate_password_hash

# Criar diretório data se não existir
os.makedirs('data', exist_ok=True)

# Caminho do banco
db_path = 'data/transport_system.db'

# Remover banco antigo se existir (para recomeçar limpo)
if os.path.exists(db_path):
    os.remove(db_path)
    print("🗑️  Banco antigo removido")

# Conectar ao SQLite e criar tabelas
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("📅 Criando tabelas...")

# Criar tabela de usuários
cursor.execute('''
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT 1
)
''')

# Criar tabela de pacientes
cursor.execute('''
CREATE TABLE patient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    emergency_contact VARCHAR(100),
    emergency_phone VARCHAR(15),
    special_needs TEXT,
    priority_type VARCHAR(20)
)
''')

# Criar tabela de motoristas
cursor.execute('''
CREATE TABLE driver (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    cnh VARCHAR(20) UNIQUE NOT NULL,
    cnh_category VARCHAR(5) NOT NULL,
    cnh_expiry DATE NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    hire_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT 1
)
''')

# Criar tabela de veículos
cursor.execute('''
CREATE TABLE vehicle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate VARCHAR(8) UNIQUE NOT NULL,
    model VARCHAR(50) NOT NULL,
    brand VARCHAR(30) NOT NULL,
    year INTEGER NOT NULL,
    ownership VARCHAR(20) NOT NULL,
    capacity INTEGER DEFAULT 4,
    has_wheelchair_access BOOLEAN DEFAULT 0,
    has_stretcher BOOLEAN DEFAULT 0,
    has_oxygen BOOLEAN DEFAULT 0,
    current_km INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1
)
''')

# Criar tabela de transportes
cursor.execute('''
CREATE TABLE transport (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    driver_id INTEGER,
    vehicle_id INTEGER,
    origin VARCHAR(200) DEFAULT 'UBS - Unidade Básica de Saúde',
    destination VARCHAR(200) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME,
    departure_time TIME,
    medical_guide VARCHAR(50),
    specialty VARCHAR(100),
    status VARCHAR(20) DEFAULT 'agendado',
    observations TEXT,
    created_by INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patient (id),
    FOREIGN KEY (driver_id) REFERENCES driver (id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicle (id),
    FOREIGN KEY (created_by) REFERENCES user (id)
)
''')

print("✅ Tabelas criadas!")

# Criar usuário admin
password_hash = generate_password_hash('admin123')
cursor.execute('''
INSERT INTO user (username, email, password_hash, role)
VALUES (?, ?, ?, ?)
''', ('admin', 'admin@transporte.com', password_hash, 'admin'))

print("✅ Usuário admin criado!")
print("   Login: admin")
print("   Senha: admin123")

# Salvar e fechar
conn.commit()
conn.close()

print("🎉 Banco de dados criado com sucesso em:", db_path)