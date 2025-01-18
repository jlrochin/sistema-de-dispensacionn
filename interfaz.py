import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import sys
from main import flujo_principal

opcion_map = {
    "Solo ONC": {"num": "1", "url": "http://172.18.28.101/emotion/index.xhtml"},
    "Solo ANT": {"num": "2", "url": "http://172.18.28.101/emotion/index.xhtml"},
    "Ambos (ONC y ANT)": {"num": "3", "url": "http://172.18.28.101/emotion/index.xhtml"},
    "NPT": {"num": "4", "url": "https://172.18.28.101/emotion/index.xhtml"}
}

flujo_en_ejecucion = False
driver = None
workbook = None

class RedirectOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        if "[ERROR]" in string:
            tag = "red"
        elif "[SUCCESS]" in string:
            tag = "green"
        elif "[WARNING]" in string:
            tag = "orange"
        elif "[INFO]" in string:
            tag = "blue"
        else:
            tag = "black"

        self.text_widget.config(state="normal")
        self.text_widget.insert(tk.END, string, tag)
        self.text_widget.see(tk.END)
        self.text_widget.config(state="disabled")

    def flush(self):
        pass

def cerrar_navegador():
    global driver
    try:
        if driver:
            driver.quit()
            print("\033[34m[INFO] Navegador cerrado correctamente.\033[0m\n")
        else:
            print("\033[33m[WARNING] No se encontró un navegador activo para cerrar.\033[0m\n")
    except Exception as e:
        print(f"\033[31m[ERROR] Error al cerrar el navegador: {e}\033[0m\n")

def reiniciar_interfaz():
    for widget in frame.winfo_children():
        widget.destroy()

    ventana.geometry("500x300")
    configurar_formulario_inicio()

def configurar_formulario_inicio():
    global entry_usuario, entry_contraseña, combo_opcion, btn_finalizar

    COLOR_FONDO = "#FFFFFF"
    COLOR_TEXTO = "#003366"
    COLOR_RESALTADO = "#1E90FF"
    COLOR_BOTON = "#1ce42e"
    COLOR_BOTON_ACTIVO = "#74ff33"
    COLOR_BOTON_TEXTO = "#FFFFFF"
    COLOR_ENTRADA = "#F0F8FF"
    COLOR_FOOTER = "#00264D"

    ruta_imagen = r"C:\Users\EQUIPO 7\Desktop\jlru\fondo.jpg"
    imagen = Image.open(ruta_imagen)
    imagen_fondo = ImageTk.PhotoImage(imagen)
    
    label_fondo = tk.Label(frame, image=imagen_fondo)
    label_fondo.image = imagen_fondo
    label_fondo.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    label_titulo = tk.Label(frame, text="Inicio de Sesión", font=("Arial", 14, "bold"), bg=COLOR_TEXTO, fg=COLOR_BOTON_TEXTO)
    label_titulo.place(x=185, y=20)

    btn_version = tk.Button(
        frame, text="Acerca de", command=mostrar_version,
        bg=COLOR_TEXTO, fg=COLOR_BOTON_TEXTO, relief="flat", font=("Arial", 10, "bold")
    )
    btn_version.place(x=420, y=10)

    label_usuario = tk.Label(frame, text="Usuario:", font=("Arial", 10), bg=COLOR_TEXTO, fg=COLOR_BOTON_TEXTO)
    label_usuario.place(x=100, y=60)
    entry_usuario = tk.Entry(frame, width=30, relief="flat", highlightbackground=COLOR_RESALTADO, highlightthickness=1)
    entry_usuario.place(x=200, y=60)

    label_contraseña = tk.Label(frame, text="Contraseña:", font=("Arial", 10), bg=COLOR_TEXTO, fg=COLOR_BOTON_TEXTO)
    label_contraseña.place(x=100, y=100)
    entry_contraseña = tk.Entry(frame, show="*", width=30, relief="flat", highlightbackground=COLOR_RESALTADO, highlightthickness=1)
    entry_contraseña.place(x=200, y=100)

    label_opcion = tk.Label(frame, text="Tipo de mezcla:", font=("Arial", 10), bg=COLOR_TEXTO, fg=COLOR_BOTON_TEXTO)
    label_opcion.place(x=100, y=140)
    combo_opcion = ttk.Combobox(frame, values=["Solo ONC", "Solo ANT", "Ambos (ONC y ANT)", "NPT"], state="readonly", width=27)
    combo_opcion.place(x=200, y=140)
    combo_opcion.current(0)

    btn_iniciar = tk.Button(
        frame, text="Iniciar Sesión", command=iniciar_sesion,
        bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, activebackground=COLOR_BOTON_ACTIVO, activeforeground=COLOR_BOTON_TEXTO,
        relief="flat", font=("Arial", 12, "bold")
    )
    btn_iniciar.place(x=190, y=180)
    
    label_footer = tk.Label(frame, text="Desarrollado por JLRU", font=("Arial", 10), fg=COLOR_BOTON_TEXTO, bg=COLOR_FOOTER)
    label_footer.pack(side=tk.BOTTOM, pady=5)

    btn_finalizar = tk.Button(
        frame, text="Finalizar", command=finalizar_programa,
        bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, activebackground=COLOR_BOTON_ACTIVO, activeforeground=COLOR_BOTON_TEXTO,
        relief="flat", font=("Arial", 12, "bold")
    )
    btn_finalizar.place(x=230, y=300)
    btn_finalizar.place_forget()

