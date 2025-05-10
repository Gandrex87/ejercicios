# Legalia Automator

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