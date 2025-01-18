from selenium.webdriver.common.by import By
from utils import safe_find_element
from logger import log_message

def verificar_registros_npt(driver, log_dict=None):
    try:
        filas_xpath = '//*[@id="mainForm:tblSurtimientos_data"]/tr'
        filas = driver.find_elements(By.XPATH, filas_xpath)
        if not filas:
            log_message(log_dict, "WARNING", "No se encontraron filas en la tabla para NPT.")
            return False
        for fila in filas:
            if "NPT" in fila.text:
                log_message(log_dict, "SUCCESS", "Se encontraron registros para NPT.")
                return True
        log_message(log_dict, "INFO", "No se encontraron registros específicos para NPT.")
        return False
    except Exception as e:
        log_message(log_dict, "ERROR", f"Error al verificar registros para NPT: {str(e)}")
        return False