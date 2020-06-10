from flask import Flask, request, jsonify
from controller import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index(): 
    return jsonify({'name': 'CatatHarga Web Service', 'version': '1.0.0', 'end_point': 'https://opservice.herokuapp.com/api/v1', 'copyright': 2020, 'company': 'Softh Axi Inc.'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

app.register_blueprint(product_controller, url_prefix='/api/v1/product')

if __name__ == '__main__':
    app.run(threaded=True)