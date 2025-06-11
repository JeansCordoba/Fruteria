from src import db
from src.models import Supplier
from werkzeug.exceptions import NotFound, Conflict, BadRequest
from src.utils.validations import (
    validate_string_field,
    validate_phone,
    validate_email,
    validate_address
)

def validate_nit(nit):
    """
    Validate NIT format.
    
    Args:
        nit (str): NIT to validate
        
    Raises:
        BadRequest: If NIT format is invalid
    """
    if not nit or not nit.strip():
        raise BadRequest("NIT cannot be empty")
    if not isinstance(nit, str):
        raise BadRequest("NIT must be a string")
    if not (10 <= len(nit) <= 11):
        raise BadRequest("NIT must have between 10 and 11 characters")
    if not nit.isdigit():
        raise BadRequest("NIT must contain only digits")

def validate_supplier(supplier_id):
    """
    Validate if a supplier exists.
    
    Args:
        supplier_id (int): The ID of the supplier to validate
        
    Returns:
        Supplier: The validated supplier instance
        
    Raises:
        BadRequest: If supplier_id is not an integer
        NotFound: If supplier is not found
    """
    if not isinstance(supplier_id, int):
        raise BadRequest("Supplier ID must be an integer")
    
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        raise NotFound(f"Supplier not found: {supplier_id}")
    return supplier

def validate_supplier_fields(**kwargs):
    """
    Validate supplier fields.
    
    Args:
        **kwargs: Supplier fields to validate
        
    Returns:
        bool: True if all validations pass
        
    Raises:
        BadRequest: If any validation fails
        Conflict: If supplier name or NIT already exists
    """
    validate_string_field(kwargs.get('name'), 'Name')
    validate_phone(kwargs.get('phone'))
    validate_email(kwargs.get('email'), required=True)
    validate_address(kwargs.get('address'), required=True)
    
    if 'nit' in kwargs:
        validate_nit(kwargs['nit'])
        existing_supplier = Supplier.query.filter_by(nit=kwargs['nit']).first()
        if existing_supplier:
            raise Conflict(f"Supplier with NIT already exists: {kwargs['nit']}")
    
    if 'name' in kwargs:
        existing_supplier = Supplier.query.filter_by(name=kwargs['name']).first()
        if existing_supplier:
            raise Conflict(f"Supplier already exists: {kwargs['name']}")
    
    return True

def get_all_suppliers():
    """
    Get all suppliers.
    
    Returns:
        list: List of all suppliers
    """
    return Supplier.query.all()

def get_supplier_by_id(supplier_id):
    """
    Get a supplier by its ID.
    
    Args:
        supplier_id (int): The ID of the supplier to get
        
    Returns:
        Supplier: The requested supplier
    """
    return validate_supplier(supplier_id)

def get_supplier_by_nit(nit):
    supplier = Supplier.query.filter_by(nit=nit).first()
    if not supplier:
        raise NotFound(f"Supplier not found: {nit}")
    return supplier

def create_supplier(name, phone, nit, email, address):
    """
    Create a new supplier.
    
    Args:
        name (str): Supplier name
        phone (str): Supplier phone number
        nit (str): Supplier NIT (tax ID)
        email (str): Supplier email address
        address (str): Supplier address
    
    Returns:
        Supplier: The created supplier instance
    """
    validate_supplier_fields(
        name=name,
        phone=phone,
        nit=nit,
        email=email,
        address=address
    )
    
    supplier = Supplier(
        name=name,
        phone=phone,
        nit=nit,
        email=email,
        address=address
    )
    
    db.session.add(supplier)
    db.session.commit()
    return supplier

def update_supplier(supplier_id, **kwargs):
    """
    Update a supplier.
    
    Args:
        supplier_id (int): The ID of the supplier to update
        **kwargs: Fields to update
        
    Returns:
        Supplier: The updated supplier instance
    """
    supplier = validate_supplier(supplier_id)
    validate_supplier_fields(**kwargs)
    
    if 'name' in kwargs:
        supplier.name = kwargs['name']
    if 'phone' in kwargs:
        supplier.phone = kwargs['phone']
    if 'nit' in kwargs:
        supplier.nit = kwargs['nit']
    if 'email' in kwargs:
        supplier.email = kwargs['email']
    if 'address' in kwargs:
        supplier.address = kwargs['address']
    
    db.session.commit()
    return supplier

def delete_supplier(supplier_id):
    """
    Delete a supplier.
    
    Args:
        supplier_id (int): The ID of the supplier to delete
        
    Returns:
        bool: True if deletion was successful
    """
    supplier = validate_supplier(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    return True
