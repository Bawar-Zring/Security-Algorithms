from flask import Flask, request, jsonify
from sha512_custom import sha512_custom

app = Flask(__name__)

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
