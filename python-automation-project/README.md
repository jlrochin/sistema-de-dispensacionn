# Python Automation Project

This project automates the update and packaging process of a `.exe` file generated with PyInstaller. It includes a Flask server that listens for GitHub Webhook events to trigger updates and packaging.

## Project Structure

```
python-automation-project
├── src
│   ├── app.py               # Main entry point of the application
│   ├── updater.py           # Logic to update the local repository
│   ├── packager.py          # Handles the packaging process with PyInstaller
│   ├── webhook_listener.py   # Listens for GitHub Webhook events
│   └── templates
│       └── index.html       # HTML template for web interface and notifications
├── requirements.txt         # Project dependencies
├── pyinstaller.spec         # PyInstaller configuration file
└── README.md                # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd python-automation-project
   ```

2. **Install dependencies:**
   Make sure you have Python installed. Then, install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask server:**
   Start the Flask server by running:
   ```bash
   python src/app.py
   ```

4. **Configure GitHub Webhooks:**
   Set up a webhook in your GitHub repository to point to your Flask server's endpoint (e.g., `http://<your-server>:<port>/webhook`).

## Usage

- When a `push` event is received from GitHub, the Flask server will trigger the update process, pulling the latest changes from the repository.
- After updating, it will initiate the packaging process to create a new `.exe` file using PyInstaller.

## Notes

- Ensure that the `.exe` file is not running during the packaging process to avoid conflicts.
- Modify the `pyinstaller.spec` file as needed to customize the build process.
- Update the `requirements.txt` file to include any additional dependencies.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
