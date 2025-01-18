# Proyecto de Automatización de Dispensación

Este proyecto es una aplicación de automatización para la dispensación de medicamentos utilizando Selenium para la automatización del navegador y xlwings para la manipulación de archivos Excel. La interfaz gráfica está construida con Tkinter.

## Archivos Principales

- [`bot.py`](bot.py): Punto de entrada principal del programa.
- [`browser.py`](browser.py): Contiene funciones para inicializar el navegador y manejar la sesión de usuario.
- [`excel.py`](excel.py): Funciones para conectar y manipular archivos Excel.
- [`finalization.py`](finalization.py): Funciones para finalizar el programa y guardar logs.
- [`interfaz.py`](interfaz.py): Interfaz gráfica construida con Tkinter.
- [`logger.py`](logger.py): Funciones para el manejo de logs.
- [`main.py`](main.py): Contiene el flujo principal de la aplicación.

## Estructura del Proyecto

```plaintext
Proyecto/
├── __pycache__/
├── _init_.py
├── bot.py
├── bot.spec
├── browser.py
├── build/
│   ├── bot/
│   │   ├── Analysis-00.toc
│   │   ├── bot.pkg
│   │   ├── EXE-00.toc
│   ├── Sistema de Dispensación/
│       └── ...
├── config.py
├── core.js.xhtml
├── data_processing.py
├── env/
│   ├── .gitignore
│   ├── Include/
│   ├── Lib/
│   ├── pyvenv.cfg
│   ├── Scripts/
├── excel.py
├── finalization.py
├── fondo.avif
├── font-awesome.css.xhtml
├── interfaz.py
├── jquery-plugins.js.xhtml
├── jquery.js.xhtml
├── logger.py
├── logs/
├── main.py
├── npt_verification.py
├── sanitization.py
├── security/
│   └── clave.key
├── security.py
├── Sistema de Dispensación.spec
├── theme.css.xhtml
└── utils.py
```

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu_usuario/tu_repositorio.git
    ```
2. Navega al directorio del proyecto:
    ```sh
    cd tu_repositorio
    ```
3. Crea y activa un entorno virtual:
    ```sh
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```
4. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta el script principal:
    ```sh
    python bot.py
    ```
2. Completa los campos de la interfaz gráfica y sigue las instrucciones para iniciar el flujo de dispensación.

## Contribución

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contacto

Para cualquier consulta o sugerencia, por favor abre un issue en el repositorio o contacta al mantenedor del proyecto.