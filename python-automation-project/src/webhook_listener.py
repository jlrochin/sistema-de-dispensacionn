from sys import version
from flask import Flask, request, jsonify
import subprocess
import main
import os
import threading
from updater import update_repository
from packager import package_executable
version-2.1

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('action') == 'push':
    # Call the updater and packager scripts
        try:
            subprocess.run(['python', 'src/updater.py'], check=True)
            subprocess.run(['python', 'src/packager.py'], check=True)
            return jsonify({'status': 'success', 'message': 'Update and packaging triggered.'}), 200
        except subprocess.CalledProcessError as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'ignored', 'message': 'Not a push event.'}), 200

def handle_push_event():
    update_repository()
    package_executable()
version-2.1

if __name__ == '__main__':
    app.run(port=5000)