from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.transport import Transport
from models.patient import Patient
from models.driver import Driver
from models.vehicle import Vehicle
from datetime import datetime

transports = Blueprint('transports', __name__)

@transports.route('/')
@login_required
def list():
    transports_list = Transport.query.order_by(Transport.appointment_date.desc()).limit(50).all()
    return render_template('transports/list.html', transports=transports_list)

@transports.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if request.method == 'POST':
        transport = Transport(
            patient_id=int(request.form['patient_id']),
            driver_id=int(request.form['driver_id']),
            vehicle_id=int(request.form['vehicle_id']),
            destination=request.form['destination'],
            appointment_date=datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date(),
            appointment_time=datetime.strptime(request.form['appointment_time'], '%H:%M').time() if request.form.get('appointment_time') else None,
            departure_time=datetime.strptime(request.form['departure_time'], '%H:%M').time() if request.form.get('departure_time') else None,
            medical_guide=request.form.get('medical_guide'),
            specialty=request.form.get('specialty'),
            observations=request.form.get('observations'),
            created_by=current_user.id
        )
        
        try:
            db.session.add(transport)
            db.session.commit()
            flash('Transporte agendado com sucesso!', 'success')
            return redirect(url_for('transports.list'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao agendar transporte.', 'danger')
    
    patients = Patient.query.all()
    drivers = Driver.query.filter_by(is_active=True).all()
    vehicles = Vehicle.query.filter_by(is_active=True).all()
    
    return render_template('transports/schedule.html', 
                         patients=patients, 
                         drivers=drivers, 
                         vehicles=vehicles)