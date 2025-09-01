import sqlite3
import os
from datetime import datetime, date
import random

# Caminho do banco
db_path = 'data/transport_system.db'

if not os.path.exists(db_path):
    print("❌ Banco de dados não encontrado!")
    exit(1)

# Lista de motoristas fictícios
drivers_data = [
    {
        'name': 'JOÃO ROBERTO DA SILVA',
        'cpf': '123.456.789-01',
        'cnh': '12345678901',
        'cnh_category': 'D',
        'cnh_expiry': '2025-12-15',
        'phone': '(61) 99123-4567',
        'address': 'Rua das Flores, 123 - Sobradinho/DF',
        'hire_date': '2020-03-15'
    },
    {
        'name': 'EDUARDO ABRANCHES',
        'cpf': '234.567.890-12',
        'cnh': '23456789012',
        'cnh_category': 'D',
        'cnh_expiry': '2026-05-20',
        'phone': '(61) 99234-5678',
        'address': 'Quadra 15, Casa 8 - Planaltina/DF',
        'hire_date': '2019-08-10'
    },
    {
        'name': 'CESAR DA LUA',
        'cpf': '345.678.901-23',
        'cnh': '34567890123',
        'cnh_category': 'D',
        'cnh_expiry': '2025-09-30',
        'phone': '(61) 99345-6789',
        'address': 'Setor Oeste, Lote 45 - Sobradinho/DF',
        'hire_date': '2021-01-20'
    },
    {
        'name': 'JOÃO DE BARROS DE ARRUDA',
        'cpf': '456.789.012-34',
        'cnh': '45678901234',
        'cnh_category': 'D',
        'cnh_expiry': '2026-02-14',
        'phone': '(61) 99456-7890',
        'address': 'Rua Principal, 567 - Fercal/DF',
        'hire_date': '2018-11-05'
    },
    {
        'name': 'CLÉCIO FERREIRA DOS SANTOS',
        'cpf': '567.890.123-45',
        'cnh': '56789012345',
        'cnh_category': 'D',
        'cnh_expiry': '2025-08-12',
        'phone': '(61) 99567-8901',
        'address': 'Quadra 8, Casa 15 - Sobradinho II/DF',
        'hire_date': '2020-06-18'
    },
    {
        'name': 'CARLOS HENRIQUE OLIVEIRA',
        'cpf': '678.901.234-56',
        'cnh': '67890123456',
        'cnh_category': 'D',
        'cnh_expiry': '2026-07-25',
        'phone': '(61) 99678-9012',
        'address': 'Rua do Comércio, 234 - Sobradinho/DF',
        'hire_date': '2019-04-12'
    },
    {
        'name': 'ANTÔNIO CARLOS DA SILVA NETO',
        'cpf': '789.012.345-67',
        'cnh': '78901234567',
        'cnh_category': 'D',
        'cnh_expiry': '2025-11-18',
        'phone': '(61) 99789-0123',
        'address': 'Setor Norte, Quadra 22 - Planaltina/DF',
        'hire_date': '2021-09-03'
    },
    {
        'name': 'FRANCISCO DE ASSIS PEREIRA',
        'cpf': '890.123.456-78',
        'cnh': '89012345678',
        'cnh_category': 'D',
        'cnh_expiry': '2026-03-22',
        'phone': '(61) 99890-1234',
        'address': 'Vila São José, Lote 12 - Sobradinho/DF',
        'hire_date': '2020-12-07'
    },
    {
        'name': 'ROBERTO ALVES DOS SANTOS',
        'cpf': '901.234.567-89',
        'cnh': '90123456789',
        'cnh_category': 'D',
        'cnh_expiry': '2025-10-05',
        'phone': '(61) 99901-2345',
        'address': 'Rua Brasília, 890 - Fercal/DF',
        'hire_date': '2018-07-22'
    },
    {
        'name': 'MARCOS VINÍCIUS LIMA',
        'cpf': '012.345.678-90',
        'cnh': '01234567890',
        'cnh_category': 'D',
        'cnh_expiry': '2026-01-30',
        'phone': '(61) 99012-3456',
        'address': 'Quadra Central, Casa 33 - Sobradinho II/DF',
        'hire_date': '2021-05-14'
    },
    {
        'name': 'JOSÉ MARIA FERNANDES',
        'cpf': '111.222.333-44',
        'cnh': '11122233344',
        'cnh_category': 'D',
        'cnh_expiry': '2025-06-28',
        'phone': '(61) 99111-2222',
        'address': 'Setor Habitacional, Lote 77 - Planaltina/DF',
        'hire_date': '2019-10-16'
    },
    {
        'name': 'PEDRO HENRIQUE COSTA',
        'cpf': '222.333.444-55',
        'cnh': '22233344455',
        'cnh_category': 'C',
        'cnh_expiry': '2026-04-10',
        'phone': '(61) 99222-3333',
        'address': 'Rua da Paz, 456 - Sobradinho/DF',
        'hire_date': '2020-02-29'
    },
    {
        'name': 'LUIZ FERNANDO ROCHA',
        'cpf': '333.444.555-66',
        'cnh': '33344455566',
        'cnh_category': 'D',
        'cnh_expiry': '2025-12-02',
        'phone': '(61) 99333-4444',
        'address': 'Vila Nova, Quadra 5 - Fercal/DF',
        'hire_date': '2021-03-08'
    },
    {
        'name': 'SEBASTIÃO ALMEIDA JUNIOR',
        'cpf': '444.555.666-77',
        'cnh': '44455566677',
        'cnh_category': 'D',
        'cnh_expiry': '2026-08-15',
        'phone': '(61) 99444-5555',
        'address': 'Setor Sul, Casa 98 - Sobradinho II/DF',
        'hire_date': '2018-12-19'
    },
    {
        'name': 'VALDECI RIBEIRO DA CRUZ',
        'cpf': '555.666.777-88',
        'cnh': '55566677788',
        'cnh_category': 'D',
        'cnh_expiry': '2025-07-03',
        'phone': '(61) 99555-6666',
        'address': 'Rua do Trabalhador, 321 - Planaltina/DF',
        'hire_date': '2020-09-11'
    }
]

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("👥 Adicionando motoristas fictícios...")

# Verificar se já existem motoristas
cursor.execute('SELECT COUNT(*) FROM driver')
existing_count = cursor.fetchone()[0]

if existing_count > 0:
    print(f"ℹ️  Já existem {existing_count} motoristas cadastrados.")
    response = input("Deseja adicionar os motoristas fictícios mesmo assim? (s/n): ")
    if response.lower() != 's':
        print("❌ Operação cancelada.")
        conn.close()
        exit()

# Adicionar cada motorista
success_count = 0
for driver in drivers_data:
    try:
        cursor.execute('''
            INSERT INTO driver (name, cpf, cnh, cnh_category, cnh_expiry, phone, address, hire_date, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', (
            driver['name'],
            driver['cpf'],
            driver['cnh'],
            driver['cnh_category'],
            driver['cnh_expiry'],
            driver['phone'],
            driver['address'],
            driver['hire_date']
        ))
        success_count += 1
        print(f"✅ {driver['name']} adicionado")
    except sqlite3.IntegrityError:
        print(f"⚠️  {driver['name']} já existe (CPF/CNH duplicado)")
    except Exception as e:
        print(f"❌ Erro ao adicionar {driver['name']}: {e}")

# Salvar mudanças
conn.commit()
conn.close()

print(f"\n🎉 {success_count} motoristas adicionados com sucesso!")
print("📋 Lista completa de motoristas fictícios disponível no sistema.")