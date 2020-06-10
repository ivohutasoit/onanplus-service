from flask import Blueprint, jsonify, request

product_controller = Blueprint('product_controller', __name__)

@product_controller.route('', methods=['GET'])
def index():
    return jsonify({ 'status': 'OK', 'products': [] }), 200

@product_controller.route('/<id>', methods=['GET'])
def detail(id):
    # try:
    #     product=Product.query.filter((Product.id==id) | (Product.barcode==id | (Product.name==id))).first()
    #     if product:
    #         prices = {} # sort price normal and promo asc
    #         product.set_prices(prices) 
    #     return jsonify({ 'status': 'OK', 'product': product.serialize() if product else '{}'}), 200
    # except Exception as e:
    #     return jsonify({ 'status': 'ERROR', 'error': str(e) }), 404
    return jsonify({ 'status': 'OK', 'product': { 'id': id, 'name': 'product ' + id } }), 200

@product_controller.route('', methods=['POST'])
def create():
    # try:
    #     product=Product(
    #         barcode= request.json['barcode'], #'9556404115044',
    #         name=request.json['name'], 
    #     )
    #     database.session.add(product)
    #     database.session.commit()
    #     return jsonify({ 'status': 'OK', 'product': product.serialize() }), 201
    # except Exception as e:
	#     return jsonify({ 'status': 'ERROR', 'error': str(e) }), 500
    return jsonify({ 'status': 'OK', 'product': [] }), 201