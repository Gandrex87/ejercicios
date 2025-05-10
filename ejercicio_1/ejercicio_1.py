from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto import Desktop
import os
import time

class LegaliaAutomator:
    """
    Automatiza el flujo de trabajo principal de la aplicación Legalia:
      1. Lanzar la app y conectar
      2. Navegar menú para abrir cuadro de selección
      3. Seleccionar depósito y Abrir
      4. Pulsar Comprobar Reglas
      5. Capturar y cerrar diálogo de error
      6. Cerrar la aplicación
    """
    def __init__(self):
        # — Configuración global —
        public = os.environ.get('PUBLIC', r"C:\Users\Public")
        user   = os.environ.get('USERPROFILE', r"C:\Users\Default")
        desktop_public = os.path.join(public, 'Desktop')
        desktop_user   = os.path.join(user,   'Desktop')
        shortcut_name  = "Legalia 2.lnk"

        self.shortcut_path = os.path.join(desktop_public, shortcut_name)
        if not os.path.exists(self.shortcut_path):
            candidate = os.path.join(desktop_user, shortcut_name)
            if os.path.exists(candidate):
                self.shortcut_path = candidate
            else:
                raise FileNotFoundError(f"No encontré '{shortcut_name}' en {desktop_public} ni en {desktop_user}")

        # — Titulares y IDs —
        self.title_main      = "Legalización de libros"
        self.dialog_title    = "Selección de la legalización de libros"
        self.dialog_auto_id  = "frmAbrirLegalizacion"
        self.list_auto_id    = "lsvLegalizaciones"
        self.deposit_name    = "PRUEBA_2"
        self.open_btn_auto   = "btnSeleccionar"

        self.form_title      = "Legalización de libros - PRUEBA_2 - Paquete de prueba 2"
        self.form_auto_id    = "frmMDIPrincipal"
        self.toolbar_auto_id = "ToolStrip"
        self.check_btn_title = "Comprobar Reglas"

        self.error_title     = "Legalia 2"
        self.error_text_id   = "65535"
        self.error_ok_id     = "2"

        # Wrappers
        self.app                = None
        self.main_window        = None
        self.selection_dialog   = None
        self.form_window        = None

    def launch_and_connect(self):
        """
        Paso 1: Ejecuta el acceso directo y conecta con la ventana principal.
        """
        print("Paso 1: Abriendo Legalia…")
        os.startfile(self.shortcut_path)
        time.sleep(5)
        self.app = Application(backend="uia").connect(title=self.title_main, timeout=30)
        self.main_window = self.app.window(title=self.title_main)
        self.main_window.wait('ready visible enabled', timeout=10)
        print("  ✓ Ventana principal lista")

    def navigate_menu(self):
        """
        Paso 2: Abre el menú mediante atajos Alt+F, Ctrl+A.
        """
        print("Paso 2: Navegando menú (Alt+F, Ctrl+A)…")
        win = self.main_window
        win.set_focus()
        win.type_keys('%F', pause=0.7)
        win.type_keys('^A', pause=0.7)
        time.sleep(3)
        print("  ✓ Menú abierto")

    def select_book(self):
        """
        Paso 3: Selecciona el depósito PRUEBA_2 en el diálogo de selección.
        """
        print(f"Paso 3: Seleccionando depósito '{self.deposit_name}'…")
        dlg = self.main_window.child_window(
            title=self.dialog_title,
            auto_id=self.dialog_auto_id,
            control_type="Window"
        )
        dlg.wait('ready visible enabled', timeout=30)
        dlg.set_focus()
        lst = dlg.child_window(auto_id=self.list_auto_id, control_type="List")
        lst.wait('ready visible', timeout=15)
        item = lst.get_item(self.deposit_name)
        if not item.is_selected():
            item.select()
        time.sleep(0.5)
        btn = dlg.child_window(auto_id=self.open_btn_auto, control_type="Button")
        btn.wait('enabled visible', timeout=10).click_input()
        dlg.wait_not('visible', timeout=15)
        time.sleep(2)
        self.selection_dialog = dlg
        print("  ✓ Diálogo de selección completado")

    def press_check_rules(self):
        """
        Paso 4: Pulsa el botón 'Comprobar Reglas' en el formulario.
        """
        print(f"Paso 4: Presionando '{self.check_btn_title}'…")
        frm = self.app.window(title=self.form_title, auto_id=self.form_auto_id)
        frm.wait('ready visible enabled', timeout=20).set_focus()
        tb = frm.child_window(auto_id=self.toolbar_auto_id, control_type="ToolBar")
        tb.wait('ready visible', timeout=10)
        btn = tb.child_window(title=self.check_btn_title, control_type="Button")
        btn.wait('enabled visible', timeout=10).click_input()
        time.sleep(5)
        self.form_window = frm
        print("  ✓ Botón de comprobación pulsado")

    def handle_error_dialog(self):
        """
        Paso 5: Captura el mensaje de error, lo guarda y cierra el diálogo.
        """
        print("Paso 5: Capturando mensaje y cerrando error…")
        frm = self.form_window
        dlg = frm.child_window(title=self.error_title, control_type="Window")
        dlg.wait('ready visible enabled', timeout=20).set_focus()

        txt_ctrl = dlg.child_window(auto_id=self.error_text_id, control_type="Text")
        txt_ctrl.wait('visible', timeout=10)
        msg = txt_ctrl.window_text()
        print(f"  → Mensaje de error: '{msg}'")
        
        # Guardar a archivo
        with open("resultado.txt", "w", encoding="utf-8") as f:
            f.write(msg)
        print("  → Mensaje guardado en 'resultado.txt'")

        ok_btn = dlg.child_window(auto_id=self.error_ok_id, control_type="Button")
        ok_btn.wait('enabled visible', timeout=10).click_input()
        time.sleep(1)
        print("  ✓ Diálogo de error cerrado")

    def close_application(self):
        """
        Paso 6: Cierra la ventana del formulario y el proceso si sigue activo.
        """
        print("Paso 6: Cerrando Legalia…")
        frm = self.form_window
        frm.set_focus()
        frm.close()
        time.sleep(3)
        if self.app.is_process_running():
            self.app.kill(soft=False)
            time.sleep(2)
        print("  ✓ Aplicación cerrada")

    def run_all(self):
        try:
            self.launch_and_connect()
            self.navigate_menu()
            self.select_book()
            self.press_check_rules()
            self.handle_error_dialog()
        except Exception as e:
            print(f"ERROR en la automatización: {e}")
            raise
        finally:
            if self.form_window and self.form_window.exists(timeout=1):
                self.close_application()
            print("\n--- Script completado ---")

if __name__ == "__main__":
    automator = LegaliaAutomator()
    automator.run_all()
