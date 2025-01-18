from main import flujo_principal
from utils import obtener_credenciales_y_opcion

if __name__ == "__main__":
    usuario, contraseña, opcion = obtener_credenciales_y_opcion()
    base_url = "https://172.18.28.101/emotion/index.xhtml"
    flujo_principal(usuario, contraseña, opcion, base_url)