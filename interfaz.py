import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import sys
import re
from main import flujo_principal
from browser import inicializar_navegador
from excel import conectar_excel

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
        # Identificar el nivel del mensaje y asignar un color
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

        # Escribe el texto en el widget de texto con el color correspondiente
        self.text_widget.config(state="normal")
        self.text_widget.insert(tk.END, string, tag)
        self.text_widget.see(tk.END)  # Desplaza al final
        self.text_widget.config(state="disabled")

    def flush(self):
        pass

def cerrar_navegador():
    """
    Cierra el navegador de Selenium si está activo.
    """
    global driver
    try:
        # Verifica si el objeto `driver` está inicializado
        if driver:
            driver.quit()
            print("\033[34m[INFO] Navegador cerrado correctamente.\033[0m\n")
        else:
            print("\033[33m[WARNING] No se encontró un navegador activo para cerrar.\033[0m\n")
    except Exception as e:
        print(f"\033[31m[ERROR] Error al cerrar el navegador: {e}\033[0m\n")

def reiniciar_interfaz():
    """
    Reinicia la interfaz gráfica al estado inicial, manteniendo la misma ventana.
    """
    for widget in frame.winfo_children():
        widget.destroy()  # Elimina todos los widgets del marco

    # Restaurar la geometría original
    ventana.geometry("500x300")

    # Restaurar el formulario de inicio
    configurar_formulario_inicio()

def configurar_formulario_inicio():
    """
    Configura el formulario inicial en la ventana con una imagen de fondo y estilo mejorado.
    """
    global entry_usuario, entry_contraseña, combo_opcion, btn_finalizar  # Declarar los widgets como globales

    # Colores
    COLOR_FONDO = "#FFFFFF"  # Fondo general
    COLOR_TEXTO = "#003366"  # Azul oscuro para texto
    COLOR_RESALTADO = "#1E90FF"  # Azul vibrante para bordes
    COLOR_BOTON = "#1ce42e"  # Verde oscuro para botones
    COLOR_BOTON_ACTIVO = "#74ff33"  # Verde más oscuro para botones activos
    COLOR_BOTON_TEXTO = "#FFFFFF"  # Texto de botones
    COLOR_ENTRADA = "#F0F8FF"  # Fondo de los campos de entrada
    COLOR_FOOTER = "#00264D"  # Fondo del footer

    # Cargar la imagen de fondo
    ruta_imagen = r"C:\Users\EQUIPO 7\Desktop\jlru\fondo.jpg"  # Ruta a tu imagen
    imagen = Image.open(ruta_imagen)  # Ajustar al tamaño de la ventana/frame
    imagen_fondo = ImageTk.PhotoImage(imagen)
    
    # Mostrar la imagen sin redimensionar
    label_fondo = tk.Label(frame, image=imagen_fondo)
    label_fondo.image = imagen_fondo  # Mantener referencia
    label_fondo.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Título centrado
    label_titulo = tk.Label(frame, text="Inicio de Sesión", font=("Arial", 14, "bold"), bg=COLOR_TEXTO, fg=COLOR_BOTON_TEXTO)
    label_titulo.place(x=185, y=20)

    # Botón "Acerca de"
    btn_version = tk.Button(
        frame, text="Acerca de", command=mostrar_version,
        bg=COLOR_TEXTO, fg=COLOR_BOTON_TEXTO, relief="flat", font=("Arial", 10, "bold")
    )
    btn_version.place(x=420, y=10)  # Ajusta la posición según tu diseño

    # Usuario
    label_usuario = tk.Label(frame, text="Usuario:", font=("Arial", 10), bg=COLOR_TEXTO, fg=COLOR_BOTON_TEXTO)
    label_usuario.place(x=100, y=60)
    entry_usuario = tk.Entry(frame, width=30, relief="flat", highlightbackground=COLOR_RESALTADO, highlightthickness=1)
    entry_usuario.place(x=200, y=60)

    # Contraseña
    label_contraseña = tk.Label(frame, text="Contraseña:", font=("Arial", 10), bg=COLOR_TEXTO, fg=COLOR_BOTON_TEXTO)
    label_contraseña.place(x=100, y=100)
    entry_contraseña = tk.Entry(frame, show="*", width=30, relief="flat", highlightbackground=COLOR_RESALTADO, highlightthickness=1)
    entry_contraseña.place(x=200, y=100)

    # Tipo de mezcla
    label_opcion = tk.Label(frame, text="Tipo de mezcla:", font=("Arial", 10), bg=COLOR_TEXTO, fg=COLOR_BOTON_TEXTO)
    label_opcion.place(x=100, y=140)
    combo_opcion = ttk.Combobox(frame, values=["Solo ONC", "Solo ANT", "Ambos (ONC y ANT)", "NPT"], state="readonly", width=27)
    combo_opcion.place(x=200, y=140)
    combo_opcion.current(0)

    # Botón Iniciar Sesión
    btn_iniciar = tk.Button(
        frame, text="Iniciar Sesión", command=iniciar_sesion,
        bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, activebackground=COLOR_BOTON_ACTIVO, activeforeground=COLOR_BOTON_TEXTO,
        relief="flat", font=("Arial", 12, "bold")
    )
    btn_iniciar.place(x=190, y=180)
    
    # Footer "Desarrollado por JLRU"
    label_footer = tk.Label(frame, text="Desarrollado por JLRU", font=("Arial", 10), fg=COLOR_BOTON_TEXTO, bg=COLOR_FOOTER)
    label_footer.pack(side=tk.BOTTOM, pady=5)

    # Crear el botón "Finalizar" (invisible por ahora)
    btn_finalizar = tk.Button(
        frame, text="Finalizar", command=finalizar_programa,
        bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, activebackground=COLOR_BOTON_ACTIVO, activeforeground=COLOR_BOTON_TEXTO,
        relief="flat", font=("Arial", 12, "bold")
    )
    # Colocar el botón "Finalizar" justo encima del footer
    btn_finalizar.place(x=230, y=300)  # Ajustar la coordenada `y` para que esté justo encima del footer
    btn_finalizar.place_forget()  # Esconde el botón al inicio

