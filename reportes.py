# reportes.py
# Arma la tabla con Pandas, la analiza, la guarda en Excel y hace un
# gráfico.
# =====================================================================

import pandas as pd
import matplotlib                   #Dibuja graficos
matplotlib.use("Agg")               #dibuja el gráfico en un archivo, sin abrir ventana emergente y pausar el programa
import matplotlib.pyplot as plt


def crear_tabla(resultados):
    """Convierte la lista de diccionarios en un DataFrame de Pandas."""
    return pd.DataFrame(resultados)


def mostrar_resumen(tabla):
    """Muestra el análisis de los resultados con Pandas."""
    # 1. Cuántos libros hay en cada clasificación
    print("\n  Libros por clasificación:")
    conteo = tabla["clasificacion"].value_counts()
    print(conteo.to_string())

    # 2. Variación promedio por categoría (+ caro / - barato)
    print("\n  Variación promedio por categoría (%):")
    promedios = tabla.groupby("categoria")["variacion_pct"].mean()
    promedios = promedios.round(2).dropna().sort_values()
    print(promedios.to_string())


def ranking_oportunidades(tabla):
    """Devuelve solo las oportunidades, de la más barata a la menos barata."""
    oportunidades = tabla[tabla["clasificacion"] == "oportunidad"]
    return oportunidades.sort_values("variacion_pct")


def guardar_excel(tabla, ruta):
    """Guarda un Excel con dos hojas: la comparación completa y el ranking."""
    with pd.ExcelWriter(ruta) as archivo:
        tabla.to_excel(archivo, sheet_name="Comparacion", index=False)
        ranking_oportunidades(tabla).to_excel(archivo, sheet_name="Ranking oportunidades", index=False)
    print(f"  Excel guardado: {ruta}")


def guardar_grafico(tabla, ruta):
    """Gráfico de barras: variación promedio por categoría."""
    con_datos = tabla.dropna(subset=["variacion_pct"])
    por_categoria = con_datos.groupby("categoria")["variacion_pct"].mean().sort_values()

    grafico = por_categoria.plot(kind="barh", title="Nuestro precio vs. competidor (%)")
    grafico.set_xlabel("Variación % (positivo = somos más caros)")
    grafico.axvline(0, color="black", linewidth=0.8)    # línea en el 0
    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()
    print(f"  Gráfico guardado: {ruta}")
