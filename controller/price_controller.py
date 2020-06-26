from datetime import date
from flask import Blueprint, jsonify, request

from application import database
from model import Price

price_controller = Blueprint('price_controller', __name__)

@price_controller.route('', methods=['POST'])
def create():
    try:
        price = Price(
            sku=request.json['sku'],
            seller=request.json['seller'],
            product_id=request.json['product_id'],
            store_id=request.json['store_id'],
            promotion=request.json['promotion'] or False,
            unit=request.json['unit'] or 'PC',
            currency=request.json['currency'] or 'MYR',
            amount=request.json['amount'] or 0
        )
        price.start_date = date.today()
        price.active = True

        latestPrice = Price.query.filter((Price.promotion==price.promotion) &\
            (Price.product_id==price.product_id) & (Price.unit==price.unit) &\
            (Price.store_id==price.store_id) & (Price.active == True)).first()

        if latestPrice:
            latestPrice.active = False
            latestPrice.end_date = date.today()
            database.session.commit()
        
        database.session.add(price)
        database.session.commit()
        return jsonify({ 'status': 'OK', 'price': price.serialize() }), 201
    except Exception as e:
        return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

@price_controller.route('/<id>', methods=['GET'])
def detail(id): 
    try:
        price=Price.query.filter(id=id).first()

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