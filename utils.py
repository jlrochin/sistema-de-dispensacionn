import msvcrt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from logger import log_message

def safe_find_element(driver, xpath, default_value="", modo=None, log_dict=None):
    try:
        if modo == "clickable":
            elemento = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            if log_dict:
                log_message(log_dict, "INFO", "Elemento listo para clic.")
            return elemento
        elif modo == "visible":
            elemento = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            if log_dict:
                log_message(log_dict, "INFO", "Elemento visible encontrado.")
            return elemento
        else:
            elemento = driver.find_element(By.XPATH, xpath)
            if elemento:
                if log_dict:
                    log_message(log_dict, "SUCCESS", "Elemento encontrado correctamente.")
            return elemento.text if elemento else default_value
    except Exception:
        if log_dict:
            log_message(log_dict, "ERROR", "No se pudo encontrar el elemento.")
        return default_value if modo is None else None

def input_con_asteriscos(prompt):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        char = msvcrt.getch()
        if char == b"\r":
            print("")
            break
        elif char == b"\x08":
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        else:
            password += char.decode("utf-8")
            print("*", end="", flush=True)
    return password

def obtener_credenciales_y_opcion(log_dict=None):
    try:
        if log_dict:
            log_message(log_dict, "INFO", "Solicitando usuario...")
        usuario = input("Ingresa el usuario: ").strip()
        if log_dict:
            log_message(log_dict, "INFO", "Solicitando contraseña...")
        password = input_con_asteriscos("Ingresa la contraseña: ")
        if log_dict:
            log_message(log_dict, "INFO", "Mostrando opciones de mezcla al usuario.")
        print("1. Solo ONC")
        print("2. Solo ANT")
        print("3. Ambos (ONC y ANT)")
        opcion = input("Selecciona el número de la opción: ").strip()
        while opcion not in ["1", "2", "3"]:
            if log_dict:
                log_message(log_dict, "WARNING", "Opción no válida ingresada por el usuario.")
            opcion = input("Selecciona una opción válida (1, 2, 3): ").strip()
        if log_dict:
            log_message(log_dict, "SUCCESS", "Credenciales y opción obtenidas correctamente.")
        return usuario, password, opcion
    except Exception:
        if log_dict:
            log_message(log_dict, "ERROR", "Error al obtener credenciales y opción.")
        return None, None, None

def capturar_primero_valido(driver, xpath_list, default_value=""):
    for xpath in xpath_list:
        try:
            elemento = driver.find_element(By.XPATH, xpath)
            if elemento:
                return elemento.text
        except Exception:
            continue
    return default_value

def verificar_tabla_registros(driver, log_dict=None):
    try:
        filas_xpath = '//*[@id="mainForm:tblSurtimientos_data"]/tr'
        filas = driver.find_elements(By.XPATH, filas_xpath)
        if not filas:
            if log_dict:
                log_message(log_dict, "WARNING", "La tabla parece estar vacía. No se encontraron filas.")
            return False
        primera_celda_xpath = '//*[@id="mainForm:tblSurtimientos_data"]/tr/td'
        primera_celda = driver.find_element(By.XPATH, primera_celda_xpath).text
        if "No se encontraron Registros" in primera_celda:
            if log_dict:
                log_message(log_dict, "WARNING", "No se encontraron registros en la tabla.")
            return False
        if log_dict:
            log_message(log_dict, "SUCCESS", "Se encontraron registros válidos en la tabla.")
        return True
    except Exception:
        if log_dict:
            log_message(log_dict, "ERROR", "Error al verificar la tabla de registros.")
        return False

def obtener_filas_procesables(driver, opcion, log_dict=None):
    try:
        filas_xpath = '//*[@id="mainForm:tblSurtimientos_data"]/tr'
        filas = driver.find_elements(By.XPATH, filas_xpath)
        if not filas or len(filas) == 0:
            if log_dict:
                log_message(log_dict, "INFO", "No se encontraron registros en la tabla.")
            return []
        conteo_tipos = {"ONC": 0, "ANT": 0, "NPT": 0}
        filas_procesables = []
        opcion_tipo = {"1": "ONC", "2": "ANT", "3": "AMBOS", "4": "NPT"}
        tipo_requerido = opcion_tipo.get(opcion, None)
        if tipo_requerido is None:
            if log_dict:
                log_message(log_dict, "ERROR", f"Opción inválida: {opcion}. No se puede filtrar filas.")
            return []
        for i, fila in enumerate(filas, start=1):
            tipo_xpath = f'//*[@id="mainForm:tblSurtimientos_data"]/tr[{i}]/td[2]'
            intento = 0
            while intento < 3:
                try:
                    tipo_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, tipo_xpath))
                    )
                    tipo = tipo_element.get_attribute("innerText").strip()
                    if tipo in conteo_tipos:
                        conteo_tipos[tipo] += 1
                    if tipo_requerido != "AMBOS" and tipo != tipo_requerido:
                        break
                    filas_procesables.append((i, tipo))
                    break
                except StaleElementReferenceException:
                    intento += 1
                except Exception:
                    break
        if len(filas_procesables) == 0:
            if log_dict:
                log_message(log_dict, "INFO", "No se encontraron filas procesables después de evaluar la tabla.")
        if log_dict:
            log_message(
                log_dict,
                "INFO",
                f"Se encontraron {conteo_tipos['ONC']} filas de tipo 'ONC', {conteo_tipos['ANT']} de tipo 'ANT', "
                f"y {conteo_tipos['NPT']} de tipo 'NPT' en la tabla."
            )
        if log_dict:
            log_message(log_dict, "INFO", f"Total de filas procesables para la opción seleccionada ({tipo_requerido}): {len(filas_procesables)}.")
        return filas_procesables
    except Exception:
        return []

def verificar_filas_procesables(driver, filas_procesables, opcion, log_dict=None):
    if not filas_procesables:
        if log_dict:
            log_message(log_dict, "WARNING", f"No se encontraron filas procesables para la opción seleccionada ({opcion}).")
        driver.quit()
        exit()