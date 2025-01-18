from logger import log_message, guardar_log_incremental, finalizar_log_definitivo

def finalizar_programa(driver, workbook, log_dict=None, usuario="usuario_demo"):
    try:
        workbook.save()
        if log_dict:
            log_message(log_dict, "SUCCESS", "Archivo Excel guardado correctamente.")
    except Exception:
        if log_dict:
            log_message(log_dict, "ERROR", "Error al guardar el archivo Excel.")
    finally:
        if log_dict:
            guardar_log_incremental(usuario, log_dict)
        if log_dict:
            log_message(log_dict, "INFO", "Cerrando el programa...")
        driver.quit()
        try:
            finalizar_log_definitivo(usuario, log_dict)
        except Exception as e:
            if log_dict:
                log_message(log_dict, "ERROR", f"Error al finalizar el log: {e}")
        input("Presiona cualquier tecla para cerrar el programa...")