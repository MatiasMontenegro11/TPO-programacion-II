# TPO-programacion-II

# INTEGRANTES:
Gonzalez Luz - 
Gural Guadalupe - 
Liberato Dalila - 
Montenegro Matías - 
Rivas Ayelen


*** Inteligencia Retail - Librería ***

# Instalar librerías
Abrir la terminal en la carpeta del proyecto y escribir:

Mac: python3 -m pip install -r requirements.txt

Windows: python -m pip install -r requirements.txt

(requirements.txt tiene la lista de librerías que usa el programa)

# Crear un archivo .env con
GMAIL_USUARIO=

GMAIL_PASSWORD_APP=

API_KEY=clave_secreta_123

# Ejecutar el programa
Abrir main.py y ejecutarlo.

# API propia
cd "TP_Retail"

Mac: python3 -m uvicorn api_propia:app --reload

Windows: python -m uvicorn api_propia:app --reload

Abrir http://127.0.0.1:8000/docs, tocar Authorize y cargar la clave que está en `API_KEY` del `.env`.

Rutas: POST /generar, GET /reporte, GET /reporte/{sku}

# Cómo ejecutar la API propia paso a paso

La API no se ejecuta con el botón ▶. Se prende desde la terminal y se prueba desde el navegador.

1. Abrir la terminal en VS Code: menú **Terminal > New Terminal**.
2. Entrar a la carpeta donde están los archivos, escribiendo `cd "TP_Retail"`, y Enter.
3. Prender la API escribiendo el comando y Enter:
   - Mac: `python3 -m uvicorn api_propia:app --reload`
   - Windows: `python -m uvicorn api_propia:app --reload`
4. Esperar a que aparezca **"Application startup complete."**
   La terminal queda "trabada": es normal, la API está prendida esperando pedidos. No cerrarla.
5. Abrir en el navegador: http://127.0.0.1:8000/docs
6. Arriba a la derecha tocar **Authorize**, escribir la clave que está en `API_KEY` del `.env`, tocar **Authorize** y después **Close**.
7. Elegir una ruta, tocar **Try it out** y después **Execute**:
   - **POST /generar**: ejecuta todo el programa y devuelve el reporte nuevo (también manda el mail).
   - **GET /reporte**: muestra el último reporte completo.
   - **GET /reporte/{sku}**: muestra un solo libro. Escribir el código, por ejemplo `LIB-007`.
8. Abajo, en **Responses**, aparece la respuesta:
   - **200**: salió bien, se ven los datos.
   - **401**: falta la clave o es incorrecta.
   - **404**: no hay reporte todavía o el código del libro no existe.
9. Para apagar la API: en la terminal apretar **Ctrl + C**.
