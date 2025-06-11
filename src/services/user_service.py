from src import db
from src.models import User, Role
from src.utils.validations import validate_string_field, validate_email, validate_numeric_field, validate_password
from werkzeug.exceptions import NotFound, Conflict, BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

def validate_user(user_id):
    """
    Valida que el ID de usuario sea válido y que el usuario exista.
    
    Args:
        user_id: ID del usuario a validar
    
    Returns:
        User: Objeto usuario si existe
    
    Raises:
        BadRequest: Si el ID no es un entero
        NotFound: Si el usuario no existe
    """
    if not isinstance(user_id, int):
        raise BadRequest('User ID must be an integer')
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        raise NotFound('User not found')
    return user

def validate_user_fields(**kwargs):
    """
    Valida todos los campos de un usuario.
    
    Args:
        **kwargs: Diccionario con los campos a validar (name, last_name, email, password, role_id)
    
    Raises:
        BadRequest: Si algún campo no cumple con las validaciones
    """
    validate_string_field(kwargs.get('name'), 'Name')
    validate_string_field(kwargs.get('last_name'), 'Last name')
    validate_email(kwargs.get('email'), 'Email')
    validate_numeric_field(kwargs.get('role_id'), 'Role')
    validate_password(kwargs.get('password'))

def create_user(name, last_name, email, password, role_id):
    """
    Crea un nuevo usuario en el sistema.
    
    Args:
        name: Nombre del usuario
        last_name: Apellido del usuario
        email: Correo electrónico del usuario
        password: Contraseña del usuario
        role_id: ID del rol asignado al usuario
    
    Returns:
        User: Usuario creado
    
    Raises:
        Conflict: Si el email ya existe
        NotFound: Si el rol no existe
        BadRequest: Si algún campo no cumple con las validaciones
    """
    validate_user_fields(name=name, last_name=last_name, email=email, password=password, role_id=role_id)
    
    if User.query.filter_by(email=email).first():
        raise Conflict('Email already exists')
    if Role.query.filter_by(id=role_id).first() is None:
        raise NotFound('Role not found')
    
    username = f"{name.lower().replace(' ', '.')}.{last_name.lower().replace(' ', '.')}"
    counter = 1
    while User.query.filter_by(username=username).first():
        username = f"{username}.{counter}"
        counter += 1

    hashed_password = generate_password_hash(password)
    user = User(name=name, last_name=last_name, email=email, password=hashed_password, role_id=role_id, username=username)
    db.session.add(user)
    db.session.commit()
    return user
    
def get_all_users():
    """
    Obtiene todos los usuarios del sistema.
    
    Returns:
        List[User]: Lista de todos los usuarios
    """
    return User.query.all()

def get_user_by_id(user_id):
    """
    Obtiene un usuario por su ID.
    
    Args:
        user_id: ID del usuario a buscar
    
    Returns:
        User: Usuario encontrado
    
    Raises:
        BadRequest: Si el ID no es un entero
        NotFound: Si el usuario no existe
    """
    return validate_user(user_id)

def get_user_by_username(username):
    """
    Obtiene un usuario por su nombre de usuario.
    
    Args:
        username: Nombre de usuario a buscar
    
    Returns:
        User: Usuario encontrado
    
    Raises:
        NotFound: Si el usuario no existe
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise NotFound('User not found')
    return user

def update_user(user_id, **kwargs):
    """
    Actualiza los datos de un usuario existente.
    
    Args:
        user_id: ID del usuario a actualizar
        **kwargs: Diccionario con los campos a actualizar (name, last_name, email, password, role_id)
    
    Returns:
        User: Usuario actualizado
    
    Raises:
        BadRequest: Si el ID no es un entero o algún campo no cumple con las validaciones
        NotFound: Si el usuario no existe
    """
    user = validate_user(user_id)
    validate_user_fields(**kwargs) 
      
    if 'name' in kwargs:
        user.name = kwargs['name']
    if 'last_name' in kwargs:
        user.last_name = kwargs['last_name']
    if 'email' in kwargs:
        user.email = kwargs['email']
    if 'role_id' in kwargs:
        user.role_id = kwargs['role_id']
    if 'password' in kwargs:
        user.password = generate_password_hash(kwargs['password'])
        
    db.session.commit()
    return user

def delete_user(user_id):
    """
    Elimina un usuario del sistema.
    
    Args:
        user_id: ID del usuario a eliminar
    
    Returns:
        bool: True si el usuario fue eliminado
    
    Raises:
        BadRequest: Si el ID no es un entero
        NotFound: Si el usuario no existe
    """
    user = validate_user(user_id)
    db.session.delete(user)
    db.session.commit()
    return True

def get_users_by_role(role_id):
    """
    Obtiene todos los usuarios que tienen un rol específico.
    
    Args:
        role_id: ID del rol a buscar
    
    Returns:
        List[User]: Lista de usuarios con el rol especificado
    
    Raises:
        NotFound: Si no se encuentran usuarios con ese rol
    """
    users = User.query.filter_by(role_id=role_id).all()
    if not users:
        raise NotFound('No users found for this role')
    return users

def authenticate_user(username, password):
    """
    Autentica un usuario verificando sus credenciales.
    
    Args:
        username: Nombre de usuario
        password: Contraseña del usuario
    
    Returns:
        User: Usuario autenticado
    
    Raises:
        BadRequest: Si las credenciales son inválidas
        NotFound: Si el usuario no existe
    """
    user = get_user_by_username(username)
    
    if not user or not check_password_hash(user.password, password):
        raise BadRequest('Invalid username or password')
    
    return user
