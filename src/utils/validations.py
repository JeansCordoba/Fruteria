from werkzeug.exceptions import BadRequest

def validate_string_field(value, field_name, max_length=50, required=True):
    """
    Valida un campo de tipo string.
    
    Args:
        value: Valor a validar
        field_name: Nombre del campo para mensajes de error
        max_length: Longitud máxima permitida
        required: Si el campo es requerido
    
    Returns:
        bool: True si la validación es exitosa
    
    Raises:
        BadRequest: Si la validación falla
    """
    if required and (not value or not value.strip()):
        raise BadRequest(f"{field_name} cannot be empty")
    if value:
        if not isinstance(value, str):
            raise BadRequest(f"{field_name} must be a string")
        if len(value) > max_length:
            raise BadRequest(f"{field_name} must have less than {max_length} characters")
    return True

def validate_phone(phone, required=True):
    """
    Valida un número de teléfono.
    
    Args:
        phone: Número de teléfono a validar
        required: Si el campo es requerido
    
    Returns:
        bool: True si la validación es exitosa
    
    Raises:
        BadRequest: Si la validación falla
    """
    if required and (not phone or not phone.strip()):
        raise BadRequest("Phone cannot be empty")
    if phone:
        if not isinstance(phone, str):
            raise BadRequest("Phone must be a string")
        if not phone.isdigit():
            raise BadRequest("Phone must contain only digits")
        if len(phone) > 10:
            raise BadRequest("Phone must have less than 10 digits")
    return True

def validate_email(email, required=True):
    """
    Valida un correo electrónico.
    
    Args:
        email: Email a validar
        required: Si el campo es requerido
    
    Returns:
        bool: True si la validación es exitosa
    
    Raises:
        BadRequest: Si la validación falla
    """
    if required and (not email or not email.strip()):
        raise BadRequest("Email cannot be empty")
    if email:
        if not isinstance(email, str):
            raise BadRequest("Email must be a string")
        if not '@' in email:
            raise BadRequest("Invalid email format")
        if len(email) > 50:
            raise BadRequest("Email must have less than 50 characters")
    return True

def validate_numeric_field(value, field_name, min_value=0, required=True):
    """
    Valida un campo numérico.
    
    Args:
        value: Valor a validar
        field_name: Nombre del campo para mensajes de error
        min_value: Valor mínimo permitido
        required: Si el campo es requerido
    
    Returns:
        bool: True si la validación es exitosa
    
    Raises:
        BadRequest: Si la validación falla
    """
    if required and value is None:
        raise BadRequest(f"{field_name} is required")
    if value is not None:
        if not isinstance(value, (int, float)):
            raise BadRequest(f"{field_name} must be a number")
        if value < min_value:
            raise BadRequest(f"{field_name} must be greater than or equal to {min_value}")
    return True

def validate_identity_card(identity_card, required=True):
    """
    Valida un número de identidad (DNI/RUC).
    
    Args:
        identity_card: Número de identidad a validar
        required: Si el campo es requerido
    
    Returns:
        bool: True si la validación es exitosa
    
    Raises:
        BadRequest: Si la validación falla
    """
    if required and (not identity_card or not identity_card.strip()):
        raise BadRequest("Identity card cannot be empty")
    if identity_card:
        if not isinstance(identity_card, str):
            raise BadRequest("Identity card must be a string")
        if not identity_card.isdigit():
            raise BadRequest("Identity card must contain only digits")
        if not (8 <= len(identity_card) <= 11):
            raise BadRequest("Identity card must have between 8 and 11 digits")
    return True

def validate_address(address, required=True):
    """
    Valida una dirección.
    
    Args:
        address: Dirección a validar
        required: Si el campo es requerido
    
    Returns:
        bool: True si la validación es exitosa
    
    Raises:
        BadRequest: Si la validación falla
    """
    if required and (not address or not address.strip()):
        raise BadRequest("Address cannot be empty")
    if address:
        if not isinstance(address, str):
            raise BadRequest("Address must be a string")
        if len(address) > 100:
            raise BadRequest("Address must have less than 100 characters")
    return True 