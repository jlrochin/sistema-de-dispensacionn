from flask import Flask, request, jsonify
import threading
import updater
import packager

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        if data.get('action') == 'push':
            threading.Thread(target=updater.update_and_package).start()
            return jsonify({'status': 'Update and packaging started'}), 200
    return jsonify({'status': 'Invalid request'}), 400

if __name__ == '__main__':
    app.run(port=5000)