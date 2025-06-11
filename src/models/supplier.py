from src import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    nit = db.Column(db.String(20))
    
    products = db.relationship('Product', backref='supplier', lazy=True)
    
    def __repr__(self):
        return f'<Supplier {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.supplier_id,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'nit': self.nit
        } 