import os
import json
from datetime import date

INVENTARIO_FILE = "inventario.json"
HISTORIAL_FILE = "historial_inventario.json"
CATALOGO_DELIVERY_FILE = "catalogo_delivery.json"
VENTAS_DELIVERY_FILE = "ventas_delivery.json"

def cargar_inventario(productos_por_categoria):
    if os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return productos_por_categoria.copy()

def guardar_inventario(inventario):
    with open(INVENTARIO_FILE, "w", encoding="utf-8") as f:
        json.dump(inventario, f, ensure_ascii=False, indent=2)

def guardar_historial(fecha, usuario, categoria, producto, cantidad, modo):
    """Guarda un registro detallado del movimiento de inventario."""
    registro = {
        "fecha": str(fecha),
        "usuario": usuario,
        "categoria": categoria,
        "producto": producto,
        "cantidad": cantidad,
        "modo": modo
    }
    historial = []
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            historial = json.load(f)
    historial.append(registro)
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

def cargar_historial():
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def cargar_catalogo_delivery():
    if os.path.exists(CATALOGO_DELIVERY_FILE):
        with open(CATALOGO_DELIVERY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_catalogo_delivery(catalogo):
    with open(CATALOGO_DELIVERY_FILE, "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=2)

def guardar_venta_delivery(usuario, venta):
    hoy = str(date.today())
    registro = {
        "fecha": hoy,
        "usuario": usuario,
        "venta": venta
    }
    ventas = []
    if os.path.exists(VENTAS_DELIVERY_FILE):
        with open(VENTAS_DELIVERY_FILE, "r", encoding="utf-8") as f:
            ventas = json.load(f)
    ventas.append(registro)
    with open(VENTAS_DELIVERY_FILE, "w", encoding="utf-8") as f:
        json.dump(ventas, f, ensure_ascii=False, indent=2)

def cargar_ventas_delivery():
    if os.path.exists(VENTAS_DELIVERY_FILE):
        with open(VENTAS_DELIVERY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
