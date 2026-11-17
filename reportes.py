# Arma la tabla con Pandas, la analiza, la guarda en Excel y hace el
# gráfico de precios por libro.

import pandas as pd
import matplotlib                   #Dibuja graficos
matplotlib.use("Agg")               #dibuja el gráfico en un archivo, sin abrir ventana emergente y pausar el programa
import matplotlib.pyplot as plt

def crear_tabla(resultados):
   #Convierte la lista de diccionarios en un DataFrame de Pandas."""
    return pd.DataFrame(resultados)

def mostrar_resumen(tabla):
    """Muestra el análisis de los resultados con Pandas."""
    # Cuántos libros hay en cada clasificación
    print("\n  Libros por clasificación:")
    conteo = tabla["clasificacion"].value_counts()
    print(conteo.to_string())

def ranking_oportunidades(tabla):
    """Devuelve solo las oportunidades, de la más barata a la menos barata."""
    oportunidades = tabla[tabla["clasificacion"] == "oportunidad"]
    return oportunidades.sort_values("variacion_pct")

# Nombres de las columnas para que el Excel se entienda
NOMBRES_EXCEL = {
    "sku": "SKU",
    "titulo": "Título",
    "precio_propio": "Nuestro precio ($)",
    "precio_competidor": "Precio competidor ($)",
    "variacion_pct": "Variación vs. competidor (%)",
    "margen_pct": "Margen de ganancia (%)",
    "stock": "Stock",
    "clasificacion": "Clasificación",
    "recomendacion": "Qué hacer",
}

def guardar_excel(tabla, ruta):
    """Guarda un Excel con dos hojas: la comparación completa y el ranking."""
    with pd.ExcelWriter(ruta, engine="openpyxl") as archivo:
        tabla.rename(columns=NOMBRES_EXCEL).to_excel(archivo, sheet_name="Comparacion", index=False)
        ranking_oportunidades(tabla).rename(columns=NOMBRES_EXCEL).to_excel(archivo, sheet_name="Ranking oportunidades", index=False)

        # Columnas más anchas para que se lean los títulos y los textos completos
        for hoja in archivo.sheets.values():
            for letra in "ACDEFGH":
                hoja.column_dimensions[letra].width = 28
            hoja.column_dimensions["B"].width = 40      # título del libro: más ancha
            hoja.column_dimensions["I"].width = 35      # qué hacer: más ancha
    print(f"  Excel guardado: {ruta}")

def guardar_grafico(tabla, ruta):
    """Gráfico de barras: nuestro precio y el del competidor, libro por libro."""
    # Pasamos las columnas de la tabla a listas comunes de Python
    skus = tabla["sku"].tolist()
    nuestros = tabla["precio_propio"].tolist()
    competidor = tabla["precio_competidor"].fillna(0).tolist()   # si no hay dato queda en 0

    # Posición de cada barra: la nuestra un poco a la izquierda y la del competidor a la derecha
    lugar_nuestro = []
    lugar_competidor = []
    for i in range(len(skus)):
        lugar_nuestro.append(i - 0.2)
        lugar_competidor.append(i + 0.2)

    plt.figure(figsize=(14, 6))     # crea la imagen del gráfico: 14 de ancho por 6 de alto (pulgadas)
    plt.bar(lugar_nuestro, nuestros, width=0.4, label="Nuestro precio", color="royalblue")
    plt.bar(lugar_competidor, competidor, width=0.4, label="Competidor", color="orange")
    plt.xticks(range(len(skus)), skus)          # abajo de cada par de barras va el SKU
    plt.ylabel("Precio ($)")                    # nombre del eje vertical
    plt.title("Nuestro precio vs. competidor por libro")
    plt.legend()                                # cuadro que explica qué color es cada barra

    plt.tight_layout()                          # acomoda los márgenes para que no se corte nada
    plt.savefig(ruta)                           # guarda el gráfico como imagen .png en la carpeta salidas
    plt.close()                                 # cierra el gráfico para liberar memoria
    print(f"  Gráfico guardado: {ruta}")        # avisa en la consola dónde se guardó