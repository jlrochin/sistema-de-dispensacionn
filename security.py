from cryptography.fernet import Fernet
import os
from config import CLAVE_PATH

def cargar_o_generar_clave():
    """
    Carga la clave de encriptación si existe, de lo contrario la genera y la guarda
    en el directorio definido.
    """
    if not os.path.exists(CLAVE_PATH):
        clave = Fernet.generate_key()
        with open(CLAVE_PATH, "wb") as clave_file:
            clave_file.write(clave)
    with open(CLAVE_PATH, "rb") as clave_file:
        return clave_file.read()