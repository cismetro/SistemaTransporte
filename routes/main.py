from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db
from models.patient import Patient
from models.driver import Driver
from models.vehicle import Vehicle
from models.transport import Transport
from datetime import datetime, date

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
@login_required
def dashboard():
    # Estatísticas básicas
    total_patients = Patient.query.count()
    total_drivers = Driver.query.filter_by(is_active=True).count()
    total_vehicles = Vehicle.query.filter_by(is_active=True).count()
    
    # Transportes de hoje
    today = date.today()
    today_transports = Transport.query.filter_by(appointment_date=today).count()
    
    # Próximos transportes (próximos 5)
    upcoming_transports = Transport.query.filter(
        Transport.appointment_date >= today,
        Transport.status == 'agendado'
    ).order_by(Transport.appointment_date, Transport.appointment_time).limit(5).all()
    
    return render_template('dashboard.html',
                         total_patients=total_patients,
                         total_drivers=total_drivers,
                         total_vehicles=total_vehicles,
                         today_transports=today_transports,
                         upcoming_transports=upcoming_transports)

@main.route('/reports')
@login_required
def reports():
    return render_template('reports.html')