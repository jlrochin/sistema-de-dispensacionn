from sys import version
from flask import Flask, request, jsonify
import threading
from updater import update_repository
from packager import package_application

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        if data.get('action') == 'push':
            threading.Thread(target=handle_push_event).start()
            return 'Processing push event', 202
    return 'Invalid request', 400

def handle_push_event():
    update_repository()
    package_application()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
