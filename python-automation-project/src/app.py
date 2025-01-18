main
from flask import Flask, request
import subprocess
import os
import threading
from updater import update_repository
from packager import package_application
from flask import Flask, request, jsonify
import threading
import updater
import packager
version-2.1

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        if data.get('action') == 'push':
main
            threading.Thread(target=handle_push_event).start()
            return 'Processing push event', 202
    return 'Invalid request', 400

def handle_push_event():
    update_repository()
    package_application()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

            threading.Thread(target=updater.update_and_package).start()
            return jsonify({'status': 'Update and packaging started'}), 200
    return jsonify({'status': 'Invalid request'}), 400

if __name__ == '__main__':
    app.run(port=5000)
version-2.1
