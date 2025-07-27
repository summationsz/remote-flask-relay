# relay_server.py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
connections = {}
key_logs = {}
host_commands = {}

@app.route('/connect', methods=['POST'])
def connect():
    data = request.get_json()
    host = data.get('host')
    connector = data.get('connector')

    if host not in connections:
        connections[host] = []
        key_logs[host] = []
    if connector not in connections[host]:
        connections[host].append(connector)
    return jsonify({'status': 'connected'})

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    host = data.get('host')
    connector = data.get('connector')
    key = data.get('key')

    if host in connections:
        key_logs[host].append([connector, key])
        return jsonify({'status': 'sent'})
    return jsonify({'status': 'host_not_found'}), 404

@app.route('/status/<host>', methods=['GET'])
def status(host):
    return jsonify({
        'connectors': connections.get(host, []),
        'key_logs': key_logs.get(host, [])
    })

@app.route('/poll', methods=['GET'])
def poll():
    host = request.args.get('host')
    if host not in key_logs:
        return jsonify([])

    commands = key_logs[host]
    key_logs[host] = []
    return jsonify(commands)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
