from flask import Flask, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from waitress import serve
import os
from config import Config
from models import init_db, db, login_manager
from models.user import User
from models.patient import Patient
from models.driver import Driver
from models.vehicle import Vehicle
from models.transport import Transport

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensões
    init_db(app)
    
    # User loader para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Registrar blueprint de autenticação
    from auth import auth
    app.register_blueprint(auth)
    
    # Rota principal
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect('/dashboard')
        return redirect(url_for('auth.login'))
    
    # Dashboard
    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Contar dados básicos
        total_patients = Patient.query.count()
        total_drivers = Driver.query.filter_by(is_active=True).count()
        total_vehicles = Vehicle.query.filter_by(is_active=True).count()
        total_transports = Transport.query.count()
        
        return render_template('dashboard.html',
                             total_patients=total_patients,
                             total_drivers=total_drivers,
                             total_vehicles=total_vehicles,
                             total_transports=total_transports)
    
    # Pacientes
    @app.route('/patients')
    @login_required
    def patients():
        search = request.args.get('search', '')
        patients_list = []
        
        if search:
            patients_list = Patient.query.filter(
                Patient.name.contains(search) | Patient.cpf.contains(search)
            ).all()
        else:
            patients_list = Patient.query.all()
        
        return render_template('patients.html', patients=patients_list, search=search)
    
    @app.route('/patients/new', methods=['GET', 'POST'])
    @login_required
    def patients_new():
        if request.method == 'POST':
            try:
                from datetime import datetime
                patient = Patient(
                    cpf=request.form['cpf'],
                    name=request.form['name'],
                    birth_date=datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date(),
                    phone=request.form.get('phone'),
                    address=request.form.get('address'),
                    emergency_contact=request.form.get('emergency_contact'),
                    emergency_phone=request.form.get('emergency_phone'),
                    special_needs=request.form.get('special_needs'),
                    priority_type=request.form.get('priority_type')
                )
                
                db.session.add(patient)
                db.session.commit()
                flash('Paciente cadastrado com sucesso!', 'success')
                return redirect('/patients')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar paciente: {str(e)}', 'danger')
        
        return render_template('patients/form.html', patient=None)
    
    # Outras páginas básicas
    @app.route('/drivers')
    @login_required
    def drivers():
        drivers_list = Driver.query.filter_by(is_active=True).all()
        return render_template('drivers.html', drivers=drivers_list)
    
    @app.route('/vehicles')
    @login_required
    def vehicles():
        vehicles_list = Vehicle.query.filter_by(is_active=True).all()
        return render_template('vehicles.html', vehicles=vehicles_list)
    
    @app.route('/transports')
    @login_required
    def transports():
        transports_list = Transport.query.order_by(Transport.appointment_date.desc()).limit(50).all()
        return render_template('transports.html', transports=transports_list)
    
    # Criar diretórios necessários
    os.makedirs('data', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    return app

def main():
    app = create_app()
    
    if os.environ.get('FLASK_ENV') == 'development':
        print("🚀 Iniciando servidor de desenvolvimento na porta 8080...")
        app.run(debug=True, host='0.0.0.0', port=8080)
    else:
        print("🚀 Iniciando servidor de produção na porta 8080...")
        serve(app, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()