def mostrar_boton_finalizar():
    print("Mostrando el botón Finalizar...")
    btn_finalizar.place(x=230, y=300)

def finalizar_programa():
    global driver, workbook
    try:
        sys.stdout = sys.__stdout__
        
        if driver:
            driver.quit()
            print("[INFO] Navegador cerrado correctamente.")
        else:
            print("[WARNING] No se encontró un navegador activo.")

        if workbook:
            workbook.save()
            print("[SUCCESS] Archivo Excel guardado correctamente.")
        else:
            print("[WARNING] No se encontró archivo Excel.")
    except Exception as e:
        print(f"[ERROR] Ocurrió un error al finalizar el programa: {e}")
    finally:
        ventana.quit()
    
def redirigir_a_login():
    global driver
    try:
        driver.get("http://172.18.28.101/emotion/index.xhtml")
        print("\033[34m[INFO] Navegador redirigido al formulario de inicio de sesión.\033[0m\n")
    except Exception as e:
        print(f"\033[31m[ERROR] No se pudo redirigir al formulario de inicio de sesión: {e}\033[0m\n")
 
def mostrar_boton_finalizar():
    btn_finalizar.place(x=230, y=300)

def mostrar_version():
    pass

def mostrar_version():
    version = "Versión del Sistema: v2.1"
    messagebox.showinfo("Acerca del Sistema", version)

def centrar_popup(popup, parent):
    popup.update_idletasks()
    popup_width = popup.winfo_width()
    popup_height = popup.winfo_height()

    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()
    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()

    position_x = parent_x + (parent_width - popup_width) // 2
    position_y = parent_y + (parent_height - popup_height) // 2

    popup.geometry(f"{popup_width}x{popup_height}+{position_x}+{position_y}")

def abrir_popup():
    popup = tk.Toplevel(ventana)
    popup.title("Pop-up centrado")
    popup.geometry("300x200")
    popup.resizable(False, False)

    centrar_popup(popup, ventana)

    label = tk.Label(popup, text="Esto es un pop-up centrado.", font=("Arial", 12))
    label.pack(pady=50)

def iniciar_sesion():
    global flujo_en_ejecucion
    flujo_en_ejecucion = True

    usuario = entry_usuario.get().strip()
    contraseña = entry_contraseña.get().strip()
    opcion = combo_opcion.get()

    if not usuario or not contraseña or not opcion:
        messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
        flujo_en_ejecucion = False
        return

    opcion_info = opcion_map.get(opcion)
    if not opcion_info:
        messagebox.showerror("Error", "Opción inválida seleccionada.")
        flujo_en_ejecucion = False
        return

    opcion_num = opcion_info["num"]
    base_url = opcion_info["url"]

    ventana.geometry("600x450")

    global text_area
    text_area = tk.Text(frame, wrap=tk.WORD, state="normal", font=("Arial", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    text_area.tag_configure("red", foreground="red")
    text_area.tag_configure("green", foreground="green")
    text_area.tag_configure("orange", foreground="orange")
    text_area.tag_configure("blue", foreground="blue")
    text_area.tag_configure("black", foreground="black")

    sys.stdout = RedirectOutput(text_area)

    def ejecutar_flujo():
        global flujo_en_ejecucion
        try:
            print("[INFO] Iniciando el flujo principal...")
            flujo_principal(usuario, contraseña, opcion_num, base_url)
            print("[SUCCESS] Flujo principal completado.")
        except Exception as e:
            print(f"[ERROR] Ha ocurrido un error: {e}")
        finally:
            flujo_en_ejecucion = False
            sys.stdout = sys.__stdout__

    hilo = threading.Thread(target=ejecutar_flujo)
    hilo.daemon = True
    hilo.start()

    mostrar_boton_finalizar()

def intentar_cerrar_ventana():
    if flujo_en_ejecucion:
        messagebox.showwarning("Advertencia", "El flujo principal aún no ha terminado. Por favor, espera.")
    else:
        ventana.destroy()

ventana = tk.Tk()

window_width = 500
window_height = 300

screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()

position_x = int((screen_width - window_width) / 2)
position_y = int((screen_height - window_height) / 2)

ventana.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

ventana.title("Sistema de Dispensación")
ventana.resizable(False, False)
ventana.protocol("WM_DELETE_WINDOW", intentar_cerrar_ventana)

frame = tk.Frame(ventana, bg="white")
frame.pack(fill="both", expand=True)

configurar_formulario_inicio()

ventana.mainloop()
