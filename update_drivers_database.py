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

print("🔄 Atualizando estrutura da tabela de motoristas...")

try:
    cursor.execute('ALTER TABLE driver ADD COLUMN employment_type VARCHAR(20) DEFAULT "prefeitura"')
    print("✅ Campo employment_type adicionado")
except:
    print("ℹ️  Campo employment_type já existe")

try:
    cursor.execute('ALTER TABLE driver ADD COLUMN company_name VARCHAR(150)')
    print("✅ Campo company_name adicionado")
except:
    print("ℹ️  Campo company_name já existe")

try:
    cursor.execute('ALTER TABLE driver ADD COLUMN company_cnpj VARCHAR(20)')
    print("✅ Campo company_cnpj adicionado")
except:
    print("ℹ️  Campo company_cnpj já existe")

try:
    cursor.execute('ALTER TABLE driver ADD COLUMN company_contact VARCHAR(100)')
    print("✅ Campo company_contact adicionado")
except:
    print("ℹ️  Campo company_contact já existe")

try:
    cursor.execute('ALTER TABLE driver ADD COLUMN company_phone VARCHAR(15)')
    print("✅ Campo company_phone adicionado")
except:
    print("ℹ️  Campo company_phone já existe")

try:
    cursor.execute('ALTER TABLE driver ADD COLUMN company_address TEXT')
    print("✅ Campo company_address adicionado")
except:
    print("ℹ️  Campo company_address já existe")

# Atualizar motoristas existentes para serem da prefeitura por padrão
cursor.execute('''
    UPDATE driver 
    SET employment_type = "prefeitura" 
    WHERE employment_type IS NULL
''')

# Salvar mudanças
conn.commit()
conn.close()

print("🎉 Banco de dados atualizado com sucesso!")