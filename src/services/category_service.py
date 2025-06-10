from src import db
from src.models import Category
from werkzeug.exceptions import NotFound, Conflict, BadRequest
from src.utils.validations import validate_string_field

def validate_category(category_id):
    """
    Validate if a category exists.
    
    Args:
        category_id (int): The ID of the category to validate
        
    Returns:
        Category: The validated category instance
        
    Raises:
        BadRequest: If category_id is not an integer
        NotFound: If category is not found
    """
    if not isinstance(category_id, int):
        raise BadRequest("Category ID must be an integer")
    
    category = Category.query.get(category_id)
    if not category:
        raise NotFound(f"Category not found: {category_id}")
    return category

def validate_category_fields(**kwargs):
    """
    Validate category fields.
    
    Args:
        **kwargs: Category fields to validate
        
    Returns:
        bool: True if all validations pass
        
    Raises:
        BadRequest: If any validation fails
        Conflict: If category name already exists
    """
    validate_string_field(kwargs.get('name'), 'Name')
    
    if 'name' in kwargs:
        existing_category = Category.query.filter_by(name=kwargs['name']).first()
        if existing_category:
            raise Conflict(f"Category already exists: {kwargs['name']}")
    
    return True

def get_all_categories():
    """
    Get all categories.
    
    Returns:
        list: List of all categories
    """
    return Category.query.all()

def get_category_by_id(category_id):
    """
    Get a category by its ID.
    
    Args:
        category_id (int): The ID of the category to get
        
    Returns:
        Category: The requested category
    """
    return validate_category(category_id)

def create_category(name, description=None):
    """
    Create a new category.
    
    Args:
        name (str): Category name
        description (str, optional): Category description. Defaults to None.
    
    Returns:
        Category: The created category instance
    """
    validate_category_fields(name=name)
    
    category = Category(
        name=name,
        description=description
    )
    
    db.session.add(category)
    db.session.commit()
    return category

def update_category(category_id, **kwargs):
    """
    Update a category.
    
    Args:
        category_id (int): The ID of the category to update
        **kwargs: Fields to update
        
    Returns:
        Category: The updated category instance
    """
    category = validate_category(category_id)
    validate_category_fields(**kwargs)
    
    if 'name' in kwargs:
        category.name = kwargs['name']
    if 'description' in kwargs:
        category.description = kwargs['description']
    
    db.session.commit()
    return category

def delete_category(category_id):
    """
    Delete a category.
    
    Args:
        category_id (int): The ID of the category to delete
        
    Returns:
        bool: True if deletion was successful
    """
    category = validate_category(category_id)
    db.session.delete(category)
    db.session.commit()
    return True 