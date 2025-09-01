import sqlite3
import os

# Caminho do banco
db_path = 'data/transport_system.db'

if not os.path.exists(db_path):
    print("❌ Banco de dados não encontrado!")
    exit(1)

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔄 Atualizando estrutura do banco de dados...")

try:
    # Adicionar novos campos na tabela patient
    cursor.execute('ALTER TABLE patient ADD COLUMN appointment_date DATE')
    print("✅ Campo appointment_date adicionado")
except:
    print("ℹ️  Campo appointment_date já existe")

try:
    cursor.execute('ALTER TABLE patient ADD COLUMN attendant_name VARCHAR(100)')
    print("✅ Campo attendant_name adicionado")
except:
    print("ℹ️  Campo attendant_name já existe")

try:
    cursor.execute('ALTER TABLE patient ADD COLUMN destination VARCHAR(200)')
    print("✅ Campo destination adicionado")
except:
    print("ℹ️  Campo destination já existe")

try:
    cursor.execute('ALTER TABLE patient ADD COLUMN appointment_time TIME')
    print("✅ Campo appointment_time adicionado")
except:
    print("ℹ️  Campo appointment_time já existe")

try:
    cursor.execute('ALTER TABLE patient ADD COLUMN specialty VARCHAR(150)')
    print("✅ Campo specialty adicionado")
except:
    print("ℹ️  Campo specialty já existe")

try:
    cursor.execute('ALTER TABLE patient ADD COLUMN has_companion BOOLEAN DEFAULT 0')
    print("✅ Campo has_companion adicionado")
except:
    print("ℹ️  Campo has_companion já existe")

try:
    cursor.execute('ALTER TABLE patient ADD COLUMN companion_count INTEGER DEFAULT 0')
    print("✅ Campo companion_count adicionado")
except:
    print("ℹ️  Campo companion_count já existe")

try:
    cursor.execute('ALTER TABLE patient ADD COLUMN companion_name VARCHAR(100)')
    print("✅ Campo companion_name adicionado")
except:
    print("ℹ️  Campo companion_name já existe")

try:
    cursor.execute('ALTER TABLE patient ADD COLUMN companion_rg VARCHAR(20)')
    print("✅ Campo companion_rg adicionado")
except:
    print("ℹ️  Campo companion_rg já existe")

try:
    cursor.execute('ALTER TABLE patient ADD COLUMN other_specialty TEXT')
    print("✅ Campo other_specialty adicionado")
except:
    print("ℹ️  Campo other_specialty já existe")

# Salvar mudanças
conn.commit()
conn.close()

print("🎉 Banco de dados atualizado com sucesso!")