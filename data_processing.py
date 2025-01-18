from utils import safe_find_element
from logger import log_message
from sanitization import marcar_sanitizados, dispensar_y_confirmar
from excel import guardar_registro
from colorama import Fore, init
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

init(autoreset=True)

def manejar_claves(driver, wait, log_dict=None):
    try:
        claves = driver.find_elements(By.XPATH, '//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr/td[2]/span[2]')
        claves_texto = [clave.text for clave in claves]

        for index, clave in enumerate(claves_texto, start=1):
            cantidad_xpath = f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{index}]/td[5]'
            cantidad_solicitada = driver.find_element(By.XPATH, cantidad_xpath).text
            cantidad_solicitada = int(cantidad_solicitada) if cantidad_solicitada.isdigit() else 0

            if log_dict:
                log_message(log_dict, "INFO", f"Procesando clave {clave} con cantidad solicitada {cantidad_solicitada}.")

            campo_buscar = safe_find_element(driver, '//*[@id="formSurtimientoDetail:codigSurt_input"]', modo="clickable", log_dict=log_dict)
            if campo_buscar:
                campo_buscar.clear()
                campo_buscar.send_keys(clave)
                time.sleep(1)

                if cantidad_solicitada > 1:
                    campo_cantidad = safe_find_element(driver, '//*[@id="formSurtimientoDetail:xcantidad"]', modo="clickable", log_dict=log_dict)
                    if campo_cantidad:
                        campo_cantidad.clear()
                        valor_dinamico = str(cantidad_solicitada)
                        driver.execute_script("arguments[0].value = arguments[1];", campo_cantidad, valor_dinamico)
                        driver.execute_script("PrimeFaces.ab({s:'formSurtimientoDetail:xcantidad',e:'keyup',f:'formSurtimientoDetail',p:'formSurtimientoDetail:xcantidad',u:'formSurtimientoDetail:xcantidad'});")
                        time.sleep(1)

                campo_buscar.send_keys(u'\ue007')
                time.sleep(1)

                if log_dict:
                    log_message(log_dict, "SUCCESS", f"Clave {clave} procesada correctamente con cantidad {cantidad_solicitada}.")
    except Exception:
        if log_dict:
            log_message(log_dict, "ERROR", "Error al procesar las claves asociadas a la fila.")

def procesar_datos_fila(driver, log_dict=None):
    try:
        folio = safe_find_element(driver, '//*[@id="formSurtimientoDetail:j_idt92"]', "Sin Folio", log_dict=log_dict)
        paciente = safe_find_element(driver, '//*[@id="formSurtimientoDetail:j_idt113"]', "Sin Paciente", log_dict=log_dict)

        try:
            fila_medicamento = driver.find_element(By.XPATH, '//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[1]')
            medicamento_xpath_options = ['./td[3]/u', './td[3]']
            medicamento = None
            for xpath in medicamento_xpath_options:
                try:
                    elemento_medicamento = fila_medicamento.find_element(By.XPATH, xpath)
                    if elemento_medicamento.text.strip():
                        medicamento = elemento_medicamento.text.strip()
                        break
                except Exception:
                    continue
            if not medicamento:
                medicamento = "Sin Medicamento"
                print("Error: No se pudo capturar el medicamento correctamente.")
            else:
                print(f"Medicamento capturado: {medicamento}")
        except Exception as e:
            medicamento = "Error en captura"
            print(f"Error general al capturar el medicamento: {str(e)}")

        dosis = safe_find_element(driver, '//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[1]/td[4]/span[2]', "0", log_dict=log_dict)
        frascos = safe_find_element(driver, '//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[1]/td[5]', "0", log_dict=log_dict)
        lote = safe_find_element(driver, '//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[1]/td[6]/span[2]', "Sin Lote", log_dict=log_dict)

        solucion = safe_find_element(driver, '//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[2]/td[3]', "Sin Solución", log_dict=log_dict)
        if solucion != "Sin Solución":
            volumen = safe_find_element(driver, '//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[2]/td[4]/span[2]', "0", log_dict=log_dict)
            cantidad = safe_find_element(driver, '//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[2]/td[5]', "0", log_dict=log_dict)
            lote_solucion = safe_find_element(driver, '//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[2]/td[6]/span[2]', "Sin Lote Solución", log_dict=log_dict)
        else:
            volumen, cantidad, lote_solucion = "0", "1", "Sin Lote Solución"

        datos_fila = {
            "folio": folio,
            "paciente": paciente,
            "medicamento": medicamento,
            "dosis": dosis,
            "frascos": frascos,
            "lote": lote,
            "solucion": solucion,
            "volumen": volumen,
            "cantidad": cantidad,
            "lote_solucion": lote_solucion,
        }

        if log_dict:
            log_message(log_dict, "SUCCESS", f"Datos procesados correctamente: {datos_fila}")

        return datos_fila
    except Exception:
        if log_dict:
            log_message(log_dict, "ERROR", "Error al procesar datos de la fila.")
        return None

