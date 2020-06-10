from flask import Flask, request, jsonify

app = Flask(__name__)

app.route('/', methods=['GET'])
def index(): 
    return '<h2>Welcome to OnanPlus web service</h2>'

app.route('/api/v1/product', methods=['GET'])
def products():
    return '<h2>List of product</h2>'

if __name__ == '__main__':
    app.run(threaded=True)