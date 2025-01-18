from excel import conectar_excel
from browser import inicializar_navegador, iniciar_sesion, navegar_a_submenu
from utils import obtener_credenciales_y_opcion, verificar_tabla_registros, obtener_filas_procesables
from finalization import finalizar_programa
from npt_verification import verificar_registros_npt
from data_processing import procesar_fila
from logger import log_message, finalizar_log_definitivo
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def flujo_principal(usuario=None, contraseña=None, opcion=None, base_url=None):
    if not base_url or not base_url.strip():
        raise ValueError("La URL base no está definida o es inválida. Revisa el flujo de interfaz.py.")
    
    log_dict = {}

    log_message(log_dict, "INFO", f"Iniciando flujo con la URL: {base_url}")
    print(f"[DEBUG] Usuario: {usuario}, Opción: {opcion}, URL: {base_url}")
    
    log_history = {}

    try:
        log_message(log_history, "INFO", "Intentando conectar al archivo Excel...")
        workbook, sheet = conectar_excel(log_dict=log_history)
        if not workbook or not sheet:
            log_message(log_history, "ERROR", "No se pudo conectar al archivo Excel. Finalizando flujo...")
            return

        driver, wait = inicializar_navegador(log_dict=log_history)
        
        if not driver or not wait:
            log_message(log_history, "ERROR", "No se pudo inicializar el navegador. Finalizando flujo...")
            return
        
        log_message(log_history, "INFO", "Intentando iniciar sesión...")
        while True:
            if iniciar_sesion(driver, wait, usuario, contraseña, log_dict=log_history, base_url=base_url):
                log_message(log_history, "SUCCESS", "Inicio de sesión realizado con éxito.")
                break
            else:
                log_message(log_history, "WARNING", "Inicio de sesión fallido. Solicita nuevamente las credenciales...")
                usuario, contraseña, _ = obtener_credenciales_y_opcion(log_dict=log_history)
                if not usuario or not contraseña:
                    log_message(log_history, "ERROR", "El usuario decidió no continuar. Finalizando flujo...")
                    driver.quit()
                    return
                log_message(log_history, "INFO", "Redirigiendo al formulario de inicio de sesión...")
                driver.get(base_url)
        
        log_message(log_history, "INFO", "Inicio de sesión exitoso. Continuando con el flujo principal...")

        if not navegar_a_submenu(driver, wait, log_dict=log_history):
            log_message(log_history, "ERROR", "No se pudo navegar al submenú correctamente.")
            driver.quit()
            return
        log_message(log_history, "SUCCESS", "Navegación al submenú realizada con éxito.")

        log_message(log_history, "INFO", "Aplicando filtro en la tabla...")
        try:
            filtro_xpath = '//*[@id="mainForm:tblSurtimientos:j_idt57"]/span[1]'
            filtro_element = wait.until(EC.element_to_be_clickable((By.XPATH, filtro_xpath)))
            filtro_element.click()
            log_message(log_history, "SUCCESS", "Filtro aplicado con éxito.")
        except Exception:
            log_message(log_history, "ERROR", "No se pudo aplicar el filtro. Finalizando flujo...")
            driver.quit()
            time.sleep(1)
            return
        
        try:
            filtro_input_xpath = '//*[@id="mainForm:tblSurtimientos:j_idt54:filter"]'
            filtro_input_element = wait.until(EC.element_to_be_clickable((By.XPATH, filtro_input_xpath)))
            if opcion == "1":
                filtro_input_element.send_keys("ONC")
            elif opcion == "2":
                filtro_input_element.send_keys("ANT")
            elif opcion == "4":
                filtro_input_element.send_keys("NPT")
                time.sleep(1)
            log_message(log_history, "SUCCESS", "Opción seleccionada escrita en el recuadro del filtro.")
            time.sleep(1)
        except Exception as e:
            log_message(log_history, "ERROR", f"No se pudo escribir en el recuadro del filtro: {e}")

        log_message(log_history, "INFO", "Verificando registros en la tabla...")
        if not verificar_tabla_registros(driver, log_dict=log_history):
            driver.quit()
            return
                
        if opcion == "4":
            log_message(log_history, "INFO", "Verificando registros específicos para NPT...")
            if not verificar_registros_npt(driver, log_dict=log_history):
                log_message(log_history, "ERROR", "No se encontraron registros específicos para NPT. Finalizando flujo...")
                driver.quit()
                return
            else:
                log_message(log_history, "SUCCESS", "Se encontraron registros específicos para NPT. Continuando con el flujo...")

        log_message(log_history, "INFO", "Iniciando procesamiento dinámico de filas...")
        total_procesadas = 0

        while True:
            try:
                log_message(log_history, "INFO", "Obteniendo filas procesables según la opción seleccionada...")
                filas_procesables = obtener_filas_procesables(driver, opcion, log_dict=log_history)
                if not filas_procesables:
                    log_message(log_history, "INFO", "No se encontraron más filas procesables. Finalizando...")
                    break
                else:
                    log_message(log_history, "DEBUG", f"Filas procesables obtenidas: {filas_procesables}")

                fila_tipo = filas_procesables[0]
                log_message(log_history, "INFO", f"Procesando fila: {fila_tipo}")

                procesar_fila(driver, fila_tipo, sheet, workbook, wait)
                total_procesadas += 1

                log_message(log_history, "INFO", "Volviendo a evaluar filas procesables tras procesar la fila...")
            except Exception as e:
                log_message(log_history, "ERROR", f"Error al procesar la fila {fila_tipo}: {str(e)}")
                continue

        log_message(log_history, "SUCCESS", f"Procesamiento finalizado. Total de filas procesadas exitosamente: {total_procesadas}")

        workbook.save()
        log_message(log_history, "SUCCESS", f"Archivo Excel guardado correctamente con {total_procesadas} filas procesadas.")
    
    except Exception as e:
        log_message(log_history, "ERROR", f"Ocurrió un problema general en el flujo principal: {e}")
    
    finally:
        if 'driver' in locals() and driver:
            driver.quit()
        log_message(log_history, "INFO", "Flujo principal finalizado.")
        finalizar_log_definitivo(usuario, log_history)