def procesar_fila(driver, fila_tipo, sheet, workbook, wait, log_dict=None):
    try:
        fila_numero, tipo = fila_tipo
        tipo_xpath = f'//*[@id="mainForm:tblSurtimientos_data"]/tr[{fila_numero}]/td[2]'
        tipo_actual = safe_find_element(driver, tipo_xpath, "Desconocido")

        print(f"{Fore.GREEN}Procesando fila {fila_numero} de tipo '{tipo_actual}'.")

        celda_xpath = f'//*[@id="mainForm:tblSurtimientos_data"]/tr[{fila_numero}]/td[2]'
        try:
            celda = wait.until(EC.presence_of_element_located((By.XPATH, celda_xpath)))
            acciones = ActionChains(driver)
            acciones.double_click(celda).perform()
            time.sleep(2)
            print(f"{Fore.GREEN}Detalle de la fila {fila_numero} abierto exitosamente.")
        except Exception as e:
            print(f"{Fore.RED}Error al abrir el detalle de la fila {fila_numero}: {e}")
            return
        
        if tipo_actual == "NPT":
            log_message(log_dict, "INFO", f"Procesando fila de tipo NPT: {fila_tipo}")
            procesar_datos_y_guardar_npt(driver, workbook, log_dict=log_dict)
        else:
            log_message(log_dict, "INFO", f"Procesando fila de tipo {tipo_actual}: {fila_tipo}")
            procesar_datos_y_guardar(driver, sheet, workbook)

        manejar_claves(driver, wait)
        marcar_sanitizados(driver, wait)
        dispensar_y_confirmar(driver, wait)

    except Exception as e:
        print(f"{Fore.RED}Error al procesar la fila {fila_tipo}: {e}")

