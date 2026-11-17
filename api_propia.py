# Ejecuta main.py y publica el reporte JSON que genera.
#   python -m uvicorn api_propia:app --reload
import glob
import json
import os

from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader

import main

CARPETA_SALIDAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salidas")
API_KEYS_VALIDAS = ["clave_secreta_123", "mi_otra_clave_456", "clave_admin_789"]

encabezado = APIKeyHeader(name="X-API-Key", auto_error=False)


def verificar_api_key(clave: str = Security(encabezado)):
    if clave not in API_KEYS_VALIDAS:
        raise HTTPException(status_code=401, detail="API Key inválida o faltante")


app = FastAPI(title="API propia del reporte", dependencies=[Depends(verificar_api_key)])


def cargar_reporte():
    archivos = glob.glob(os.path.join(CARPETA_SALIDAS, "reporte_precios_*.json"))
    if not archivos:
        raise HTTPException(status_code=404, detail="No hay reporte. Usá POST /generar")
    with open(max(archivos, key=os.path.getmtime), encoding="utf-8") as f:
        return json.load(f)


@app.post("/generar")
def generar():
    main.main()
    return cargar_reporte()


@app.get("/reporte")
def ver_reporte():
    return cargar_reporte()


@app.get("/reporte/{sku}")
def ver_libro(sku: str):
    for fila in cargar_reporte():
        if fila["sku"].lower() == sku.lower():
            return fila
    raise HTTPException(status_code=404, detail=f"No existe el SKU {sku}")