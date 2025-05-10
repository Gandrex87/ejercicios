from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import os
import csv
import random
import sys 

# --- Constantes de Configuración ---
GECKODRIVER_PATH = "/Users/andresrsalamanca/Documents/geckodriver" # Cambiar por RUTA DEL GECKODRIVERa
BASE_URL = "https://quotes.toscrape.com"
KEYWORDS_TO_FILTER = ["life", "humor"] # Palabras clave para filtrar en el TEXTO de la cita
OUTPUT_CSV_FILE = "citas_filtradas_refactorizado.csv"

# Configuración para la Navegación Aleatoria por Subconjunto
RANGO_PAGINAS_INICIO = 1
RANGO_PAGINAS_FIN = 10     # El sitio tiene 10 páginas
MIN_NUM_PAGINAS_A_ESCOGER = 1 # Mínimo de páginas distintas a visitar del rango
MAX_NUM_PAGINAS_A_ESCOGER = 5 # Máximo de páginas distintas a visitar del rango

# --- Funciones de Utilidad y Pasos Lógicos ---

def inicializar_webdriver(geckodriver_path):
    """Inicializa y devuelve el WebDriver de Firefox."""
    print(f"Intentando usar GeckoDriver desde: {geckodriver_path}")
    if not os.path.isfile(geckodriver_path):
        print(f"Error: El archivo ejecutable 'geckodriver' no se encontró en '{geckodriver_path}'")
        sys.exit("GeckoDriver no encontrado. Terminando script.")

    firefox_options = FirefoxOptions()
    # firefox_options.add_argument("--headless") # Descomenta para ejecución sin UI

    service = FirefoxService(executable_path=geckodriver_path)
    
    print("Inicializando el navegador Firefox...")
    try:
        driver = webdriver.Firefox(service=service, options=firefox_options)
        print("Navegador Firefox inicializado exitosamente.")
        return driver
    except Exception as e_init_driver:
        print(f"Error CRÍTICO al inicializar GeckoDriver/Firefox: {e_init_driver}")
        sys.exit("Fallo al inicializar WebDriver. Terminando script.")

def seleccionar_paginas_a_visitar(rango_inicio, rango_fin, min_a_escoger, max_a_escoger):
    """Determina aleatoriamente una lista de números de página únicos a visitar de un rango dado."""
    paginas_disponibles_en_rango = list(range(rango_inicio, rango_fin + 1))
    print(f"Páginas disponibles para selección en el rango [{rango_inicio}-{rango_fin}]: {paginas_disponibles_en_rango}")

    # Ajustar el número máximo de páginas a escoger para que no exceda las disponibles
    num_max_real_a_escoger = min(max_a_escoger, len(paginas_disponibles_en_rango))
    # Ajustar el número mínimo para que no sea mayor que el máximo real
    num_min_real_a_escoger = min(min_a_escoger, num_max_real_a_escoger)

    k_paginas_a_visitar = 0
    if paginas_disponibles_en_rango and num_min_real_a_escoger <= num_max_real_a_escoger:
        k_paginas_a_visitar = random.randint(num_min_real_a_escoger, num_max_real_a_escoger)
    elif paginas_disponibles_en_rango: # Si min > max (ajustado), tomar todas las disponibles hasta min_real
        k_paginas_a_visitar = num_min_real_a_escoger 
    
    if k_paginas_a_visitar == 0:
        print("No se seleccionaron páginas para visitar según la configuración.")
        return []
    
    paginas_seleccionadas = random.sample(paginas_disponibles_en_rango, k_paginas_a_visitar)
    paginas_seleccionadas.sort() # Opcional para logs más claros
    print(f"Se visitarán {k_paginas_a_visitar} página(s) seleccionada(s) aleatoriamente: {paginas_seleccionadas}")
    return paginas_seleccionadas

def extraer_datos_cita(quote_element):
    """Extrae texto, autor y etiquetas de un WebElement de cita."""
    try:
        text = quote_element.find_element(By.CLASS_NAME, "text").text
    except NoSuchElementException: text = "N/A (texto no encontrado)"
    try:
        author = quote_element.find_element(By.CLASS_NAME, "author").text
    except NoSuchElementException: author = "N/A (autor no encontrado)"
    
    tags_list = []
    try:
        tags_container = quote_element.find_element(By.CLASS_NAME, "tags")
        tag_elements = tags_container.find_elements(By.CLASS_NAME, "tag")
        for tag_element in tag_elements:
            tags_list.append(tag_element.text)
    except NoSuchElementException:
        pass # No es un error si una cita no tiene etiquetas

    return {"cita": text, "autor": author, "etiquetas_originales": tags_list}

def filtrar_cita_por_palabras_clave(datos_cita, palabras_clave):
    """Verifica si el texto de la cita contiene alguna de las palabras clave."""
    texto_cita_lower = datos_cita["cita"].lower()
    for keyword in palabras_clave:
        if keyword.lower() in texto_cita_lower:
            return True
    return False

