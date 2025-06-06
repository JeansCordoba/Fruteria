from src import db

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Clave foránea
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    
    # Relación con ventas
    sales = db.relationship('Sale', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.user_id,
            'username': self.username,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'is_active': self.is_active,
            'role_id': self.role_id
        } 