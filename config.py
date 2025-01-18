import os

CLAVE_FILENAME = "clave.key"
LOG_DIR = "logs"
SECURITY_DIR = "security"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SECURITY_DIR, exist_ok=True)

CLAVE_PATH = os.path.join(SECURITY_DIR, CLAVE_FILENAME)