def procesar_datos_y_guardar(driver, sheet, workbook, log_dict=None):
    try:
        folio = safe_find_element(driver, '//*[@id="formSurtimientoDetail:j_idt92"]', "Sin Folio", log_dict=log_dict)
        paciente = safe_find_element(driver, '//*[@id="formSurtimientoDetail:j_idt113"]', "Sin Paciente", log_dict=log_dict)

        filas_xpath = '//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr'
        filas = driver.find_elements(By.XPATH, filas_xpath)

        medicamento = solucion = "Sin Solución"
        dosis = frascos = lote_medicamento = "0"
        volumen = "0"
        cantidad = "1"
        lote_solucion = "Sin Lote Solución"

        palabras_clave_solucion = ["Cloruro", "Glucosa"]

        for i, fila in enumerate(filas, start=1):
            nombre_producto = safe_find_element(driver, f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{i}]/td[3]', "Sin Nombre", log_dict=log_dict)

            if any(palabra in nombre_producto for palabra in palabras_clave_solucion):
                solucion = nombre_producto
                volumen = safe_find_element(driver, f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{i}]/td[4]/span[2]', "0", log_dict=log_dict)
                cantidad = safe_find_element(driver, f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{i}]/td[5]', "0", log_dict=log_dict)
                lote_solucion = safe_find_element(driver, f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{i}]/td[6]/span[2]', "Sin Lote", log_dict=log_dict)
            else:
                medicamento = nombre_producto
                dosis = safe_find_element(driver, f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{i}]/td[4]/span[2]', "0", log_dict=log_dict)
                frascos = safe_find_element(driver, f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{i}]/td[5]', "0", log_dict=log_dict)
                lote_medicamento = safe_find_element(driver, f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{i}]/td[6]/span[2]', "Sin Lote", log_dict=log_dict)

        registro = [
            folio, paciente, medicamento, dosis, frascos, "", lote_medicamento,
            "",
            solucion, volumen, cantidad, lote_solucion
        ]

        guardar_registro(sheet, registro, workbook, log_dict)
        if log_dict:
            log_message(log_dict, "SUCCESS", f"Datos guardados correctamente en una fila: {registro}")

    except Exception as e:
        if log_dict:
            log_message(log_dict, "ERROR", f"Error al procesar y guardar los datos: {e}")

def procesar_datos_y_guardar_npt(driver, workbook, log_dict=None):
    try:
        nombre_hoja = "NPT"
        hoja_npt = None
        if nombre_hoja not in [sheet.name for sheet in workbook.sheets]:
            hoja_npt = workbook.sheets.add(name=nombre_hoja)
        else:
            hoja_npt = workbook.sheets[nombre_hoja]

        folio = safe_find_element(driver, '//*[@id="formSurtimientoDetail:j_idt92"]', "Sin Folio", log_dict=log_dict)
        paciente = safe_find_element(driver, '//*[@id="formSurtimientoDetail:j_idt113"]', "Sin Paciente", log_dict=log_dict)

        filas_xpath = '//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr'
        filas = driver.find_elements(By.XPATH, filas_xpath)

        ultima_fila_con_datos = hoja_npt.range("C1").end("down").row if hoja_npt.range("C1").value else 0
        fila_actual = ultima_fila_con_datos + 1

        while hoja_npt.range(f"C{fila_actual}").value is not None or \
            hoja_npt.range(f"C{fila_actual + 1}").value is not None or \
            hoja_npt.range(f"C{fila_actual + 2}").value is not None:
            fila_actual += 1

        ultima_fila = fila_actual + 2

        for i, fila in enumerate(filas, start=1):
            medicamento = safe_find_element(driver, f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{i}]/td[3]', "Sin Medicamento", log_dict=log_dict)
            dosis = safe_find_element(driver, f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{i}]/td[4]/span[2]', "0", log_dict=log_dict)
            cantidad = safe_find_element(driver, f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{i}]/td[5]', "0", log_dict=log_dict)
            lote = safe_find_element(driver, f'//*[@id="formSurtimientoDetail:tblInsumos_data"]/tr[{i}]/td[6]/span[2]', "Sin Lote", log_dict=log_dict)

            if i == 1:
                registro = [folio, paciente, medicamento, dosis, cantidad, lote]
            else:
                registro = ["", "", medicamento, dosis, cantidad, lote]

            hoja_npt.range(f"A{ultima_fila}").value = registro
            ultima_fila += 1

        log_message(log_dict, "SUCCESS", f"Datos de NPT guardados correctamente en la hoja 'NPT'.")
        print(f"{Fore.GREEN}Datos guardados exitosamente en la hoja 'NPT'.")

    except Exception as e:
        log_message(log_dict, "ERROR", f"Error al procesar y guardar datos dinámicos en la hoja 'NPT': {str(e)}")
        print(f"{Fore.RED}Error general al procesar y guardar datos en 'NPT': {e}")