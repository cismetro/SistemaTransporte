from flask import Flask
from models import init_db, db
from models.user import User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
init_db(app)

with app.app_context():
    # Verificar se o usuário admin existe
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print("✅ Usuário admin encontrado!")
        print(f"   Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Role: {admin.role}")
        print(f"   Ativo: {admin.is_active}")
        
        # Testar senha
        if admin.check_password('admin123'):
            print("✅ Senha 'admin123' está correta!")
        else:
            print("❌ Senha 'admin123' está incorreta!")
            
            # Resetar senha
            admin.set_password('admin123')
            db.session.commit()
            print("🔄 Senha resetada para 'admin123'")
    else:
        print("❌ Usuário admin não encontrado!")
        
        # Criar usuário admin
        from werkzeug.security import generate_password_hash
        admin = User(
            username='admin',
            email='admin@transporte.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuário admin criado!")