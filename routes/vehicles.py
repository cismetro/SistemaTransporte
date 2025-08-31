from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db
from models.vehicle import Vehicle

vehicles = Blueprint('vehicles', __name__)

@vehicles.route('/')
@login_required
def list():
    vehicles_list = Vehicle.query.filter_by(is_active=True).all()
    return render_template('vehicles/list.html', vehicles=vehicles_list)

@vehicles.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        vehicle = Vehicle(
            plate=request.form['plate'].upper(),
            model=request.form['model'],
            brand=request.form['brand'],
            year=int(request.form['year']),
            ownership=request.form['ownership'],
            capacity=int(request.form.get('capacity', 4)),
            has_wheelchair_access='wheelchair' in request.form,
            has_stretcher='stretcher' in request.form,
            has_oxygen='oxygen' in request.form,
            current_km=int(request.form.get('current_km', 0))
        )
        
        try:
            db.session.add(vehicle)
            db.session.commit()
            flash('Veículo cadastrado com sucesso!', 'success')
            return redirect(url_for('vehicles.list'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar veículo.', 'danger')
    
    return render_template('vehicles/form.html', vehicle=None)