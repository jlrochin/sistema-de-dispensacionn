import xlwings as xw
from logger import log_message

def conectar_excel(log_dict=None):
    global workbook
    try:
        if log_dict:
            log_message(log_dict, "INFO", "Intentando conectar al archivo Excel...")
        app = xw.App(visible=False, add_book=False)
        app.window_state = 'minimized'
        workbook = None
        for book in xw.books:
            if "ordenes surtidas" in book.name.lower().strip():
                workbook = book
                break
        if workbook is None:
            raise FileNotFoundError("No se encontró un archivo abierto que contenga 'ordenes surtidas' en el nombre.")
        sheet = workbook.sheets["Dispensación"]
        if log_dict:
            log_message(log_dict, "SUCCESS", f"Conectado al archivo Excel correctamente: {workbook.name}")
        return workbook, sheet
    except FileNotFoundError as fnfe:
        if log_dict:
            log_message(log_dict, "WARNING", str(fnfe))
        return None, None
    except Exception:
        if log_dict:
            log_message(log_dict, "ERROR", "No se pudo conectar al archivo Excel. Asegúrate de que esté abierto.")
        return None, None

def guardar_registro(sheet, registro, workbook, log_dict=None):
    try:
        siguiente_fila = encontrar_ultima_fila(sheet)
        sheet.range(f"A{siguiente_fila}").value = registro
        workbook.save()
        if log_dict:
            log_message(log_dict, "SUCCESS", f"Datos guardados en la fila {siguiente_fila}.")
    except Exception:
        if log_dict:
            log_message(log_dict, "ERROR", "Error al guardar el registro en Excel.")

def encontrar_ultima_fila(sheet):
    fila_actual = 1
    while True:
        celda_valor = sheet.range(f"A{fila_actual}").value
        if celda_valor in [None, ""]:
            return fila_actual
        fila_actual += 1