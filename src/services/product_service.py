from src import db
from src.models import Product
from src.services.category_service import get_category_by_id

def validate_category(category_id):
    try:
        category = get_category_by_id(category_id)
        if not category:
            raise ValueError(f"Category not found: {category_id}")
        return category
    except ValueError as e:
        raise ValueError(f"Category not found: {e}")

def get_all_products():
    return Product.query.all()

def get_all_products_by_category(category_id):
    validate_category(category_id)
    return Product.query.filter_by(category_id=category_id).all()

def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if not product:
        raise ValueError(f"Product not found: {product_id}")
    return product

def create_product(name, price, category_id, stock):
    if not name or not price or not category_id or stock is None:
        raise ValueError("All fields are required")
    if price < 0 or stock < 0:
        raise ValueError("Price and stock must be positive numbers")
    
    category = validate_category(category_id)
    product = Product(name=name, price=price, category_id=category.id, stock=stock)
    db.session.add(product)
    db.session.commit()
    return product

def update_product(product_id, **kwargs):
    allowed_fields = {'name', 'price', 'category_id'}
    invalid_fields = set(kwargs.keys()) - allowed_fields
    
    if invalid_fields:
        raise ValueError(f"Invalid fields: {invalid_fields}. Allowed fields are: {allowed_fields}")
    
    product = get_product_by_id(product_id)
    category_id = kwargs.get('category_id')
    
    if category_id:
        category = validate_category(category_id)
        product.category_id = category.id
    
    if 'name' in kwargs:
        product.name = kwargs['name']
    if 'price' in kwargs:
        product.price = kwargs['price']
    
    db.session.commit()
    return product

def update_stock(product_id, stock):
    if stock < 0:
        raise ValueError("Stock cannot be negative")
    
    product = get_product_by_id(product_id)
    product.stock = stock
    db.session.commit()
    return product

def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return product
