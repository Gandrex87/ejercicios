from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto import Desktop
import time
import os

# --- Variables Globales / Configurables ---
main_window_title_inicial = "Legalización de libros"


titulo_dialogo_seleccion = 'Selección de la legalización de libros'
auto_id_dialogo_seleccion = "frmAbrirLegalizacion"
deposito_a_seleccionar = "PRUEBA_2"
auto_id_lista_depositos = "lsvLegalizaciones"
auto_id_boton_abrir_dialogo = "btnSeleccionar"
texto_boton_abrir_dialogo = "Abrir"

titulo_ventana_con_formulario = "Legalización de libros - PRUEBA_2 - Paquete de prueba 2"
auto_id_ventana_con_formulario = "frmMDIPrincipal"

auto_id_toolbar_en_formulario = "ToolStrip"
title_boton_comprobar_reglas = "Comprobar Reglas"

# Para la ventana de error (Paso 5) - Título y IDs obtenidos de tu print_control_identifiers
titulo_ventana_error_esperado = "Legalia 2"
auto_id_texto_error_msg = "65535"      # << Definido aquí
auto_id_boton_ok_error_dialogo = "2"   # << Definido aquí
texto_boton_ok_error_dialogo = "OK"  # El título del botón OK

app = None
main_win_ref_inicial = None
ventana_formulario_actual = None
dialogo_interaccion = None
ventana_error = None



# Ruta al acceso directo de forma más genérica
try:
    # Obtener la ruta de la carpeta pública y construir la ruta al Escritorio Público
    public_folder = os.environ['PUBLIC']
    public_desktop_path = os.path.join(public_folder, 'Desktop')
    shortcut_name = "Legalia 2.lnk" # Asumimos que el nombre del acceso directo es consistente
    shortcut_path = os.path.join(public_desktop_path, shortcut_name)

    # Verificar si el acceso directo existe en esa ubicación
    if not os.path.exists(shortcut_path):
        print(f"ADVERTENCIA: El acceso directo '{shortcut_name}' no se encontró en el Escritorio Público: {public_desktop_path}")
        # Podrías intentar otra ubicación común aquí, como el escritorio del usuario actual
        user_profile_folder = os.environ['USERPROFILE']
        user_desktop_path = os.path.join(user_profile_folder, 'Desktop')
        shortcut_path_user = os.path.join(user_desktop_path, shortcut_name)
        if os.path.exists(shortcut_path_user):
            print(f"Se encontró el acceso directo en el Escritorio del Usuario Actual: {shortcut_path_user}")
            shortcut_path = shortcut_path_user
        else:
            print(f"ADVERTENCIA: El acceso directo tampoco se encontró en el Escritorio del Usuario Actual: {user_desktop_path}")
            print("Por favor, verifica la ubicación y el nombre del acceso directo 'Legalia 2.lnk' o actualiza la ruta en el script.")
            # Podrías decidir salir si no se encuentra, o pedir la ruta al usuario.
            # Por ahora, el script podría fallar más adelante si shortcut_path no es válido.
            # sys.exit("Error: No se pudo localizar el acceso directo de Legalia.") # Descomenta para salir si no se encuentra
    else:
        print(f"Usando acceso directo encontrado en: {shortcut_path}")

except KeyError as e_env:
    print(f"Error: No se pudo encontrar la variable de entorno necesaria ({e_env}). Usando una ruta por defecto (esto podría fallar).")
    # Ruta de fallback si no se pueden obtener las variables de entorno (menos probable)
    shortcut_path = r"C:\Users\Public\Desktop\Legalia 2.lnk"

