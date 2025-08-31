from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models import db
from models.patient import Patient
from datetime import datetime

patients = Blueprint('patients', __name__)

@patients.route('/')
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Patient.query
    if search:
        query = query.filter(Patient.name.contains(search) | Patient.cpf.contains(search))
    
    patients_list = query.paginate(page=page, per_page=20, error_out=False)
    return render_template('patients/list.html', patients=patients_list, search=search)

@patients.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
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
        
        try:
            db.session.add(patient)
            db.session.commit()
            flash('Paciente cadastrado com sucesso!', 'success')
            return redirect(url_for('patients.list'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar paciente. CPF pode já estar cadastrado.', 'danger')
    
    return render_template('patients/form.html', patient=None)

@patients.route('/search')
@login_required
def search():
    cpf = request.args.get('cpf')
    if cpf:
        patient = Patient.query.filter_by(cpf=cpf).first()
        if patient:
            return jsonify({
                'found': True,
                'id': patient.id,
                'name': patient.name,
                'cpf': patient.cpf,
                'phone': patient.phone,
                'special_needs': patient.special_needs,
                'priority_type': patient.priority_type
            })
    return jsonify({'found': False})