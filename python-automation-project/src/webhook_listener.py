from flask import Flask, request, jsonify
import subprocess
import threading
from updater import update_repository
from packager import package_executable

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('action') == 'push':
        threading.Thread(target=handle_push_event).start()
        return jsonify({'status': 'processing'}), 202
    return jsonify({'status': 'ignored'}), 400

def handle_push_event():
    update_repository()
    package_executable()

if __name__ == '__main__':
    app.run(port=5000)