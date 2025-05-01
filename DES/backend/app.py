from flask import Flask, request, jsonify, send_from_directory
from des_implementation import DES
import re
import os

app = Flask(__name__, static_folder='../frontend')
des = DES()

BINARY_64_RE = re.compile(r'^[01]{64}$')

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        data = request.get_json()
        plaintext = data.get('plaintext')
        key       = data.get('key')           # already binary (or None)

        if not plaintext:
            return jsonify({'error': 'Plaintext is required'}), 400

        # ① validate/optionally generate key
        if key:
            if not BINARY_64_RE.fullmatch(key):
                return jsonify({'error': 'Key must be a 64-bit binary string'}), 400
        else:
            key = des._generate_random_key()

        # ② encrypt
        encrypted = des.encrypt(plaintext, key, 'text', 'hex')

        return jsonify({'encrypted': encrypted, 'key': key})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext')
        key        = data.get('key')

        if not ciphertext:
            return jsonify({'error': 'Ciphertext is required'}), 400
        if not key:
            return jsonify({'error': 'Key is required for decryption'}), 400
        if not BINARY_64_RE.fullmatch(key):
            return jsonify({'error': 'Key must be a 64-bit binary string'}), 400

        decrypted = des.decrypt(ciphertext, key, 'hex', 'text')
        return jsonify({'decrypted': decrypted})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
