import json
from datetime import date
from flask import Blueprint, jsonify, request

from application import database
from model import Price, Product

product_controller = Blueprint('product_controller', __name__)

@product_controller.route('', methods=['GET'])
def index():
    try:
        products = Product.query.order_by(Product.barcode).all()
        return jsonify({ 'status': 'OK', 'products': [product.serialize() \
            for product in products] }), 200
    except Exception as e:
        return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

@product_controller.route('', methods=['POST'])
def create():
    try:
        product=Product(
            barcode= request.json['barcode'], #'9556404115044',
            name=request.json['name'], 
            manufacture=request.json['manufacture'] or None,
            detail=request.json['detail'] or None,
        )
        database.session.add(product)
        database.session.commit()
        return jsonify({ 'status': 'OK', 'product': product.serialize() }), 201
    except Exception as e:
	    return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500
    

@product_controller.route('/<id>', methods=['GET'])
def detail(id):
    """
    id can be product id or barcode
    """
    try:
        product=Product.query.filter((Product.id==int(id)) |\
            (Product.barcode==id)).first()
        if product:
            return jsonify({ 'status': 'OK', 'product': product.serialize() }), 200

        return jsonify({ 'status': 'NOT FOUND'}), 404
    except Exception as e:
        return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

@product_controller.route('/<id>/price', methods=['GET'])
def price(id):
    """
    id can be product id or barcode
    """
    try:
        product=Product.query.filter((Product.id==int(id)) |\
            (Product.barcode==id)).first()

        prices=Price.query.filter_by(product_id=product.id).\
            filter_by(active=True).\
            order_by(Price.start_date.asc(), Price.end_date.desc(), Price.amount.asc()).all()

        # sortedPrices = sorted(prices)
        
        return jsonify({ 'status': 'OK', 'prices': [price.serialize('product') \
            for price in prices] }), 200
    except Exception as e:
        return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500

# @price_controller.route('/<id>/price/cheaper', methods=['POST'])
# def cheaper(id):
#     latitude = request.json['latitude']
#     longitude = request.json['longitude']
#     try:
#         price=Price.query.filter_by(id=id).\
#             order_by(Price.date.desc()).first()

#         if price:
#             return jsonify({ 'status': 'OK', 'price': price.serialize() }), 200
        
#         return jsonify({ 'status': 'NOT FOUND'}), 404
#     except Exception as e:
#         return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500
