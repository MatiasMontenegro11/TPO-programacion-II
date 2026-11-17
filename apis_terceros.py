# MÓDULO DE DATOS DE TERCEROS
# Todo lo que viene de afuera de la empresa:
#   1. Permisos del sitio del competidor (robots.txt)
#   2. Precios del competidor con web scraping (books.toscrape.com)
#   3. Cotización de la libra con una API 
#   4. Envío del resumen con POST

import urllib.robotparser            # para armar direcciones web (la del robots.txt)
import urllib.parse                 # para leer el robots.txt

import requests                     # para pedir páginas y APIs por internet (GET y POST)
from bs4 import BeautifulSoup       # para leer el HTML y buscar los datos


# ---------------------------------------------------------------------
# CONFIGURACIÓN

URL_COMPETIDOR = "http://books.toscrape.com/"

# API pública de tipo de cambio sin API KEY

URL_API_CAMBIO = "https://open.er-api.com/v6/latest/GBP"

# Servicio de prueba que recibe datos por POST y los devuelve

URL_POST = "https://httpbin.org/post"

# Headers

HEADERS = {
    "User-Agent": "LibreriaInteligenciaBot/1.0 (proyecto academico UADE)"
}

TIMEOUT = 10           # segundos máximos de espera por respuesta

# ---------------------------------------------------------------------
# 1. Permisos Robots.txt

def puede_scrapear(url):
    """Lee el robots.txt del sitio y responde si nos deja entrar."""
    lector = urllib.robotparser.RobotFileParser()
    lector.set_url(urllib.parse.urljoin(url, "/robots.txt"))
    try:
        lector.read()
    except Exception:
        print("  No se pudo leer robots.txt: por precaución no entramos.")
        return False
    return lector.can_fetch(HEADERS["User-Agent"], url)

# ---------------------------------------------------------------------
# 2. WEB SCRAPING: precios del competidor

def scrapear_competidor(cantidad_paginas=1):
    """
    Descarga las páginas del catálogo del competidor y saca de cada libro:
    título, precio en libras y disponibilidad.

    Devuelve un DICCIONARIO: {titulo_normalizado: datos_del_libro}
    así después es fácil buscar un libro por su título.
    """
    # Importamos acá la función para no repetir código
    from funciones import normalizar_titulo

    libros = {}

    for numero in range(1, cantidad_paginas + 1):
        if numero == 1:
            url = URL_COMPETIDOR
        else:
            url = urllib.parse.urljoin(URL_COMPETIDOR, f"catalogue/page-{numero}.html")

        print(f"  Descargando {url} ...")
        try:
            respuesta = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            respuesta.raise_for_status()     # error si el status es 4xx o 5xx
        except requests.exceptions.RequestException as error:
            print(f"  Error al descargar la página: {error}")
            continue                         # seguimos con la próxima página

        respuesta.encoding = "utf-8"         # para que el símbolo £ se lea bien
        sopa = BeautifulSoup(respuesta.text, "html.parser")

        # find_all: todos los <article class="product_pod"> (uno por libro)
        articulos = sopa.find_all("article", class_="product_pod")

        for articulo in articulos:
            enlace = articulo.find("h3").find("a")
            titulo = enlace.get("title")                     # atributo title

            texto_precio = articulo.find("p", class_="price_color").get_text()  # "£51.77"
            precio = float(texto_precio.replace("£", "").replace("Â", "").strip())

            texto_stock = articulo.find("p", class_="instock").get_text()
            disponible = "In stock" in texto_stock

            libros[normalizar_titulo(titulo)] = {
                "titulo": titulo,
                "precio_libras": precio,
                "disponible": disponible,
            }

    return libros

# ---------------------------------------------------------------------
# 3. API PÚBLICA: cotización de la libra (GET)

def obtener_tasa_libra():
    """
    Consulta cuántos pesos argentinos vale 1 libra
    Y devuelve un número (float) o None si hubo un error.
    """
    try:
        respuesta = requests.get(URL_API_CAMBIO, headers=HEADERS, timeout=TIMEOUT)
        respuesta.raise_for_status()          
        datos = respuesta.json()              # JSON: diccionario de Python
        tasa = datos["rates"]["ARS"]
        print(f"  Status HTTP: {respuesta.status_code}")
        return tasa
    except requests.exceptions.RequestException as error:
        print(f"  No se pudo conectar con la API: {error}")
    except KeyError:
        print("  La respuesta de la API no tiene el dato esperado.")
    return None


# ---------------------------------------------------------------------
# 4. POST: enviar el resumen del análisis

def enviar_resumen_post(resumen):
    """
    Envía el resumen con el método POST.
    Usamos httpbin.org, un servicio de prueba que devuelve lo que le mandamos.
    """
    try:
        respuesta = requests.post(URL_POST, json=resumen, headers=HEADERS, timeout=TIMEOUT)
        respuesta.raise_for_status()
        recibido = respuesta.json()["json"]      # httpbin devuelve lo que recibió
        print(f"  POST enviado. Status HTTP: {respuesta.status_code}")
        print(f"  El servidor recibió: {recibido}")
        return True
    except requests.exceptions.RequestException as error:
        print(f"  No se pudo enviar el POST: {error}")
        return False
