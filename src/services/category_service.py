from src import db
from src.models import Category
from werkzeug.exceptions import NotFound, Conflict, BadRequest

def validate_category(category_id):
    if not isinstance(category_id, int):
        raise BadRequest("Category ID must be an integer")
    
    category = Category.query.get(category_id)
    if not category:
        raise NotFound(f"Category not found: {category_id}")
    return category

def get_all_categories():
    return Category.query.all()

def get_category_by_id(category_id):
    return validate_category(category_id)

def create_category(name):
    if not name or not name.strip():
        raise BadRequest("Name cannot be empty")
    
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        raise Conflict(f"Category already exists: {name}")
    
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return category

def update_category(category_id, name):
    if not name or not name.strip():
        raise BadRequest("Name cannot be empty")
    
    category = validate_category(category_id)
    
    # Verificar si el nuevo nombre ya existe en otra categoría
    existing_category = Category.query.filter(Category.name == name, Category.category_id != category_id).first()
    if existing_category:
        raise Conflict(f"Category name already exists: {name}")
    
    category.name = name
    db.session.commit()
    return category

def delete_category(category_id):
    category = validate_category(category_id)
    
    # Verificar si la categoría tiene productos asociados
    if category.products:
        raise Conflict(f"Cannot delete category with associated products: {category.name}")
    
    db.session.delete(category)
    db.session.commit()
    return category 