from flask import Flask, request, jsonify
import subprocess
import os

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
    return jsonify({'status': 'ignored', 'message': 'Not a push event.'}), 200

if __name__ == '__main__':
    app.run(port=5000)