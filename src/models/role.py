from src import db

class Role(db.Model):
    __tablename__ = 'roles'
    
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100))
    
    # Relación con usuarios
    users = db.relationship('User', backref='role', lazy=True)
    
    def __repr__(self):
        return f'<Role {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.role_id,
            'name': self.name,
            'description': self.description
        } 