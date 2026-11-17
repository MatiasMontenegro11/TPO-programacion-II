# MÓDULO DE DATOS PROPIOS
# Catálogo con precios,
# costos y stock, y los mails destino.
# ---------------------------------------------------------------------
# CATÁLOGO:
# Lista de libros. Cada libro es un DICCIONARIO con sus datos.
# Títulos escritos cargados manualmente
# (con mayúsculas o espacios de más),
# Los normalizarlos para poder compararlos con los del competidor.
# Precios y costos en pesos argentinos (ARS).
# ---------------------------------------------------------------------
CATALOGO = [
    {"sku": "LIB-001", "titulo": "A Light in the Attic",       "categoria": "Poesía",
     "precio": 95000,  "costo": 60000, "stock": 8},
    {"sku": "LIB-002", "titulo": "SAPIENS: A Brief History of Humankind", "categoria": "Historia",
     "precio": 118000, "costo": 70000, "stock": 0},
    {"sku": "LIB-003", "titulo": "Sharp  Objects",             "categoria": "Misterio",
     "precio": 96500,  "costo": 58000, "stock": 5},
    {"sku": "LIB-004", "titulo": "the requiem red",            "categoria": "Juvenil",
     "precio": 41000,  "costo": 25000, "stock": 12},
    {"sku": "LIB-005", "titulo": "Tipping the Velvet",         "categoria": "Ficción histórica",
     "precio": 115000, "costo": 68000, "stock": 3},
    {"sku": "LIB-006", "titulo": "Shakespeare's Sonnets",      "categoria": "Poesía",
     "precio": 39900,  "costo": 24000, "stock": 10},
    {"sku": "LIB-007", "titulo": "Olio ",                      "categoria": "Poesía",
     "precio": 47500,  "costo": 29000, "stock": 0},
    {"sku": "LIB-008", "titulo": "Rip it Up and Start Again",  "categoria": "Música",
     "precio": 78000,  "costo": 45000, "stock": 4},
    {"sku": "LIB-009", "titulo": "It's Only the Himalayas",    "categoria": "Viajes",
     "precio": 84000,  "costo": 52000, "stock": 6},
    {"sku": "LIB-010", "titulo": "Libertarianism for Beginners", "categoria": "Política",
     "precio": 99000,  "costo": 61000, "stock": 2},
    {"sku": "LIB-011", "titulo": "Rayuela",                    "categoria": "Novela",
     "precio": 32000,  "costo": 18000, "stock": 15},
]

# ---------------------------------------------------------------------
# DESTINATARIOS DEL REPORTE

DESTINATARIOS = [
    "ayerivass@gmail.com",
]

# ---------------------------------------------------------------------
# FUNCIONES PARA CONSULTAR NUESTROS DATOS

def obtener_catalogo():
    return CATALOGO


def libros_sin_stock():
    sin_stock = []
    for libro in CATALOGO:
        if libro["stock"] == 0:
            sin_stock.append(libro["titulo"].strip())
    return sin_stock


def stock_total():
    total = 0
    for libro in CATALOGO:
        total = total + libro["stock"]
    return total
