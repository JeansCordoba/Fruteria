from flask import Blueprint, jsonify, request
from src.services.client_service import (get_all_clients, get_client_by_id, create_client,update_client, delete_client, search_clients)
from werkzeug.exceptions import HTTPException

client_bp = Blueprint('client', __name__)

@client_bp.route('/clients', methods=['GET'])
def get_clients():
    try:
        clients = get_all_clients()
        return jsonify([client.to_dict() for client in clients])
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@client_bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    try:
        client = get_client_by_id(client_id)
        return jsonify(client.to_dict())
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@client_bp.route('/clients', methods=['POST'])
def create_client_route():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['name', 'last_name', 'identity_card', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        client = create_client(**data)
        return jsonify(client.to_dict()), 201
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@client_bp.route('/clients/<int:client_id>', methods=['PATCH'])
def update_client_route(client_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['name', 'last_name', 'identity_card', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        client = update_client(client_id, **data)
        return jsonify(client.to_dict())
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@client_bp.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client_route(client_id):
    try:
        client = delete_client(client_id)
        return jsonify({'message': 'Client deleted successfully'})
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@client_bp.route('/clients/search', methods=['GET'])
def search_clients_route():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['identity_card']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        identity_card = data['identity_card']
        client = search_clients(identity_card)
        return jsonify(client.to_dict())
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    