from flask import Blueprint, jsonify, request

from application import database
from model import Price

price_controller = Blueprint('price_controller', __name__)

@price_controller.route('', methods=['POST'])
def create():
    try:
        price = Price(
            seller=request.json['seller'],
            product_id=request.json['product'],
            store_id=request.json['store'],
            normal=request.json['normal'],
            promo=request.json['promo'],
            promo_start=request.json['promo_start'],
            promo_end=request.json['promo_end'],
        )
        database.session.add(price)
        database.session.commit()
        return jsonify({ 'status': 'OK', 'price': price.serialize() }), 201
    except Exception as e:
        return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

@price_controller.route('/<id>', methods=['GET'])
def detail(id): 
    try:
        price=Price.query.filter_by(id=id).\
            order_by(Price.date.desc()).first()

        if price:
            return jsonify({ 'status': 'OK', 'price': price.serialize() }), 200
        
        return jsonify({ 'status': 'NOT FOUND'}), 404
    except Exception as e:
        return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

@price_controller.route('/by/<product>/<store>', methods=['GET'])
def by(product, store):
    try:
        prices=Price.query.filter_by(product_id=product).\
            filter_by(store_id=store).\
                order_by(Price.date.desc()).all()

        return jsonify({ 'status': 'OK', 'prices': [price.serialize() \
            for price in price] }), 200
    except Exception as e:
        return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500