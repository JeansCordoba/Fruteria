from flask import Blueprint, jsonify, request
from src.services.product_service import(
    get_all_products, get_product_by_id, create_product, 
    update_product, update_stock, delete_product, 
    get_all_products_by_category)
from werkzeug.exceptions import HTTPException

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    try:
        products = get_all_products()
        return jsonify([product.to_dict() for product in products])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/products/category/<int:category_id>', methods=['GET'])
def get_products_by_category(category_id):
    try:
        products = get_all_products_by_category(category_id)
        return jsonify([product.to_dict() for product in products])
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = get_product_by_id(product_id)
        return jsonify(product.to_dict())
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['name', 'price', 'category_id', 'stock']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        product = create_product(
            name=data['name'],
            price=data['price'],
            category_id=data['category_id'],
            stock=data['stock']
        )
        return jsonify(product.to_dict()), 201
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@product_bp.route('/products/<int:product_id>', methods=['PATCH'])
def update_product_route(product_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    try:
        product = update_product(product_id, **data)
        return jsonify(product.to_dict())
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@product_bp.route('/products/<int:product_id>/stock', methods=['PUT'])
def update_stock_route(product_id):
    data = request.get_json()
    if not data or 'stock' not in data:
        return jsonify({'error': 'Stock value is required'}), 400
    
    try:
        product = update_stock(product_id, data['stock'])
        return jsonify(product.to_dict())
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    try:
        product = delete_product(product_id)
        return jsonify({'message': 'Product deleted successfully'})
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500