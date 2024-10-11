from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
registered = False

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not all([hostname, ip, as_ip, as_port]):
        return 'Bad Request: Missing registration data', 400

    try:
        as_port = int(as_port)
    except ValueError:
        return 'Bad Request: Invalid AS port', 400

    # Register with AS
    try:
        registration_data = {
            'hostname': hostname,
            'value': ip,
            'type': 'A',
            'ttl': 10
        }
        response = requests.post(f'http://{as_ip}:{as_port}/register', json=registration_data)
        if response.status_code != 201:
            return 'Registration with AS failed', 500
    except Exception:
        return 'Error communicating with AS', 500

    global registered
    registered = True
    return '', 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    if number is None:
        return 'Bad Request: Missing number parameter', 400

    try:
        number = int(number)
        if number < 0:
            return 'Bad Request: Number must be non-negative', 400
    except ValueError:
        return 'Bad Request: Invalid number', 400
        
    a, b = 0, 1
    for _ in range(number):
        a, b = b, a + b

    return jsonify({'result': a}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
