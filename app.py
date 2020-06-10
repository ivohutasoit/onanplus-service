from flask import Flask, request, jsonify

app = Flask(__name__)

app.route('/', methods=['GET'])
def index(): 
    return '<h2>Welcome to OnanPlus web service</h2>'

if __name__ == '__main__':
    app.run(threaded=True, port=5000)