import json

from flask import Blueprint, jsonify, request

from model import Store

store_controller = Blueprint('store_controller', __name__)

@store_controller.route('', methods=['GET'])
def index():
    try:
        stores = Store.query.order_by(Store.name).all()
        return jsonify({ 'status': 'OK', 'stores': json.dumps([store.serialize() \
            for store in stores]) }), 200
    except Exception as e:
        return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

@store_controller.route('', methods=['POST'])
def create():
    try:
        store=Store(
            code= request.json['code'],
            name=request.json['name'], 
            online=request.json['online'],
            website=request.json['website'],
            longitude=request.json['longitude'],
            latitude=request.json['latitude']
        )
        database.session.add(store)
        database.session.commit()
        return jsonify({ 'status': 'OK', 'store': store.serialize() }), 201
    except Exception as e:
	    return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

@store_controller.route('/<id>', methods=['GET'])
def detail(id):
    try:
        store=Store.query.filter_by(id=id).first()

        if store:
            return jsonify({ 'status': 'OK', 'store': store.serialize() }), 200

        return jsonify({ 'status': 'NOT FOUND'}), 404
    except Exception as e:
        return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

# @store_controller.route('search/<query>', methods=['GET'])
# def search(query):
#     try:
#         store=Store.query.filter_by(code=query).first()
#         if not store:
#             store=Store.query.filter_by(name=query).first()

#         return jsonify({ 'status': 'OK', 'store': store.serialize() if store else '{}'}), 200
#     except Exception as e:
#         return jsonify({ 'status': 'ERROR', 'error': str(e) }), 404