from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return 'Bad Request: Missing parameters', 400

    # Validate ports and number
    try:
        fs_port = int(fs_port)
        as_port = int(as_port)
        number = int(number)
    except ValueError:
        return 'Bad Request: Invalid port or number', 400

    try:
        dns_query = {'name': hostname, 'type': 'A'}
        response = requests.get(f'http://{as_ip}:{as_port}/dns-query', params=dns_query)
        if response.status_code != 200:
            return 'Hostname resolution failed', 500
        ip_address = response.json().get('value')
        if not ip_address:
            return 'Hostname not found', 404
    except Exception:
        return 'Error communicating with AS', 500

    print("Query Successful")
    
    try:
        fib_response = requests.get(f'http://{ip_address}:{fs_port}/fibonacci', params={'number': number})
        if fib_response.status_code != 200:
            return 'Error retrieving Fibonacci number', 500
        result = fib_response.json().get('result')
        return jsonify({'result': result}), 200
    except Exception:
        return 'Error communicating with FS', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
