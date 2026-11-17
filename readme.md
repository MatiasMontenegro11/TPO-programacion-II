# Inteligencia Retail - Librería

## Instalar librerías
python3 -m pip install python-dotenv requests beautifulsoup4 pandas openpyxl matplotlib certifi fastapi uvicorn

## Crear un archivo .env con
GMAIL_USUARIO=
GMAIL_PASSWORD_APP=

## Ejecutar el programa
Abrir main.py y ejecutarlo.

## API propia
cd "TP Retail"
python3 -m uvicorn api_propia:app --reload

Abrir http://127.0.0.1:8000/docs, tocar Authorize y cargar la clave.

Rutas: POST /generar, GET /reporte, GET /reporte/{sku}

## Cómo ejecutar la API propia paso a paso

La API no se ejecuta con el botón ▶. Se prende desde la terminal y se prueba desde el navegador.

1. Abrir la terminal en VS Code: menú **Terminal > New Terminal**.
2. Entrar a la carpeta del TP escribiendo `cd "TP Retail"` y Enter.
   Antes del `$` tiene que decir **TP Retail**.
3. Prender la API escribiendo `python3 -m uvicorn api_propia:app --reload` y Enter.
4. Esperar a que aparezca **"Application startup complete."**
   La terminal queda "trabada": es normal, la API está prendida esperando pedidos. No cerrarla.
5. Abrir en el navegador: http://127.0.0.1:8000/docs
6. Arriba a la derecha tocar **Authorize**, escribir la clave `clave_secreta_123`, tocar **Authorize** y después **Close**.
7. Elegir una ruta, tocar **Try it out** y después **Execute**:
   - **POST /generar**: ejecuta todo el programa y devuelve el reporte nuevo (también manda el mail).
   - **GET /reporte**: muestra el último reporte completo.
   - **GET /reporte/{sku}**: muestra un solo libro. Escribir el código, por ejemplo `LIB-007`.
8. Abajo, en **Responses**, aparece la respuesta:
   - **200**: salió bien, se ven los datos.
   - **401**: falta la clave o es incorrecta.
   - **404**: no hay reporte todavía o el código del libro no existe.
9. Para probar que la clave funciona: tocar **Authorize > Logout** y ejecutar cualquier ruta. Tiene que dar **401**.
10. Para apagar la API: en la terminal apretar **Ctrl + C**.

### Si aparece un error
- **Could not import module "api_propia"**: la terminal no está en la carpeta. Hacer `cd "TP Retail"`.
- **Address already in use**: ya hay una API prendida. Escribir `lsof -ti:8000 | xargs kill` y volver al paso 3.
- **No module named fastapi**: falta instalar. Escribir `python3 -m pip install fastapi uvicorn`.