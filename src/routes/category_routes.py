from flask import Blueprint, jsonify, request
from src.services.category_service import get_all_categories, get_category_by_id, create_category, update_category, delete_category
from werkzeug.exceptions import HTTPException

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = get_all_categories()
        return jsonify([category.to_dict() for category in categories])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        category = get_category_by_id(category_id)
        return jsonify(category.to_dict())
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    try:
        category = create_category(data['name'])
        return jsonify(category.to_dict()), 201
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
def modify_category(category_id):
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    try:
        category = update_category(category_id, data['name'])
        return jsonify(category.to_dict())
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def remove_category(category_id):
    try:
        category = delete_category(category_id)
        return jsonify({'message': 'Category deleted successfully'})
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500 