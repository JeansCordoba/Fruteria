from src import db

class SaleDetail(db.Model):
    __tablename__ = 'sale_details'
    
    # Claves primarias compuestas
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.sale_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True)
    
    # Campos adicionales
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Precio unitario al momento de la venta
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<SaleDetail {self.sale_id} - {self.product_id}>'
    
    def to_dict(self):
        return {
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': float(self.price),
            'subtotal': float(self.subtotal)
        } 