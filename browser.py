from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from logger import log_message

def inicializar_navegador(log_dict=None):
    try:
        if log_dict:
            log_message(log_dict, "INFO", "Configurando opciones de Chrome...")
        chrome_options = Options()
        chrome_options.add_argument("--start-minimized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-insecure-localhost')
        service_path = "C:/Users/EQUIPO 7/Desktop/jlru/chromedriver.exe"
        if log_dict:
            log_message(log_dict, "DEBUG", f"Ruta de ChromeDriver: {service_path}")
        service = Service(service_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 20)
        if log_dict:
            log_message(log_dict, "SUCCESS", "Navegador inicializado correctamente.")
        return driver, wait
    except Exception as e:
        log_message(log_dict, "ERROR", f"Error al inicializar el navegador: {str(e)}")
        return None, None

def iniciar_sesion(driver, wait, usuario, password, log_dict=None, base_url=None):
    try:
        if not base_url or not base_url.strip():
            log_message(log_dict, "ERROR", "base_url no se proporcionó o es inválida.")
            raise ValueError("La URL base no se ha proporcionado o es inválida.")
        log_message(log_dict, "INFO", f"Navegando a la URL base: {base_url}")
        driver.get(base_url)
        log_message(log_dict, "INFO", "Introduciendo credenciales...")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_username"]'))).send_keys(usuario)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_password"]'))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-login"]/form/div/div[2]/div[1]/div[4]/input'))).click()
        try:
            mensaje_error = driver.find_element(By.XPATH, '//*[contains(text(), "Contraseña incorrecta") or contains(text(), "Cuenta de usuario no encontrado")]')
            if mensaje_error.is_displayed():
                log_message(log_dict, "ERROR", f"Error en inicio de sesión: {mensaje_error.text}")
                return False
        except NoSuchElementException:
            log_message(log_dict, "SUCCESS", "Inicio de sesión realizado con éxito.")
            return True
    except Exception as e:
        log_message(log_dict, "ERROR", f"Error durante el inicio de sesión: {str(e)}")
        return False

def navegar_a_submenu(driver, wait, log_dict=None):
    try:
        if log_dict:
            log_message(log_dict, "INFO", "Intentando navegar al submenú...")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_idt11"]/ul/li[4]/a'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_idt11"]/ul/li[4]/ul/li[5]'))).click()
        if log_dict:
            log_message(log_dict, "SUCCESS", "Navegación al submenú realizada con éxito.")
        return True
    except Exception:
        if log_dict:
            log_message(log_dict, "ERROR", "Error al navegar al submenú.")
        return False

def verificar_navegador_activo(driver):
    try:
        driver.current_url
        return True
    except Exception:
        return False