def scrapear_citas_de_una_pagina(driver_instance, url_de_pagina):
    """Navega a una URL y extrae todas las citas de esa página."""
    print(f"Accediendo a: {url_de_pagina}")
    driver_instance.get(url_de_pagina)
    
    citas_extraidas_de_pagina = []
    print("Esperando a que las citas carguen en la página...")
    try:
        WebDriverWait(driver_instance, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
        )
        print("Citas encontradas. Extrayendo información...")
        quote_elements = driver_instance.find_elements(By.CLASS_NAME, "quote")
        print(f"Se encontraron {len(quote_elements)} citas en esta página para procesar.")

        for q_element in quote_elements:
            info_cita = extraer_datos_cita(q_element)
            citas_extraidas_de_pagina.append(info_cita)
            
    except TimeoutException:
        print(f"Timeout: No se encontraron citas en '{url_de_pagina}' o la página no cargó a tiempo.")
    except Exception as e_scrape_page:
        print(f"Error al scrapear la página '{url_de_pagina}': {e_scrape_page}")
        
    return citas_extraidas_de_pagina

def guardar_datos_en_csv(lista_datos_filtrados, nombre_archivo):
    """Guarda una lista de diccionarios (citas filtradas) en un archivo CSV."""
    if not lista_datos_filtrados:
        print("No hay datos filtrados para guardar en CSV.")
        return

    print(f"\nGuardando {len(lista_datos_filtrados)} citas filtradas en '{nombre_archivo}'...")
    try:
        fieldnames = ['cita', 'autor', 'etiquetas'] # Columnas del CSV
        
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for data_item in lista_datos_filtrados:
                # Preparamos la fila para el CSV
                fila_a_escribir = {
                    'cita': data_item['cita'],
                    'autor': data_item['autor'],
                    'etiquetas': ", ".join(data_item['etiquetas_originales']) # Unir lista de etiquetas
                }
                writer.writerow(fila_a_escribir)
        print(f"Datos guardados exitosamente en '{nombre_archivo}'.")
    except Exception as e_csv:
        print(f"Error al guardar los datos en CSV: {e_csv}")

# --- Flujo Principal del Script ---
def ejecutar_scraping():
    """Orquesta todo el proceso de scraping."""
    driver_selenium = None
    citas_filtradas_global = []
    textos_citas_procesadas = set() # Para evitar duplicados si visitamos la misma cita por diferentes vías

    try:
        driver_selenium = inicializar_webdriver(GECKODRIVER_PATH)
        
        paginas_a_visitar_lista = seleccionar_paginas_a_visitar(
            RANGO_PAGINAS_INICIO, 
            RANGO_PAGINAS_FIN, 
            MIN_NUM_PAGINAS_A_ESCOGER, 
            MAX_NUM_PAGINAS_A_ESCOGER
        )

        if not paginas_a_visitar_lista:
            print("No se han seleccionado páginas para visitar. Terminando.")
            return # Salir de la función si no hay páginas

        for numero_de_pagina in paginas_a_visitar_lista:
            url_pagina_a_scrapear = ""
            if numero_de_pagina == 1 and BASE_URL.endswith("/"): # Evitar doble //
                 url_pagina_a_scrapear = BASE_URL
            elif numero_de_pagina == 1:
                 url_pagina_a_scrapear = BASE_URL + "/"
            else:
                url_pagina_a_scrapear = f"{BASE_URL}/page/{numero_de_pagina}/"
            
            print(f"\n--- Procesando Página {numero_de_pagina} ---")
            citas_de_pagina_actual = scrapear_citas_de_una_pagina(driver_selenium, url_pagina_a_scrapear)

            for datos_de_cita in citas_de_pagina_actual:
                if filtrar_cita_por_palabras_clave(datos_de_cita, KEYWORDS_TO_FILTER):
                    # Evitar duplicados si la misma cita aparece en diferentes páginas seleccionadas
                    if datos_de_cita["cita"] not in textos_citas_procesadas:
                        citas_filtradas_global.append(datos_de_cita)
                        textos_citas_procesadas.add(datos_de_cita["cita"])
                        
                        # Imprimir la cita filtrada (opcional)
                        print("-" * 20)
                        print(f"Cita (Coincide Filtro): {datos_de_cita['cita']}")
                        print(f"Autor: {datos_de_cita['autor']}")
                        if datos_de_cita['etiquetas_originales']: 
                            print(f"Etiquetas: {', '.join(datos_de_cita['etiquetas_originales'])}")
            
            time.sleep(random.uniform(1.0, 2.5)) # Pausa aleatoria y educada entre páginas

        guardar_datos_en_csv(citas_filtradas_global, OUTPUT_CSV_FILE)

    except SystemExit as e_exit: # Captura sys.exit() de inicializar_webdriver
        print(f"Script terminado controladamente: {e_exit}")
    except Exception as e_main_flow:
        print(f"Ocurrió un ERROR INESPERADO en el flujo principal del scraping: {e_main_flow}")
    finally:
        if driver_selenium:
            print("Cerrando el navegador Firefox...")
            driver_selenium.quit()
            print("Navegador Firefox cerrado.")
        print("\nFin de la ejecución del script de scraping.")

if __name__ == "__main__":
    ejecutar_scraping()