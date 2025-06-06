from src import db

class Payment(db.Model):
    __tablename__ = 'payments'
    
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(100))
    
    # Relación con ventas
    sales = db.relationship('Sale', backref='payment', lazy=True)
    
    def __repr__(self):
        return f'<Payment {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.payment_id,
            'name': self.name,
            'description': self.description
        } 