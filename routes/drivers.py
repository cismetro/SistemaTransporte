from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db
from models.driver import Driver
from datetime import datetime

drivers = Blueprint('drivers', __name__)

@drivers.route('/')
@login_required
def list():
    drivers_list = Driver.query.filter_by(is_active=True).all()
    return render_template('drivers/list.html', drivers=drivers_list)

@drivers.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        driver = Driver(
            name=request.form['name'],
            cpf=request.form['cpf'],
            cnh=request.form['cnh'],
            cnh_category=request.form['cnh_category'],
            cnh_expiry=datetime.strptime(request.form['cnh_expiry'], '%Y-%m-%d').date(),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            hire_date=datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()
        )
        
        try:
            db.session.add(driver)
            db.session.commit()
            flash('Motorista cadastrado com sucesso!', 'success')
            return redirect(url_for('drivers.list'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar motorista.', 'danger')
    
    return render_template('drivers/form.html', driver=None)