# --- PASO 1, 2, 3, 4 (Como los teníamos y funcionaban) ---
try:
    print("Paso 1: Abriendo Legalia...")
    os.startfile(shortcut_path)
    time.sleep(5)
    app = Application(backend="uia").connect(title=main_window_title_inicial, timeout=30)
    main_win_ref_inicial = app.window(title=main_window_title_inicial)
    main_win_ref_inicial.wait('ready', timeout=10)
    print(f"Ventana '{main_win_ref_inicial.window_text()}' encontrada y lista.")

    print("\nPaso 2: Navegando al menú (Alt+F, Ctrl+A)...")
    main_win_ref_inicial.set_focus()
    main_win_ref_inicial.type_keys('%F', pause=0.7)
    main_win_ref_inicial.type_keys('^A', pause=0.7)
    time.sleep(3)
    print("Pasos 1 y 2 completados.")

    print(f"\nPaso 3: Interactuando con diálogo '{titulo_dialogo_seleccion}'...")
    dialogo_interaccion = main_win_ref_inicial.child_window(
        title=titulo_dialogo_seleccion, auto_id=auto_id_dialogo_seleccion, control_type="Window")
    dialogo_interaccion.wait('ready', timeout=30)
    dialogo_interaccion.set_focus()
    lista_control = dialogo_interaccion.child_window(auto_id=auto_id_lista_depositos, control_type="List")
    lista_control.wait('ready', timeout=15)
    item_a_seleccionar_wrapper = lista_control.get_item(deposito_a_seleccionar)
    if not item_a_seleccionar_wrapper.is_selected():
        item_a_seleccionar_wrapper.select()
    time.sleep(0.5)
    boton_abrir_dialogo = dialogo_interaccion.child_window(auto_id=auto_id_boton_abrir_dialogo, control_type="Button")
    boton_abrir_dialogo.wait('enabled', timeout=10)
    boton_abrir_dialogo.click_input()
    dialogo_interaccion.wait_not('visible', timeout=15)
    time.sleep(2)
    print(f"Interacción con diálogo '{titulo_dialogo_seleccion}' completada.")

    print(f"\nPaso 4: Clic en '{title_boton_comprobar_reglas}' en formulario '{titulo_ventana_con_formulario}'...")
    ventana_formulario_actual = app.window(title=titulo_ventana_con_formulario, auto_id=auto_id_ventana_con_formulario)
    ventana_formulario_actual.wait('ready', timeout=20)
    ventana_formulario_actual.set_focus()
    current_form_title_check = ventana_formulario_actual.window_text()
    print(f"Ventana del formulario encontrada y activa: '{current_form_title_check}'.")
    tool_bar = ventana_formulario_actual.child_window(auto_id=auto_id_toolbar_en_formulario, control_type="ToolBar")
    tool_bar.wait('ready', timeout=10)
    boton_comprobar = tool_bar.child_window(title=title_boton_comprobar_reglas, control_type="Button")
    boton_comprobar.wait('enabled', timeout=10)
    boton_comprobar.click_input()
    print(f"Botón '{title_boton_comprobar_reglas}' presionado.")
    print("Esperando (5 segundos) a que aparezca la ventana de error...")
    time.sleep(5)
    print("\nPaso 4 completado. La ventana de error debería estar visible.")

except Exception as e_prev:
    print(f"Error en Pasos 1-4: {e_prev}")
    active_window_for_error = ventana_formulario_actual if ventana_formulario_actual and ventana_formulario_actual.exists(timeout=1) else main_win_ref_inicial
    if active_window_for_error and active_window_for_error.exists(timeout=1):
        try:
            active_window_for_error.capture_as_image().save("error_pasos_1_a_4.png")
            print("Captura de pantalla 'error_pasos_1_a_4.png' guardada.")
        except ImportError: print("PIL/Pillow no instalado para capturas.")
        except Exception: pass
    exit()

