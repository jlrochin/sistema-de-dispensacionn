import os

# Constants
CLAVE_FILENAME = "clave.key"
LOG_DIR = "logs"
SECURITY_DIR = "security"

# Create directories if they don't exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SECURITY_DIR, exist_ok=True)

# Define the path for the key file
CLAVE_PATH = os.path.join(SECURITY_DIR, CLAVE_FILENAME)