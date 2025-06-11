from flask import Blueprint, jsonify, request
from src.services.supplier_service import ( get_all_suppliers, get_supplier_by_id, get_supplier_by_nit, 
create_supplier, update_supplier, delete_supplier )
from werkzeug.exceptions import HTTPException

supplier_bp = Blueprint('supplier', __name__)

@supplier_bp.route('/suppliers', methods=['GET'])
def get_suppliers():
    try:
        suppliers = get_all_suppliers()
        return jsonify([supplier.to_dict() for supplier in suppliers])
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@supplier_bp.route('/suppliers/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    try:
        supplier = get_supplier_by_id(supplier_id)
        return jsonify(supplier.to_dict())
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@supplier_bp.route('/suppliers/nit/<string:nit>', methods=['GET'])
def get_supplier_by_nit_route(nit):
    try:
        supplier = get_supplier_by_nit(nit)
        return jsonify(supplier.to_dict())
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@supplier_bp.route('/suppliers', methods=['POST'])
def create_supplier_route():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['name', 'phone', 'nit', 'email', 'address']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        supplier = create_supplier(data['name'], data['phone'], data['nit'], data['email'], data['address'])
        return jsonify(supplier.to_dict()), 201
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@supplier_bp.route('/suppliers/<int:supplier_id>', methods=['PATCH'])
def update_supplier_route(supplier_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        supplier = update_supplier(supplier_id, **data)
        return jsonify(supplier.to_dict())
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@supplier_bp.route('/suppliers/<int:supplier_id>', methods=['DELETE'])
def delete_supplier_route(supplier_id):
    try:
        delete_supplier(supplier_id)
        return jsonify({'message': 'Supplier deleted successfully'})
    except HTTPException as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    