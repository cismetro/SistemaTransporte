from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'transport-health-system-2024'

# Caminho do banco
DB_PATH = 'data/transport_system.db'

def get_db():
    """Conecta ao banco SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
    return conn

def check_auth():
    """Verifica se o usuário está logado"""
    return 'user_id' in session

@app.route('/')
def index():
    if check_auth():
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, password_hash, role 
                FROM user 
                WHERE username = ? AND is_active = 1
            ''', (username,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                flash('Login realizado com sucesso!', 'success')
                return redirect('/dashboard')
            else:
                flash('Usuário ou senha inválidos', 'danger')
        else:
            flash('Por favor, preencha todos os campos', 'warning')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso', 'info')
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if not check_auth():
        return redirect('/login')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Contar dados básicos
    cursor.execute('SELECT COUNT(*) as count FROM patient')
    total_patients = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM driver WHERE is_active = 1')
    total_drivers = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM vehicle WHERE is_active = 1')
    total_vehicles = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM transport')
    total_transports = cursor.fetchone()['count']
    
    conn.close()
    
    return render_template('dashboard.html',
                         total_patients=total_patients,
                         total_drivers=total_drivers,
                         total_vehicles=total_vehicles,
                         total_transports=total_transports)

@app.route('/patients')
def patients():
    if not check_auth():
        return redirect('/login')
    
    search = request.args.get('search', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    if search:
        cursor.execute('''
            SELECT * FROM patient 
            WHERE name LIKE ? OR cpf LIKE ?
            ORDER BY name
        ''', (f'%{search}%', f'%{search}%'))
    else:
        cursor.execute('SELECT * FROM patient ORDER BY name')
    
    patients_list = cursor.fetchall()
    conn.close()
    
    return render_template('patients.html', patients=patients_list, search=search)

@app.route('/patients/new', methods=['GET', 'POST'])
def patients_new():
    if not check_auth():
        return redirect('/login')
    
    if request.method == 'POST':
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            # Determinar especialidade final
            specialty = request.form['specialty']
            if specialty == 'Outro':
                specialty = request.form.get('other_specialty', 'Não especificado')
            
            cursor.execute('''
                INSERT INTO patient (cpf, name, birth_date, phone, address, 
                                   emergency_contact, emergency_phone, special_needs, priority_type,
                                   appointment_date, attendant_name, destination, appointment_time, 
                                   specialty, has_companion, companion_count, companion_name, companion_rg)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.form['cpf'],
                request.form['name'].upper(),
                request.form['birth_date'],
                request.form.get('phone'),
                request.form.get('address'),
                request.form.get('emergency_contact'),
                request.form.get('emergency_phone'),
                request.form.get('special_needs'),
                request.form.get('priority_type', 'normal'),
                request.form['appointment_date'],
                request.form['attendant_name'].upper(),
                request.form['destination'],
                request.form.get('appointment_time') or None,
                specialty,
                1 if 'has_companion' in request.form else 0,
                int(request.form.get('companion_count', 0)),
                request.form.get('companion_name', '').upper() if request.form.get('companion_name') else None,
                request.form.get('companion_rg')
            ))
            
            conn.commit()
            conn.close()
            
            flash('Paciente cadastrado com sucesso!', 'success')
            return redirect('/patients')
        except Exception as e:
            flash(f'Erro ao cadastrar paciente: {str(e)}', 'danger')
    
    return render_template('patients/form.html', patient=None)

@app.route('/drivers')
def drivers():
    if not check_auth():
        return redirect('/login')
    
    search = request.args.get('search', '')
    status_filter = request.args.get('status_filter', 'all')
    employment_filter = request.args.get('employment_filter', 'all')
    cnh_filter = request.args.get('cnh_filter', 'all')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Construir query base
    query = 'SELECT * FROM driver WHERE 1=1'
    params = []
    
    # Aplicar filtros
    if search:
        query += ' AND (name LIKE ? OR cnh LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    if status_filter == 'active':
        query += ' AND is_active = 1'
    elif status_filter == 'inactive':
        query += ' AND (is_active = 0 OR is_active IS NULL)'
    
    if employment_filter == 'prefeitura':
        query += ' AND (employment_type = "prefeitura" OR employment_type IS NULL OR employment_type = "")'
    elif employment_filter == 'terceirizado':
        query += ' AND employment_type = "terceirizado"'
    
    if cnh_filter != 'all':
        query += ' AND cnh_category = ?'
        params.append(cnh_filter)
    
    query += ' ORDER BY name'
    
    print(f"🔍 Query SQL: {query}")
    print(f"🔍 Parâmetros: {params}")
    
    cursor.execute(query, params)
    drivers_list = cursor.fetchall()
    
    print(f"🔍 Total de motoristas encontrados: {len(drivers_list)}")
    if drivers_list:
        first_driver = drivers_list[0]
        # Usar try/except para campos que podem não existir
        try:
            employment_type = first_driver['employment_type'] if 'employment_type' in first_driver.keys() else 'NULL'
        except:
            employment_type = 'NULL'
            
        try:
            company_name = first_driver['company_name'] if 'company_name' in first_driver.keys() else 'NULL'
        except:
            company_name = 'NULL'
            
        print(f"🔍 Primeiro motorista:")
        print(f"   - Nome: {first_driver['name']}")
        print(f"   - CNH Categoria: {first_driver['cnh_category']}")
        print(f"   - Ativo: {first_driver['is_active']}")
        print(f"   - Employment Type: {employment_type}")
        print(f"   - Company Name: {company_name}")
    
    conn.close()
    
    return render_template('drivers.html', 
                         drivers=drivers_list, 
                         search=search,
                         status_filter=status_filter,
                         employment_filter=employment_filter,
                         cnh_filter=cnh_filter)

@app.route('/drivers/<int:driver_id>/toggle-status', methods=['POST'])
def drivers_toggle_status(driver_id):
    if not check_auth():
        return redirect('/login')
    
    import json
    data = json.loads(request.data)
    active = data.get('active', True)
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('UPDATE driver SET is_active = ? WHERE id = ?', (1 if active else 0, driver_id))
        conn.commit()
        conn.close()
        
        status = "ativado" if active else "desativado"
        flash(f'Motorista {status} com sucesso!', 'success')
        return {'success': True}
    except Exception as e:
        conn.close()
        return {'success': False, 'error': str(e)}, 500

                         
@app.route('/vehicles')
def vehicles():
    if not check_auth():
        return redirect('/login')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicle WHERE is_active = 1 ORDER BY plate')
    vehicles_list = cursor.fetchall()
    conn.close()
    
    return render_template('vehicles.html', vehicles=vehicles_list)

@app.route('/transports')
def transports():
    if not check_auth():
        return redirect('/login')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, p.name as patient_name, d.name as driver_name, v.plate as vehicle_plate
        FROM transport t
        LEFT JOIN patient p ON t.patient_id = p.id
        LEFT JOIN driver d ON t.driver_id = d.id
        LEFT JOIN vehicle v ON t.vehicle_id = v.id
        ORDER BY t.appointment_date DESC
        LIMIT 50
    ''')
    transports_list = cursor.fetchall()
    conn.close()
    
    return render_template('transports.html', transports=transports_list)


@app.route('/drivers/new', methods=['GET', 'POST'])
def drivers_new():
    if not check_auth():
        return redirect('/login')
    
    if request.method == 'POST':
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO driver (name, cpf, cnh, cnh_category, cnh_expiry, phone, address, hire_date, 
                                  employment_type, company_name, company_cnpj, company_contact, 
                                  company_phone, company_address, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            ''', (
                request.form['name'],
                request.form['cpf'],
                request.form['cnh'],
                request.form['cnh_category'],
                request.form['cnh_expiry'],
                request.form.get('phone'),
                request.form.get('address'),
                request.form['hire_date'],
                request.form['employment_type'],
                request.form.get('company_name') if request.form['employment_type'] == 'terceirizado' else None,
                request.form.get('company_cnpj') if request.form['employment_type'] == 'terceirizado' else None,
                request.form.get('company_contact') if request.form['employment_type'] == 'terceirizado' else None,
                request.form.get('company_phone') if request.form['employment_type'] == 'terceirizado' else None,
                request.form.get('company_address') if request.form['employment_type'] == 'terceirizado' else None
            ))
            
            conn.commit()
            conn.close()
            
            flash('Motorista cadastrado com sucesso!', 'success')
            return redirect('/drivers')
        except Exception as e:
            flash(f'Erro ao cadastrar motorista: {str(e)}', 'danger')
    
    return render_template('drivers/form.html', driver=None)
@app.route('/drivers/<int:driver_id>/view')
def drivers_view(driver_id):
    if not check_auth():
        return redirect('/login')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Buscar dados do motorista
    cursor.execute('SELECT * FROM driver WHERE id = ?', (driver_id,))
    driver = cursor.fetchone()
    
    if not driver:
        flash('Motorista não encontrado!', 'danger')
        return redirect('/drivers')
    
    # Buscar transportes realizados por este motorista
    cursor.execute('''
        SELECT t.*, p.name as patient_name, v.plate as vehicle_plate
        FROM transport t
        LEFT JOIN patient p ON t.patient_id = p.id
        LEFT JOIN vehicle v ON t.vehicle_id = v.id
        WHERE t.driver_id = ?
        ORDER BY t.appointment_date DESC
        LIMIT 10
    ''', (driver_id,))
    recent_transports = cursor.fetchall()
    
    # Estatísticas do motorista
    cursor.execute('SELECT COUNT(*) as total FROM transport WHERE driver_id = ?', (driver_id,))
    total_transports = cursor.fetchone()['total']
    
    cursor.execute('''
        SELECT COUNT(*) as completed 
        FROM transport 
        WHERE driver_id = ? AND status = 'concluido'
    ''', (driver_id,))
    completed_transports = cursor.fetchone()['completed']
    
    conn.close()
    
    return render_template('drivers/view.html', 
                         driver=driver, 
                         recent_transports=recent_transports,
                         total_transports=total_transports,
                         completed_transports=completed_transports)


@app.route('/drivers/<int:driver_id>/edit', methods=['GET', 'POST'])
def drivers_edit(driver_id):
    if not check_auth():
        return redirect('/login')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Buscar dados do motorista
    cursor.execute('SELECT * FROM driver WHERE id = ?', (driver_id,))
    driver = cursor.fetchone()
    
    if not driver:
        flash('Motorista não encontrado!', 'danger')
        return redirect('/drivers')
    
    if request.method == 'POST':
        try:
            cursor.execute('''
                UPDATE driver 
                SET name = ?, cpf = ?, cnh = ?, cnh_category = ?, cnh_expiry = ?, 
                    phone = ?, address = ?, hire_date = ?, employment_type = ?,
                    company_name = ?, company_cnpj = ?, company_contact = ?,
                    company_phone = ?, company_address = ?, is_active = ?
                WHERE id = ?
            ''', (
                request.form['name'],
                request.form['cpf'],
                request.form['cnh'],
                request.form['cnh_category'],
                request.form['cnh_expiry'],
                request.form.get('phone'),
                request.form.get('address'),
                request.form['hire_date'],
                request.form['employment_type'],
                request.form.get('company_name') if request.form['employment_type'] == 'terceirizado' else None,
                request.form.get('company_cnpj') if request.form['employment_type'] == 'terceirizado' else None,
                request.form.get('company_contact') if request.form['employment_type'] == 'terceirizado' else None,
                request.form.get('company_phone') if request.form['employment_type'] == 'terceirizado' else None,
                request.form.get('company_address') if request.form['employment_type'] == 'terceirizado' else None,
                1 if 'is_active' in request.form else 0,
                driver_id
            ))
            
            conn.commit()
            conn.close()
            
            flash('Motorista atualizado com sucesso!', 'success')
            return redirect(f'/drivers/{driver_id}/view')
        except Exception as e:
            conn.close()
            flash(f'Erro ao atualizar motorista: {str(e)}', 'danger')
    else:
        conn.close()
    
    return render_template('drivers/form.html', driver=driver)

@app.route('/vehicles/new', methods=['GET', 'POST'])
def vehicles_new():
    if not check_auth():
        return redirect('/login')
    
    if request.method == 'POST':
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO vehicle (plate, model, brand, year, ownership, capacity, 
                                   has_wheelchair_access, has_stretcher, has_oxygen, current_km)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.form['plate'].upper(),
                request.form['model'],
                request.form['brand'],
                int(request.form['year']),
                request.form['ownership'],
                int(request.form.get('capacity', 4)),
                1 if 'wheelchair' in request.form else 0,
                1 if 'stretcher' in request.form else 0,
                1 if 'oxygen' in request.form else 0,
                int(request.form.get('current_km', 0))
            ))
            
            conn.commit()
            conn.close()
            
            flash('Veículo cadastrado com sucesso!', 'success')
            return redirect('/vehicles')
        except Exception as e:
            flash(f'Erro ao cadastrar veículo: {str(e)}', 'danger')
    
    return render_template('vehicles/form.html', vehicle=None)

@app.route('/transports/new', methods=['GET', 'POST'])
def transports_new():
    if not check_auth():
        return redirect('/login')
    
    if request.method == 'POST':
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            # Determinar destino final
            destination = request.form['destination']
            if destination == 'Outro':
                destination = request.form.get('custom_destination', 'Não especificado')
            
            cursor.execute('''
                INSERT INTO transport (patient_id, driver_id, vehicle_id, destination, 
                                     appointment_date, appointment_time, departure_time, 
                                     medical_guide, specialty, observations, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                int(request.form['patient_id']),
                int(request.form['driver_id']),
                int(request.form['vehicle_id']),
                destination,
                request.form['appointment_date'],
                request.form.get('appointment_time') or None,
                request.form.get('departure_time') or None,
                request.form.get('medical_guide'),
                request.form.get('specialty'),
                request.form.get('observations'),
                session['user_id']
            ))
            
            conn.commit()
            conn.close()
            
            flash('Transporte agendado com sucesso!', 'success')
            return redirect('/transports')
        except Exception as e:
            flash(f'Erro ao agendar transporte: {str(e)}', 'danger')
    
    # Buscar dados para os selects
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patient ORDER BY name')
    patients = cursor.fetchall()
    
    cursor.execute('SELECT * FROM driver WHERE is_active = 1 ORDER BY name')
    drivers = cursor.fetchall()
    
    cursor.execute('SELECT * FROM vehicle WHERE is_active = 1 ORDER BY plate')
    vehicles = cursor.fetchall()
    
    conn.close()
    
    return render_template('transports/form.html', 
                         transport=None, 
                         patients=patients, 
                         drivers=drivers, 
                         vehicles=vehicles)




if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print("❌ Banco de dados não encontrado!")
        print("Execute primeiro: python createdb_simple.py")
        exit(1)
    
    print("🚀 Iniciando servidor na porta 8080...")
    print("🔗 Acesse: http://localhost:8080")
    print("👤 Login: admin")
    print("🔑 Senha: admin123")
    
    app.run(debug=True, host='0.0.0.0', port=8080)