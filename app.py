import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from application import database, environments
from controller import *

load_dotenv()
app = Flask(__name__)
app.config.from_object(environments[os.getenv('FLASK_ENV')])

database.init_app(app)

@app.route('/', methods=['GET'])
def index(): 
    return jsonify({'name': 'OnanPlus Web Service', 'version': '1.0.0', 'end_point': 'https://opservice.herokuapp.com/api/v1', 'copyright': 2020, 'company': 'Softh Axi Inc.'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

app.register_blueprint(product_controller, url_prefix='/api/v1/product')

if __name__ == '__main__':
    app.run(threaded=True)