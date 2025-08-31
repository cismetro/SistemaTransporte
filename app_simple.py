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
            
            cursor.execute('''
                INSERT INTO patient (cpf, name, birth_date, phone, address, 
                                   emergency_contact, emergency_phone, special_needs, priority_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.form['cpf'],
                request.form['name'],
                request.form['birth_date'],
                request.form.get('phone'),
                request.form.get('address'),
                request.form.get('emergency_contact'),
                request.form.get('emergency_phone'),
                request.form.get('special_needs'),
                request.form.get('priority_type')
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
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM driver WHERE is_active = 1 ORDER BY name')
    drivers_list = cursor.fetchall()
    conn.close()
    
    return render_template('drivers.html', drivers=drivers_list)

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