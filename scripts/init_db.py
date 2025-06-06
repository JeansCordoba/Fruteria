from src import create_app, db
from src.models import Category, Product, Supplier, Role, User, Payment
from datetime import datetime

def init_db():
    app = create_app()
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Crear roles
        admin_role = Role(name='admin', description='Administrador del sistema')
        seller_role = Role(name='seller', description='Vendedor')
        db.session.add_all([admin_role, seller_role])
        
        # Crear usuario administrador
        admin = User(
            username='admin',
            password='admin123',  # En producción, esto debería estar hasheado
            name='Admin',
            last_name='System',
            email='admin@fruteria.com',
            role=admin_role
        )
        db.session.add(admin)
        
        # Crear categorías
        categories = [
            Category(name='Frutas'),
            Category(name='Verduras'),
            Category(name='Tuberculos'),
            Category(name='Legumbres')
        ]
        db.session.add_all(categories)
        
        # Crear proveedores
        suppliers = [
            Supplier(
                name='Proveedor A',
                contact_name='Juan Pérez',
                phone='1234567890',
                email='juan@proveedora.com',
                address='Calle 1 #2-3'
            ),
            Supplier(
                name='Proveedor B',
                contact_name='María López',
                phone='0987654321',
                email='maria@proveedorb.com',
                address='Calle 4 #5-6'
            )
        ]
        db.session.add_all(suppliers)
        
        # Crear métodos de pago
        payments = [
            Payment(name='Efectivo', description='Pago en efectivo'),
            Payment(name='Tarjeta', description='Pago con tarjeta de crédito/débito'),
            Payment(name='Transferencia', description='Transferencia bancaria')
        ]
        db.session.add_all(payments)
        
        # Guardar todos los cambios
        db.session.commit()
        
        print("Base de datos inicializada con éxito!")

if __name__ == '__main__':
    init_db() 