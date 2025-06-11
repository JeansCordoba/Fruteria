from src import db 
from src.models import Client
from werkzeug.exceptions import NotFound, Conflict, BadRequest
from src.utils.validations import (
    validate_string_field,
    validate_phone,
    validate_email,
    validate_identity_card,
    validate_address
)

def validate_client(client_id):
    """
    Valida que el ID de cliente sea válido y que el cliente exista.
    
    Args:
        client_id: ID del cliente a validar
    
    Returns:
        Client: Objeto cliente si existe
    
    Raises:
        BadRequest: Si el ID no es un entero
        NotFound: Si el cliente no existe
    """
    if not isinstance(client_id, int):
        raise BadRequest("Client ID must be an integer")
    
    client = Client.query.get(client_id)
    if not client:
        raise NotFound(f"Client not found: {client_id}")
    return client

def validate_client_fields(**kwargs):
    """
    Valida todos los campos de un cliente.
    
    Args:
        **kwargs: Diccionario con los campos a validar (name, last_name, phone, identity_card, email, address)
    
    Returns:
        bool: True si todas las validaciones son exitosas
    
    Raises:
        BadRequest: Si algún campo no cumple con las validaciones
        Conflict: Si el número de identidad ya existe
    """
    validate_string_field(kwargs.get('name'), 'Name')
    validate_string_field(kwargs.get('last_name'), 'Last name')
    validate_phone(kwargs.get('phone'))
    validate_identity_card(kwargs.get('identity_card'))
    validate_email(kwargs.get('email'), required=False)
    validate_address(kwargs.get('address'), required=False)
    
    # Validar duplicados
    if 'identity_card' in kwargs:
        existing_client = Client.query.filter_by(identity_card=kwargs['identity_card']).first()
        if existing_client:
            raise Conflict(f"Client already exists: {kwargs['identity_card']}")
    
    return True

def get_all_clients():
    """
    Obtiene todos los clientes del sistema.
    
    Returns:
        List[Client]: Lista de todos los clientes
    """
    return Client.query.all()

def get_client_by_id(client_id):
    """
    Obtiene un cliente por su ID.
    
    Args:
        client_id: ID del cliente a buscar
    
    Returns:
        Client: Cliente encontrado
    
    Raises:
        BadRequest: Si el ID no es un entero
        NotFound: Si el cliente no existe
    """
    return validate_client(client_id)

def search_clients(identity_card):
    """
    Busca un cliente por su número de identidad.
    
    Args:
        identity_card: Número de identidad del cliente a buscar
    
    Returns:
        Client: Cliente encontrado
    
    Raises:
        NotFound: Si el cliente no existe
    """
    client = Client.query.filter_by(identity_card=identity_card).first()
    if not client:
        raise NotFound(f"Client not found: {identity_card}")
    return client

def create_client(name, last_name, identity_card, phone, email=None, address=None):
    """
    Crea un nuevo cliente en el sistema.
    
    Args:
        name: Nombre del cliente
        last_name: Apellido del cliente
        identity_card: Número de identidad del cliente
        phone: Número de teléfono del cliente
        email: Correo electrónico del cliente (opcional)
        address: Dirección del cliente (opcional)
    
    Returns:
        Client: Cliente creado
    
    Raises:
        BadRequest: Si algún campo no cumple con las validaciones
        Conflict: Si el número de identidad ya existe
    """
    validate_client_fields(
        name=name,
        last_name=last_name,
        identity_card=identity_card,
        phone=phone,
        email=email,
        address=address
    )
    
    client = Client(
        name=name,
        last_name=last_name,
        identity_card=identity_card,
        phone=phone,
        email=email,
        address=address
    )
    
    db.session.add(client)
    db.session.commit()
    return client

def update_client(client_id, **kwargs):
    """
    Actualiza los datos de un cliente existente.
    
    Args:
        client_id: ID del cliente a actualizar
        **kwargs: Diccionario con los campos a actualizar (name, last_name, phone, identity_card, email, address)
    
    Returns:
        Client: Cliente actualizado
    
    Raises:
        BadRequest: Si el ID no es un entero o algún campo no cumple con las validaciones
        NotFound: Si el cliente no existe
        Conflict: Si el nuevo número de identidad ya existe
    """
    client = validate_client(client_id)
    validate_client_fields(**kwargs)
    
    if 'name' in kwargs:
        client.name = kwargs['name']
    if 'last_name' in kwargs:
        client.last_name = kwargs['last_name']
    if 'phone' in kwargs:
        client.phone = kwargs['phone']
    if 'identity_card' in kwargs:
        client.identity_card = kwargs['identity_card']
    if 'email' in kwargs:
        client.email = kwargs['email']
    if 'address' in kwargs:
        client.address = kwargs['address']
    
    db.session.commit()
    return client

def delete_client(client_id):
    """
    Elimina un cliente del sistema.
    
    Args:
        client_id: ID del cliente a eliminar
    
    Returns:
        bool: True si el cliente fue eliminado
    
    Raises:
        BadRequest: Si el ID no es un entero
        NotFound: Si el cliente no existe
    """
    client = validate_client(client_id)
    db.session.delete(client)
    db.session.commit()
    return True
