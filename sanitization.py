from utils import safe_find_element
from logger import log_message
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def marcar_sanitizados(driver, wait, log_dict=None):
    try:
        casilla_xpath = '//*[@id="formSurtimientoDetail:chkSanitConfirm"]/div[2]'
        casilla_element = wait.until(EC.presence_of_element_located((By.XPATH, casilla_xpath)))

        # Verificar si la casilla ya está marcada
        if "ui-state-active" not in casilla_element.get_attribute("class"):
            casilla_element.click()
            time.sleep(1)
            if "ui-state-active" in casilla_element.get_attribute("class"):
                if log_dict:
                    log_message(log_dict, "SUCCESS", "Casilla 'Insumos Sanitizados' marcada con éxito.")
                return True
            else:
                if log_dict:
                    log_message(log_dict, "ERROR", "La casilla no se activó después de intentar marcarla.")
                return False
        else:
            if log_dict:
                log_message(log_dict, "INFO", "La casilla 'Insumos Sanitizados' ya estaba marcada.")
            return True
    except Exception:
        if log_dict:
            log_message(log_dict, "ERROR", "Error al marcar la casilla 'Insumos Sanitizados'.")
        return False

def dispensar_y_confirmar(driver, wait, log_dict=None):
    try:
        # Presionar botón "Dispensar"
        if log_dict:
            log_message(log_dict, "INFO", "Presionando botón 'Dispensar'...")
        boton_dispensar_xpath = '//*[@id="formSurtimientoDetail:cmbDispensar"]/span[2]'
        boton_dispensar = wait.until(EC.element_to_be_clickable((By.XPATH, boton_dispensar_xpath)))
        boton_dispensar.click()
        time.sleep(0.5)

        # Confirmar dispensación
        if log_dict:
            log_message(log_dict, "INFO", "Confirmando dispensación...")
        boton_si_xpath = '//*[@id="formSurtimientoDetail:j_idt203"]/span[2]'
        boton_si = wait.until(EC.element_to_be_clickable((By.XPATH, boton_si_xpath)))
        boton_si.click()
        if log_dict:
            log_message(log_dict, "SUCCESS", "Dispensación confirmada.")
        time.sleep(0.5)

        # Regresar a la tabla principal
        if log_dict:
            log_message(log_dict, "INFO", "Regresando a la tabla principal...")
        boton_regresar_xpath = '//*[@id="j_idt207"]/div[1]/a/span'
        boton_regresar = wait.until(EC.element_to_be_clickable((By.XPATH, boton_regresar_xpath)))
        boton_regresar.click()
        if log_dict:
            log_message(log_dict, "SUCCESS", "Regreso a la tabla realizado con éxito.")
        time.sleep(0.5)

        return True
    except Exception:
        if log_dict:
            log_message(log_dict, "ERROR", "Error durante la dispensación o al regresar a la tabla.")
        return False