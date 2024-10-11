from flask import Flask, request, jsonify

app = Flask(__name__)
dns_records = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    value = data.get('value')
    record_type = data.get('type')
    ttl = data.get('ttl')

    if not all([hostname, value, record_type, ttl]):
        return 'Bad Request: Missing registration data', 400

    dns_records[hostname] = {
        'value': value,
        'type': record_type,
        'ttl': ttl
    }

    return '', 201

@app.route('/dns-query', methods=['GET'])
def dns_query():
    hostname = request.args.get('name')
    record_type = request.args.get('type')

    if not all([hostname, record_type]):
        return 'Bad Request: Missing query parameters', 400

    record = dns_records.get(hostname)
    if record and record.get('type') == record_type:
        return jsonify(record), 200
    else:
        return 'Record not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=53533)
