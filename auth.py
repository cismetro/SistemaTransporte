from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db
from models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"Tentativa de login: {username}")  # Debug
        
        if username and password:
            user = User.query.filter_by(username=username).first()
            
            if user:
                print(f"Usuário encontrado: {user.username}")  # Debug
                if user.check_password(password):
                    login_user(user)
                    flash('Login realizado com sucesso!', 'success')
                    print("Login bem-sucedido!")  # Debug
                    return redirect('/dashboard')
                else:
                    print("Senha incorreta")  # Debug
                    flash('Senha incorreta', 'danger')
            else:
                print("Usuário não encontrado")  # Debug
                flash('Usuário não encontrado', 'danger')
        else:
            flash('Por favor, preencha todos os campos', 'warning')
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso', 'info')
    return redirect(url_for('auth.login'))