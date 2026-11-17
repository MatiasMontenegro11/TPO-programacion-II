# MÓDULO DE DATOS DE TERCEROS
# Todo lo que viene de afuera de la empresa:
#   1. Precios del competidor con web scraping (books.toscrape.com)
#   2. Cotización de la libra con una API 
#   3. Envío del resumen con POST

import requests                     # para pedir páginas y APIs por internet (GET y POST)
from bs4 import BeautifulSoup       # para leer el HTML y buscar los datos


URL_COMPETIDOR = "http://books.toscrape.com/"

# API pública de tipo de cambio sin API KEY

URL_API_CAMBIO = "https://open.er-api.com/v6/latest/GBP"

# Servicio de prueba que recibe datos por POST y los devuelve

URL_POST = "https://httpbin.org/post"

# Headers

HEADERS = {
    "User-Agent": "LibreriaInteligenciaRetail (proyecto academico UADE)"
}

TIMEOUT = 10           # segundos máximos de espera por respuesta

# 1. WEB SCRAPING: precios del competidor

def scrapear_competidor(cantidad_paginas=1):
    from funciones import normalizar_titulo

    libros = {}

    for numero in range(1, cantidad_paginas + 1):
        if numero == 1:
            url = URL_COMPETIDOR
        else:
            url = URL_COMPETIDOR + f"catalogue/page-{numero}.html"
        print(f"  Descargando {url} ...")
        try:
            respuesta = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            respuesta.raise_for_status()   
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

# 2. API PÚBLICA: cotización de la libra (GET)

def obtener_tasa_libra():
    respuesta = requests.get(URL_API_CAMBIO, headers=HEADERS, timeout=TIMEOUT)
    respuesta.raise_for_status()
    datos = respuesta.json()             
    tasa = datos["rates"]["ARS"]
    print(f"  Status HTTP: {respuesta.status_code}")
    return tasa

# 3. POST: enviar el resumen del análisis

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
