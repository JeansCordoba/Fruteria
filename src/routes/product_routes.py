from flask import Blueprint, jsonify, request
from src.services.product_service import(
    get_all_products, get_product_by_id, create_product, 
    update_product, update_stock, delete_product, 
    get_all_products_by_category)

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = get_all_products()
    return jsonify([product.to_dict() for product in products])

@product_bp.route('/products/category/<int:category_id>', methods=['GET'])
def get_products_by_category(category_id):
    products = get_all_products_by_category(category_id)
    return jsonify([product.to_dict() for product in products])

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = get_product_by_id(product_id)
    return jsonify(product.to_dict())

@product_bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    try:
        product = create_product(
            name=data['name'],
            price=data['price'],
            category_id=data['category_id'],
            stock=data['stock']
        )
        return jsonify(product.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
@product_bp.route('/products/<int:product_id>', methods = ['PATCH'])
def update_product_route(product_id):
    data = request.get_json()
    try:
        product = update_product(product_id, **data)
        return jsonify(product.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
@product_bp.route('/products/<int:product_id>/stock', methods = ['PATCH'])
def update_stock_route(product_id):
    data = request.get_json()
    try:
        product = update_stock(product_id, data['stock'])
        return jsonify(product.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
@product_bp.route('/products/<int:product_id>', methods = ['DELETE'])
def delete_product_route(product_id):
    try:
        product = delete_product(product_id)
        return jsonify(product.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400