from src import db
from src.models import Product
from src.services.category_service import validate_category
from werkzeug.exceptions import NotFound, Conflict, BadRequest

def validate_product(product_id):
    if not isinstance(product_id, int):
        raise BadRequest("Product ID must be an integer")
    
    product = Product.query.get(product_id)
    if not product:
        raise NotFound(f"Product not found: {product_id}")
    return product

def get_all_products():
    return Product.query.all()

def get_all_products_by_category(category_id):
    category = validate_category(category_id)
    return Product.query.filter_by(category_id=category.category_id).all()

def get_product_by_id(product_id):
    return validate_product(product_id)

def create_product(name, price, category_id, stock):
    if not name or not name.strip():
        raise BadRequest("Name cannot be empty")
    
    if not isinstance(price, (int, float)) or price <= 0:
        raise BadRequest("Price must be a positive number")
    
    if not isinstance(stock, int) or stock < 0:
        raise BadRequest("Stock must be a non-negative integer")
    
    # Validar que la categoría existe
    category = validate_category(category_id)
    
    # Verificar si ya existe un producto con el mismo nombre
    existing_product = Product.query.filter_by(name=name).first()
    if existing_product:
        raise Conflict(f"Product already exists: {name}")
    
    product = Product(name=name, price=price, category_id=category.category_id, stock=stock)
    db.session.add(product)
    db.session.commit()
    return product

def update_product(product_id, **kwargs):
    # Validar campos permitidos
    allowed_fields = {'name', 'price', 'category_id'}
    invalid_fields = set(kwargs.keys()) - allowed_fields
    if invalid_fields:
        raise BadRequest(f"Invalid fields: {invalid_fields}. Allowed fields are: {allowed_fields}")
    
    product = validate_product(product_id)
    
    # Validar y actualizar cada campo si está presente
    if 'name' in kwargs:
        if not kwargs['name'] or not kwargs['name'].strip():
            raise BadRequest("Name cannot be empty")
        # Verificar si el nuevo nombre ya existe en otro producto
        existing_product = Product.query.filter(
            Product.name == kwargs['name'],
            Product.product_id != product_id
        ).first()
        if existing_product:
            raise Conflict(f"Product name already exists: {kwargs['name']}")
        product.name = kwargs['name']
    
    if 'price' in kwargs:
        if not isinstance(kwargs['price'], (int, float)) or kwargs['price'] <= 0:
            raise BadRequest("Price must be a positive number")
        product.price = kwargs['price']
    
    if 'category_id' in kwargs:
        category = validate_category(kwargs['category_id'])
        product.category_id = category.category_id
    
    db.session.commit()
    return product

def update_stock(product_id, stock):
    if not isinstance(stock, int):
        raise BadRequest("Stock must be an integer")
    if stock < 0:
        raise BadRequest("Stock cannot be negative")
    
    product = validate_product(product_id)
    product.stock = stock
    db.session.commit()
    return product

def delete_product(product_id):
    product = validate_product(product_id)
    
    # Verificar si el producto está asociado a alguna venta
    if product.sale_details:
        raise Conflict(f"Cannot delete product with associated sales: {product.name}")
    
    db.session.delete(product)
    db.session.commit()
    return product
