from flask import Flask, request, jsonify, send_from_directory
from sha512_custom import sha512_custom
import os

app = Flask(__name__)

# Get the absolute path to the frontend directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

@app.route('/')
def index():
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(frontend_dir, path)

@app.route('/hash', methods=['POST'])
def hash_message():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Missing "message" field'}), 400

    message = data['message'].encode('utf-8')
    digest = sha512_custom(message)
    return jsonify({'digest': digest})

if __name__ == '__main__':
    app.run(debug=True)