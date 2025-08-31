try:
    print("Testando imports...")
    from models import db, init_db
    print("✅ models importado")
    
    from models.user import User
    print("✅ User importado")
    
    from models.patient import Patient
    print("✅ Patient importado")
    
    from models.driver import Driver
    print("✅ Driver importado")
    
    from models.vehicle import Vehicle
    print("✅ Vehicle importado")
    
    from models.transport import Transport
    print("✅ Transport importado")
    
    print("🎉 Todos os imports funcionaram!")
    
except Exception as e:
    print(f"❌ Erro: {e}")