def mostrar_boton_finalizar():
    print("Mostrando el botón Finalizar...")  # Depuración
    btn_finalizar.place(x=230, y=300)  # Mostrar el botón justo encima del footer

def finalizar_programa():
    """
    Cierra el navegador, guarda el archivo Excel y cierra la aplicación.
    """
    global driver, workbook
    try:
        # Restaurar sys.stdout antes de cerrar
        sys.stdout = sys.__stdout__
        
        # Cerrar el navegador
        if driver:
            driver.quit()
            print("[INFO] Navegador cerrado correctamente.")
        else:
            print("[WARNING] No se encontró un navegador activo.")

        # Guardar el archivo Excel
        if workbook:
            workbook.save()
            print("[SUCCESS] Archivo Excel guardado correctamente.")
        else:
            print("[WARNING] No se encontró archivo Excel.")
    except Exception as e:
        print(f"[ERROR] Ocurrió un error al finalizar el programa: {e}")
    finally:
        # Cerrar la aplicación
        ventana.quit()
    
def redirigir_a_login():
    """
    Redirige el navegador a la página de inicio de sesión.
    """
    global driver
    try:
        driver.get("http://172.18.28.101/emotion/index.xhtml")  # URL del formulario de login
        print("\033[34m[INFO] Navegador redirigido al formulario de inicio de sesión.\033[0m\n")
    except Exception as e:
        print(f"\033[31m[ERROR] No se pudo redirigir al formulario de inicio de sesión: {e}\033[0m\n")
 
def mostrar_boton_finalizar():
    # Muestra el botón "Finalizar" después del inicio de sesión
    btn_finalizar.place(x=230, y=300)

def mostrar_version():
    # Aquí iría el código para mostrar la versión
    pass

