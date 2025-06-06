from src import db

class Sale(db.Model):
    __tablename__ = 'sales'
    
    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='completed')  # completed, cancelled, pending
    
    # Claves foráneas
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.payment_id'), nullable=False)
    
    # Relaciones
    details = db.relationship('SaleDetail', backref='sale', lazy=True)
    
    def __repr__(self):
        return f'<Sale {self.sale_id}>'
    
    def to_dict(self):
        return {
            'id': self.sale_id,
            'date': self.date.isoformat() if self.date else None,
            'total': float(self.total),
            'status': self.status,
            'client_id': self.client_id,
            'user_id': self.user_id,
            'payment_id': self.payment_id,
            'details': [detail.to_dict() for detail in self.details]
        } 