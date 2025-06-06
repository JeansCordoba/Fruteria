from src import db

class Client(db.Model):
    __tablename__ = 'clients'
    
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    identity_card = db.Column(db.String(20), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    registration_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    # Relación con ventas
    sales = db.relationship('Sale', backref='client', lazy=True)
    
    def __repr__(self):
        return f'<Client {self.name} {self.last_name}>'
    
    def to_dict(self):
        return {
            'id': self.client_id,
            'name': self.name,
            'last_name': self.last_name,
            'identity_card': self.identity_card,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None
        } 