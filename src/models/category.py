from src import db

class Category(db.Model):
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relación con productos
    products = db.relationship('Product', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.category_id,
            'name': self.name
        } 