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
    if not isinstance(client_id, int):
        raise BadRequest("Client ID must be an integer")
    
    client = Client.query.get(client_id)
    if not client:
        raise NotFound(f"Client not found: {client_id}")
    return client

def validate_client_fields(**kwargs):
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
    return Client.query.all()

def get_client_by_id(client_id):
    return validate_client(client_id)

def search_clients(identity_card):
    client = Client.query.filter_by(identity_card=identity_card).first()
    if not client:
        raise NotFound(f"Client not found: {identity_card}")
    return client

def create_client(name, last_name, identity_card, phone, email=None, address=None):
    """
    Create a new client.
    
    Args:
        name (str): Client's name
        last_name (str): Client's last name
        identity_card (str): Client's identity card number
        phone (str): Client's phone number
        email (str, optional): Client's email address. Defaults to None.
        address (str, optional): Client's address. Defaults to None.
    
    Returns:
        Client: The created client instance
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
    client = validate_client(client_id)
    db.session.delete(client)
    db.session.commit()
    return True
