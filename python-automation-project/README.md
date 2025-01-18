# python-automation-project/python-automation-project/README.md

# Python Automation Project

This project automates the update and packaging process of a `.exe` file generated with PyInstaller. It includes a Flask server that listens for GitHub Webhook events to trigger updates and packaging.

## Project Structure

```
python-automation-project
├── src
│   ├── app.py               # Main entry point of the application
│   ├── updater.py           # Logic to update the local repository
│   ├── packager.py          # Handles packaging with PyInstaller
│   ├── webhook_listener.py   # Listens for GitHub Webhook events
│   └── templates
│       └── index.html       # HTML template for web interface
├── requirements.txt         # Project dependencies
├── pyinstaller.spec         # Configuration for PyInstaller
└── README.md                # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-automation-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your GitHub repository to send Webhook events to your Flask server.

## Usage

1. Start the Flask server:
   ```
   python src/app.py
   ```

2. The server will listen for incoming Webhook events. Upon receiving a `push` event, it will trigger the update and packaging process.

## Notes

- Ensure that the `.exe` file is not running before the packaging process starts.
- Modify the `pyinstaller.spec` file as needed to customize the build process.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.