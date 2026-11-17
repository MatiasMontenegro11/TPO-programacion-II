# Margen para considerar dos precios "igualados": más o menos 2 %

UMBRAL_IGUALADO = 2.0       # Si la diferencia está entre -2 % y +2 % se considera igualado

# Normalizo titulos

def normalizar_titulo(titulo):
    titulo = titulo.strip()              # saca espacios al principio y al final
    titulo = titulo.lower()              # pasa todo a minúsculas
    titulo = " ".join(titulo.split())    # saca los espacios dobles del medio
    return titulo

# cálculos de precios

def convertir_a_pesos(precio_libras, tasa_libra):
    return round(precio_libras * tasa_libra, 2)

def calcular_variacion(precio_propio, precio_competidor):
    return round((precio_propio - precio_competidor) / precio_competidor * 100, 2)

def calcular_margen(precio, costo): #calcula margen de ganancia
    return round((precio - costo) / precio * 100, 2)

# clasificar y recomendar

def clasificar(variacion):
    #Clasifica el producto según cuánto más caro o barato es.
    if variacion is None:
        return "sin datos"
    elif variacion < -UMBRAL_IGUALADO:          #Umbral igualado = 2%
        return "oportunidad"
    elif variacion <= UMBRAL_IGUALADO:
        return "igualado"
    else:
        return "caro"

def recomendar(clasificacion, stock):

    sin_stock = stock == 0

    if clasificacion == "caro" and sin_stock:
        return "URGENTE: reponer y revisar precio"
    elif clasificacion == "sin datos":
        return "El competidor no lo vende"
    elif sin_stock:
        return "Reponer stock"
    elif clasificacion == "caro":
        return "Revisar precio"
    elif clasificacion == "oportunidad":
        return "Destacar en promoción"
    else:
        return "Mantener precio"

# Cruza nuestro catálogo con los precios del competidor.

def comparar_catalogo(catalogo, precios_competidor, tasa_libra):
    """
    Recorre nuestro catálogo y, para cada libro, busca el precio del
    competidor, lo pasa a pesos, calcula la variación y lo clasifica.

    Devuelve una lista de diccionarios, uno por libro, con el resultado.
    """
    resultados = []

    for libro in catalogo:
        clave = normalizar_titulo(libro["titulo"])

        # ¿El competidor vende este libro?
        if clave in precios_competidor:
            dato = precios_competidor[clave]
            precio_comp_pesos = convertir_a_pesos(dato["precio_libras"], tasa_libra)
            variacion = calcular_variacion(libro["precio"], precio_comp_pesos)
        else:
            precio_comp_pesos = None
            variacion = None

        clasificacion = clasificar(variacion)

        resultados.append({
            "sku": libro["sku"],
            "titulo": " ".join(libro["titulo"].split()),   # sin espacios de más
            "precio_propio": libro["precio"],
            "precio_competidor": precio_comp_pesos,
            "variacion_pct": variacion,
            "margen_pct": calcular_margen(libro["precio"], libro["costo"]),
            "stock": libro["stock"],
            "clasificacion": clasificacion,
            "recomendacion": recomendar(clasificacion, libro["stock"]),
        })

    return resultados
