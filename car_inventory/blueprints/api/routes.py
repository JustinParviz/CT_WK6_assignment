from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required 

# internal import
from car_inventory.models import Customer, Car, ProdOrder, Order, db, product_schema, products_schema 


api = Blueprint('api', __name__, url_prefix='/api') # every route needs to be preceeded with /api


@api.route('/token', methods=['GET', 'POST'])
def token():
    
    data = request.json # building api requests no () 
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id)
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status': 400,
            'message': 'Missing Client Id. Try Again.'
        }