# EJERCICIO_1 Legalia Automator

Un script en Python que automatiza el flujo de trabajo principal de la aplicación **Legalia** usando **pywinauto**.  
Realiza los siguientes pasos:

1. **Lanza** la aplicación desde un acceso directo en el Escritorio  
2. **Navega** por el menú (`Alt+F`, `Ctrl+A`) para abrir el cuadro de selección  
3. **Selecciona** el depósito “PRUEBA_2” y pulsa **Abrir**  
4. **Pulsa** el botón **Comprobar Reglas** en el formulario  
5. **Captura** el mensaje de error que aparece, lo guarda en `resultado.txt` y cierra el diálogo  
6. **Cierra** la aplicación al finalizar

---

## Requisitos

- Windows 10/11  
- Python 3.8+
- ver requirements.txt

# EJERCICIO_2 Scraper de Citas Web con Selenium y Firefox

Este script de Python utiliza la librería Selenium para automatizar el navegador Firefox y extraer (scrapear) citas del sitio web [https://quotes.toscrape.com/](https://quotes.toscrape.com/).

## Funcionalidades Principales

1.  **Navegación Aleatoria:** Accede a un número aleatorio de páginas dentro de un rango configurable del sitio.
2.  **Extracción de Datos:** De cada página visitada, extrae:
    * El texto de la cita.
    * El autor de la cita.
    * Las etiquetas (tags) asociadas a la cita.
3.  **Filtrado por Palabras Clave:** Después de extraer las citas, las filtra para conservar solo aquellas cuyo texto contenga alguna de las palabras clave especificadas (por ejemplo, "life" o "humor").
4.  **Guardado en CSV:** Los datos de las citas filtradas se guardan en un archivo CSV.

## Requisitos Previos

Antes de ejecutar el script, necesitarás tener instalado lo siguiente:

1.  **Python 3.x:** Si no lo tienes, descárgalo desde [python.org](https://www.python.org/).
2.  **Navegador Firefox:** Descárgalo desde [mozilla.org](https://www.mozilla.org/firefox/new/).
3.  **Librería Selenium para Python:**
    ```bash
    pip install selenium
    ```
4.  **GeckoDriver (WebDriver para Firefox):**
    * Descarga la versión de GeckoDriver que sea compatible con tu versión de Firefox desde la página oficial de releases: [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)
    * **Importante para usuarios de Mac (ARM64/Apple Silicon):** Asegúrate de descargar la versión `macos-aarch64.tar.gz` (o la que corresponda a tu arquitectura).
    * Descomprime el archivo descargado (obtendrás un ejecutable llamado `geckodriver`).
    * Coloca el ejecutable `geckodriver` en una ubicación conocida en tu sistema.
    * **En macOS y Linux:** Dale permisos de ejecución al archivo:
        ```bash
        chmod +x /ruta/completa/a/tu/geckodriver
        ```
    * **En macOS (Gatekeeper):** La primera vez que intentes usarlo, macOS podría bloquearlo. Para permitirlo:
        * En Finder, navega hasta `geckodriver`, haz Control-clic (o clic derecho) sobre él, selecciona "Abrir" y confirma en el diálogo.
        * Alternativamente, desde la Terminal: `xattr -d com.apple.quarantine /ruta/completa/a/tu/geckodriver`

## Configuración del Script

Antes de ejecutar, abre el script de Python (`ejercicio_2.py` :

* **`GECKODRIVER_PATH`**: **DEBES** actualizar esta variable con la ruta completa al ejecutable `geckodriver`.
* `KEYWORDS_TO_FILTER`: Lista de palabras clave para filtrar las citas (ej. `["life", "humor"]`).
* `OUTPUT_CSV_FILE`: Nombre del archivo CSV donde se guardarán los resultados (ej. `"citas_filtradas_refactorizado.csv"`).
* `RANGO_PAGINAS_INICIO` y `RANGO_PAGINAS_FIN`: Definen el subconjunto de páginas del cual el script seleccionará algunas para visitar (ej. del 1 al 10).
* `MIN_NUM_PAGINAS_A_ESCOGER` y `MAX_NUM_PAGINAS_A_ESCOGER`: Definen cuántas páginas distintas, de forma aleatoria, se visitarán del rango anterior.

## Estructura del Código

El script está organizado en varias funciones:

* `inicializar_webdriver()`: Configura e inicia el WebDriver de Selenium con Firefox.
* `seleccionar_paginas_a_visitar()`: Determina aleatoriamente la lista de números de página a visitar.
* `extraer_datos_cita()`: Extrae el texto, autor y etiquetas de un elemento web de cita individual.
* `filtrar_cita_por_palabras_clave()`: Verifica si una cita contiene las palabras clave deseadas.
* `scrapear_citas_de_una_pagina()`: Gestiona la navegación a una URL específica y la extracción de todas las citas de esa página.
* `guardar_datos_en_csv()`: Escribe los datos filtrados en un archivo CSV.
* `ejecutar_scraping()`: Función principal que orquesta todo el flujo de trabajo.

## Cómo Ejecutar el Script

1.  Asegúrar haber cumplido con todos los "Requisitos Previos".
2.  Actualiza la constante `GECKODRIVER_PATH` (y otras si lo deseas) en el script de Python.
3.  Abre una terminal o símbolo del sistema.
4.  Navega hasta el directorio donde guardaste el script.
5.  Ejecuta el script con Python:
    ```bash
    python tu_nombre_de_script.py
    ```