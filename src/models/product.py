from src import db
from decimal import Decimal

class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Precio con 2 decimales
    stock = db.Column(db.Integer, nullable=False, default=0)
    
    # Claves foráneas
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.product_id,
            'name': self.name,
            'price': float(self.price),
            'stock': self.stock,
            'category_id': self.category_id,
            'supplier_id': self.supplier_id
        } 