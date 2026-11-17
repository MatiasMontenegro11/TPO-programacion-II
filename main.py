# Inteligencia Retail: precios para una librería

# Librería argentina que vende libros importados. Este programa
# compara nuestros precios con los de una librería online 
# (books.toscrape.com) y le avisa al equipo de Compras qué hacer.

# books.toscrape.com: imita una librería online de 1.000 libros, 50 páginas, cada uno con título, 
# precio en £ libras, estrellas, stock y categoría.

# Para pasar libras a pesos y comparar los precios usamos la api (ExchangeRate-API)

#ExchangeRate-API: no pide API key, es API abierta

#El programa extrae los 20 libros de la primera página
# De cada libro extrae: título, precio y si está en stock, 
# buscando esas etiquetas en el HTML con la libreria BeautifulSoup.

# Tambien extrae nuestro catalogo cargados en el modulo datos_propios: tiene 11 libros, 10 coinciden 
# con la pagina web y 1 ("Rayuela") no, Algunos los escribimos con mayúsculas o espacios distintos para 
# simular errores de carga, y por eso normalizamos los títulos antes de cruzarlos con la funcion 
# normalizar_titulo() en funciones.py.

# Proceso ETL:
# 1. EXTRAER: nuestro catálogo + precios del competidor + cotización
# 2. TRANSFORMAR: pasar a pesos, comparar, clasificar y recomendar
# 3. CARGAR: tabla con Pandas, Excel, gráfico, POST y mail

import os                       # Modulo que permite al programa con archivos, carpetas, sistema operativo
import datetime                 # Permite trabajar con fechas, horas
from dotenv import load_dotenv  # Lee las variables definidas en el archivo .env y las carga en el entorno
                                
# Nuestros módulos (los otros archivos .py de esta carpeta)
import datos_propios                # Catalogo y destinatarios del reporte
import apis_terceros                
import funciones                    # Funciones principales del negocio
import reportes                     # Analisis con pandas
import correo                       # Envia analisis a destinatarios por gmail

# ---------------------------------------------------------------------
# CONFIGURACIÓN

CARPETA = os.path.dirname(os.path.abspath(__file__))
CARPETA_SALIDAS = os.path.join(CARPETA, "salidas")

# Cargamos las claves desde el archivo .env (así no quedan escritas en el código)

load_dotenv(os.path.join(CARPETA, ".env"))
GMAIL_USUARIO = os.getenv("GMAIL_USUARIO")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD_APP")

def titulo(texto):                         #función que imprime un título entre dos líneas de = para separar las partes del programa     
    print("\n" + "=" * 70)                 #"\n": deja un renglon vacio
    print("  " + texto)
    print("=" * 70)


def mostrar_comparacion(resultados):        #Imprime la comparación libro por libro.
    for fila in resultados:
        if fila["precio_competidor"] is None:
            print("  ", fila["titulo"], "| nuestro: $", fila["precio_propio"],
                  "| competidor: sin datos")
        else:
            print("  ", fila["titulo"], "| nuestro: $", fila["precio_propio"],
                  "| competidor: $", round(fila["precio_competidor"]),
                  "| variación:", fila["variacion_pct"], "% |", fila["clasificacion"])  #variacion_pct

# Funcion principal: pusimos el programa dentro de una funcion main() para usar return y frenar si algo falla