# --- PASO 5: CAPTURAR MENSAJE DE ERROR, GUARDAR Y "CERRAR" DIÁLOGO DE ERROR ---
if ventana_formulario_actual and ventana_formulario_actual.exists(timeout=1):
    try:
        print(f"\nPaso 5: Buscando la ventana de error '{titulo_ventana_error_esperado}' como hija de '{ventana_formulario_actual.window_text()}'...")
        time.sleep(1)

        ventana_error = ventana_formulario_actual.child_window(
            title=titulo_ventana_error_esperado,
            control_type="Window"
        )
        print(f"Esperando que la ventana de error '{titulo_ventana_error_esperado}' esté lista...")
        ventana_error.wait('ready', timeout=20)
        ventana_error.set_focus()
        titulo_real_error_encontrado = ventana_error.window_text()
        print(f"Ventana de error encontrada: '{titulo_real_error_encontrado}'. Está lista y enfocada.")

        print(f"Capturando el texto del error del control con auto_id='{auto_id_texto_error_msg}'...")
        control_texto_error = ventana_error.child_window(
            auto_id=auto_id_texto_error_msg, control_type="Text")
        control_texto_error.wait('visible', timeout=10)
        texto_capturado = control_texto_error.window_text()
        print(f"Texto del error capturado: '{texto_capturado}'")

        nombre_fichero_resultado = "resultado.txt"
        with open(nombre_fichero_resultado, "w", encoding="utf-8") as f:
            f.write(texto_capturado)
        print(f"Mensaje de error guardado en '{nombre_fichero_resultado}'.")

        print(f"Buscando el botón 'OK' (auto_id='{auto_id_boton_ok_error_dialogo}') en la ventana de error...")
        boton_ok_error = ventana_error.child_window(
            auto_id=auto_id_boton_ok_error_dialogo, control_type="Button")
        boton_ok_error.wait('enabled', timeout=10)
        print(f"Botón 'OK' encontrado. Haciendo clic...")
        boton_ok_error.click_input()
        print(f"Botón 'OK' presionado.")

        # MODIFICACIÓN: Simplemente esperamos un momento después de hacer clic en OK.
        print("Esperando 1 segundo para que el diálogo de error se procese/cierre...")
        time.sleep(1)
        if ventana_error.exists(timeout=0.5) and ventana_error.is_visible(): # Comprobación rápida
             print(f"Advertencia: La ventana de error '{titulo_real_error_encontrado}' todavía parece estar visible.")
        else:
             print(f"Ventana de error '{titulo_real_error_encontrado}' parece cerrada o ya no es visible.")
        print("\nPaso 5 completado.")

    except ElementNotFoundError as e_nf_err:
        print(f"Error CRÍTICO en Paso 5 (ElementNotFound): {e_nf_err}")
        exit()
    except Exception as e_err:
        print(f"Error general en Paso 5 (Manejar ventana de error): {e_err}")
        exit()
else:
    print("Paso 5 (manejo de ventana de error) omitido.")
    exit()

# --- PASO 6: CERRAR LEGALIA ---
if ventana_formulario_actual and ventana_formulario_actual.exists(timeout=1):
    try:
        print(f"\nPaso 6: Intentando cerrar la aplicación Legalia (ventana: '{ventana_formulario_actual.window_text()}')...")
        ventana_formulario_actual.set_focus()
        
        print("Enviando comando de cierre (close)...")
        ventana_formulario_actual.close()
        
        print("Esperando 3 segundos para que la aplicación se cierre...")
        time.sleep(3)
        
        if app.is_process_running():
            print("Advertencia: El proceso de la aplicación Legalia SIGUE CORRIENDO después de 'close()'.")
            print("Esto puede ser debido a diálogos de confirmación no guardados o manejo especial del cierre.")
            print("Intentando forzar el cierre con app.kill()...")
            try:
                app.kill(soft=False) # soft=False es más contundente (equivale a Terminar Proceso)
                print("Comando app.kill() enviado. Esperando 2 segundos adicionales...")
                time.sleep(2)
                if not app.is_process_running():
                    print("Aplicación Legalia cerrada exitosamente con app.kill().")
                else:
                    print("Error: La aplicación Legalia AÚN sigue corriendo incluso después de app.kill().")
            except Exception as e_kill:
                print(f"Error al intentar app.kill(): {e_kill}")
        else:
            print("Aplicación Legalia cerrada exitosamente con el comando close().")

    except Exception as e_close:
        print(f"Error durante el cierre de Legalia: {e_close}")
else:
    print("Paso 6 (cerrar Legalia) omitido.")

print("\n--- Script de Automatización Completado ---")