from src import db
from src.models import Product
from src.services.category_service import validate_category
from werkzeug.exceptions import NotFound, Conflict, BadRequest
from src.utils.validations import (
    validate_string_field,
    validate_numeric_field
)

def validate_product(product_id):
    """
    Validate if a product exists.
    
    Args:
        product_id (int): The ID of the product to validate
        
    Returns:
        Product: The validated product instance
        
    Raises:
        BadRequest: If product_id is not an integer
        NotFound: If product is not found
    """
    if not isinstance(product_id, int):
        raise BadRequest("Product ID must be an integer")
    
    product = Product.query.get(product_id)
    if not product:
        raise NotFound(f"Product not found: {product_id}")
    return product

def validate_product_fields(**kwargs):
    """
    Validate product fields.
    
    Args:
        **kwargs: Product fields to validate
        
    Returns:
        bool: True if all validations pass
        
    Raises:
        BadRequest: If any validation fails
        Conflict: If product name already exists
    """
    validate_string_field(kwargs.get('name'), 'Name')
    validate_numeric_field(kwargs.get('price'), 'Price')
    validate_numeric_field(kwargs.get('stock'), 'Stock')
    
    if 'name' in kwargs:
        existing_product = Product.query.filter_by(name=kwargs['name']).first()
        if existing_product:
            raise Conflict(f"Product already exists: {kwargs['name']}")
    
    return True

def get_all_products():
    """
    Get all products.
    
    Returns:
        list: List of all products
    """
    return Product.query.all()

def get_all_products_by_category(category_id):
    category = validate_category(category_id)
    return Product.query.filter_by(category_id=category.category_id).all()

def get_product_by_id(product_id):
    """
    Get a product by its ID.
    
    Args:
        product_id (int): The ID of the product to get
        
    Returns:
        Product: The requested product
    """
    return validate_product(product_id)

def create_product(name, price, stock, description=None):
    """
    Create a new product.
    
    Args:
        name (str): Product name
        price (float): Product price
        stock (int): Product stock quantity
        description (str, optional): Product description. Defaults to None.
    
    Returns:
        Product: The created product instance
    """
    validate_product_fields(
        name=name,
        price=price,
        stock=stock
    )
    
    product = Product(
        name=name,
        price=price,
        stock=stock,
        description=description
    )
    
    db.session.add(product)
    db.session.commit()
    return product

def update_product(product_id, **kwargs):
    """
    Update a product.
    
    Args:
        product_id (int): The ID of the product to update
        **kwargs: Fields to update
        
    Returns:
        Product: The updated product instance
    """
    product = validate_product(product_id)
    validate_product_fields(**kwargs)
    
    if 'name' in kwargs:
        product.name = kwargs['name']
    if 'price' in kwargs:
        product.price = kwargs['price']
    if 'stock' in kwargs:
        product.stock = kwargs['stock']
    if 'description' in kwargs:
        product.description = kwargs['description']
    
    db.session.commit()
    return product

def update_stock(product_id, stock):
    product = validate_product(product_id)
    validate_product_fields(stock=stock)
    product.stock = stock
    db.session.commit()
    return product

def delete_product(product_id):
    """
    Delete a product.
    
    Args:
        product_id (int): The ID of the product to delete
        
    Returns:
        bool: True if deletion was successful
    """
    product = validate_product(product_id)
    
    if product.sale_details:
        raise Conflict(f"Cannot delete product with associated sales: {product.name}")
    
    db.session.delete(product)
    db.session.commit()
    return True