# Resto del código de interfaz.py...
def mostrar_version():
    """
    Muestra una ventana emergente con la versión del sistema.
    """
    version = "Versión del Sistema: v2.1"
    messagebox.showinfo("Acerca del Sistema", version)

def centrar_popup(popup, parent):
    # Obtener tamaño del pop-up
    popup.update_idletasks()  # Asegura que se obtienen las dimensiones correctas
    popup_width = popup.winfo_width()
    popup_height = popup.winfo_height()

    # Obtener tamaño y posición de la ventana principal
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()
    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()

    # Calcular posición para centrar el pop-up
    position_x = parent_x + (parent_width - popup_width) // 2
    position_y = parent_y + (parent_height - popup_height) // 2

    # Ajustar la geometría del pop-up
    popup.geometry(f"{popup_width}x{popup_height}+{position_x}+{position_y}")

def abrir_popup():
    popup = tk.Toplevel(ventana)  # Crear el pop-up relacionado con la ventana principal
    popup.title("Pop-up centrado")
    popup.geometry("300x200")  # Tamaño del pop-up
    popup.resizable(False, False)

    # Centrar el pop-up
    centrar_popup(popup, ventana)

    # Contenido del pop-up
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
        flujo_en_ejecucion = False  # Restablecer en caso de error
        return

    opcion_info = opcion_map.get(opcion)
    if not opcion_info:
        messagebox.showerror("Error", "Opción inválida seleccionada.")
        flujo_en_ejecucion = False  # Restablecer en caso de error
        return

    opcion_num = opcion_info["num"]
    base_url = opcion_info["url"]

    # Expandir la ventana para mostrar logs
    ventana.geometry("600x450")

    # Crear área de texto para los logs
    global text_area
    text_area = tk.Text(frame, wrap=tk.WORD, state="normal", font=("Arial", 10))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    text_area.tag_configure("red", foreground="red")
    text_area.tag_configure("green", foreground="green")
    text_area.tag_configure("orange", foreground="orange")
    text_area.tag_configure("blue", foreground="blue")
    text_area.tag_configure("black", foreground="black")

    # Redirigir sys.stdout al área de texto
    sys.stdout = RedirectOutput(text_area)

    def ejecutar_flujo():
        global flujo_en_ejecucion
        try:
            print("[INFO] Iniciando el flujo principal...")
            flujo_principal(usuario, contraseña, opcion_num, base_url)  # Pasamos base_url aquí
            print("[SUCCESS] Flujo principal completado.")
        except Exception as e:
            print(f"[ERROR] Ha ocurrido un error: {e}")
        finally:
            flujo_en_ejecucion = False  # Marcar el flujo como terminado
            sys.stdout = sys.__stdout__  # Restaurar sys.stdout al valor original

    # Ejecutar el flujo en un hilo separado
    hilo = threading.Thread(target=ejecutar_flujo)
    hilo.daemon = True
    hilo.start()

    mostrar_boton_finalizar()

def intentar_cerrar_ventana():
    """
    Intercepta el intento de cerrar la ventana.
    """
    if flujo_en_ejecucion:
        messagebox.showwarning("Advertencia", "El flujo principal aún no ha terminado. Por favor, espera.")
    else:
        ventana.destroy()  # Permitir el cierre si el flujo ha terminado

ventana = tk.Tk()

# Tamaño fijo de la ventana
window_width = 500  # Ancho fijo
window_height = 300  # Alto fijo

# Obtener tamaño de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()

# Calcular coordenadas para centrar la ventana
position_x = int((screen_width - window_width) / 2)
position_y = int((screen_height - window_height) / 2)

# Configurar la posición y tamaño inicial de la ventana
ventana.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

ventana.title("Sistema de Dispensación")
ventana.resizable(False, False)
ventana.protocol("WM_DELETE_WINDOW", intentar_cerrar_ventana)

frame = tk.Frame(ventana, bg="white")
frame.pack(fill="both", expand=True)

configurar_formulario_inicio()

ventana.mainloop()