def main():

    titulo("INTELIGENCIA DE PRECIOS - LIBRERÍA")
    fecha_hoy = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")  #strftime es para dar formato texto a una fecha
    print("  Fecha:", fecha_hoy)

    # =================================================================
    # 1. EXTRAER

    titulo("1. EXTRAER DATOS")

    print("\n[Datos propios]")
    catalogo = datos_propios.obtener_catalogo()                         #traemos del modulo datos_propios la funcion obtner_catalogo
    print(f"  Libros en nuestro catálogo: {len(catalogo)}")
    print(f"  Unidades en stock: {datos_propios.stock_total()}")
    print(f"  Sin stock: {datos_propios.libros_sin_stock()}")           

    print("\n[Sitio del competidor]")
    print("  Sitio:", apis_terceros.URL_COMPETIDOR)
    if not apis_terceros.puede_scrapear(apis_terceros.URL_COMPETIDOR):      #Llama a la funcion puede_scrapear que lee el robots.txt para ver si nos permite scrapear
        print("  El robots.txt no permite entrar. Fin del programa.")       # Si no nos permite, termina el programa
        return
    print("  robots.txt: permitido")

    print("\n[Web scraping]")                                                       #Bloque de scrappeo
    precios_competidor = apis_terceros.scrapear_competidor(cantidad_paginas=1)      
    print(f"  Libros encontrados en el competidor: {len(precios_competidor)}")
    if len(precios_competidor) == 0:
        print("  No se pudieron obtener precios del competidor. Fin del programa.")
        return

    print("\n[API de tipo de cambio]")                      #Bloque API: averigua cuantos pesos vale una libra
    tasa = apis_terceros.obtener_tasa_libra()               #Obtener_tasa_libra pide la cotizacion y la guarda en la variabale: tasa
    if tasa is None:
        print("  Sin cotización no se puede comparar. Fin del programa.")
        return
    print("  1 libra = $", round(tasa, 2))

    # =================================================================
    # 2. TRANSFORMAR
    #En este paso tomamos los datos crudos extraidos para convertirlos en informacion

    titulo("2. COMPARAR Y CLASIFICAR")
    resultados = funciones.comparar_catalogo(catalogo, precios_competidor, tasa)    #La funcion comparar_catalgo recibe los datos extraidos antes y los guarda en la lista resultados
    mostrar_comparacion(resultados) 

    print("\n  ALERTAS (libros sin stock):")
    cantidad_alertas = 0
    for fila in resultados:
        if fila["stock"] == 0:
            print("  ⚠", fila["titulo"], "-", fila["recomendacion"])       #Recomendacion sale de la funcion llamada antes comparar_catalogo
            cantidad_alertas = cantidad_alertas + 1
    if cantidad_alertas == 0:
        print("  No hay alertas.")

    # =================================================================
    # 3. CARGAR

    titulo("3. REPORTE")
    tabla = reportes.crear_tabla(resultados)    #crear_tabla es una funcion que convierte el diccionario de resultados en un DataFrame de Pandas
    reportes.mostrar_resumen(tabla)             #mostrar_resumen analiza los resultados con pandas

    os.makedirs(CARPETA_SALIDAS, exist_ok=True)             #( os.makedirs) Crea la carpeta_salidas si ya existe no hace nada (exist_ok=True)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    ruta_excel = os.path.join(CARPETA_SALIDAS, f"reporte_precios_{fecha}.xlsx")         #Variable que anota la direccion del archivo
    ruta_grafico = os.path.join(CARPETA_SALIDAS, f"grafico_categorias_{fecha}.png")     

    print()
    reportes.guardar_excel(tabla, ruta_excel)       #Guarda el excel en la direccion escrita antes
    ruta_json = os.path.join(CARPETA_SALIDAS, f"reporte_precios_{fecha}.json")
    tabla.to_json(ruta_json, orient="records", force_ascii=False, indent=2)
    print(f"  JSON guardado: {ruta_json}")
    reportes.guardar_grafico(tabla, ruta_grafico)

    conteo = tabla["clasificacion"].value_counts()      #Value.counts es una funcion de pandas que cuanta cuantas veces aparece cada clasificacion 

    # Resumen en forma de diccionario (para el POST y para el mail), el POST envia al servidor prueba httpbin
    resumen = {
        "fecha": fecha,
        "tasa_libra": tasa,
        "total_libros": len(tabla),
        "oportunidades": int(conteo.get("oportunidad", 0)),     #Somos mas baratos
        "igualados": int(conteo.get("igualado", 0)),            #Mismo precio
        "caros": int(conteo.get("caro", 0)),                    #Somos mas caros
        "sin_datos": int(conteo.get("sin datos", 0)),           #Cuantos libros no tiene el competidor
    }

    print("\n[POST]")
    apis_terceros.enviar_resumen_post(resumen)

    print("\n[Mail]")
    if GMAIL_USUARIO and GMAIL_PASSWORD:
        cuerpo = (
            f"Hola equipo de Compras,\n\n"
            f"Resultado de la comparación de precios del {fecha}:\n"
            f"- Libros analizados: {resumen['total_libros']}\n"
            f"- Oportunidades: {resumen['oportunidades']}\n"
            f"- Igualados: {resumen['igualados']}\n"
            f"- Más caros que el competidor: {resumen['caros']}\n"
            f"- Sin datos del competidor: {resumen['sin_datos']}\n\n"
            f"Cotización usada: 1 libra = $ {round(tasa, 2)}\n\n"
            f"Se adjunta el Excel con el detalle y el ranking de oportunidades, "
            f"y el gráfico por categoría.\n"
        )
        correo.enviar_reporte(GMAIL_USUARIO, GMAIL_PASSWORD, datos_propios.DESTINATARIOS,
                              f"Reporte de precios - {fecha}", cuerpo,
                              [ruta_excel, ruta_grafico])
    else:
        print("  No se envía el mail: faltan GMAIL_USUARIO o GMAIL_PASSWORD_APP en el .env")

    titulo("FIN")


#Llamo a la funcion main

if __name__ == "__main__":
    main()