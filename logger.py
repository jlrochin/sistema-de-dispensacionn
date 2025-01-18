from datetime import datetime
import json
from cryptography.fernet import Fernet
import os

from config import CLAVE_PATH, LOG_DIR
from security import cargar_o_generar_clave

def log_message(log_dict, level, message):
    if log_dict is not None:
        if message in log_dict:
            return
        log_dict[message] = True
    print(f"[{level}] {message}")
    guardar_log_incremental("usuario_demo", log_dict)

def guardar_log_incremental(usuario, log_dict):
    clave = cargar_o_generar_clave()
    cifrador = Fernet(clave)
    log_data = {
        "usuario": usuario,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S"),
        "log": log_dict,
    }
    log_texto = json.dumps(log_data, indent=4)
    log_cifrado = cifrador.encrypt(log_texto.encode())
    temp_log_path = os.path.join(LOG_DIR, "log_temp.log")
    with open(temp_log_path, "wb") as archivo:
        archivo.write(log_cifrado)

def finalizar_log_definitivo(usuario, log_dict):
    try:
        archivo_final = os.path.join(
            LOG_DIR, f"log_{usuario} {datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.log"
        )
        clave = cargar_o_generar_clave()
        cifrador = Fernet(clave)
        log_data = {
            "usuario": usuario,
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "hora": datetime.now().strftime("%H:%M:%S"),
            "log": log_dict,
        }
        log_texto = json.dumps(log_data, indent=4)
        log_cifrado = cifrador.encrypt(log_texto.encode())
        with open(archivo_final, "wb") as archivo:
            archivo.write(log_cifrado)
    except Exception as e:
        print(f"[ERROR] {e}")