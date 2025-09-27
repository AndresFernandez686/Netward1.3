
# Entrada de la app, orquesta de los modulos y las vistas
import streamlit as st
import os
from datetime import date

# Aplicar CSS personalizado
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), '.streamlit', 'style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning("No se encontró el archivo CSS personalizado.")

# Cargar HTML personalizado
def load_html(html_file):
    html_path = os.path.join(os.path.dirname(__file__), '.streamlit', html_file)
    if os.path.exists(html_path):
        with open(html_path) as f:
            return f.read()
    else:
        st.warning(f"No se encontró el archivo HTML: {html_file}")
        return ""

from persistencia import (
    cargar_inventario, guardar_inventario, guardar_historial,
    cargar_historial, cargar_catalogo_delivery, guardar_catalogo_delivery,
    guardar_venta_delivery, cargar_ventas_delivery
)
from auth import login, logout  # Importar también la función logout
from ui_empleado import empleado_inventario_ui, empleado_delivery_ui
from ui_admin import admin_inventario_ui, admin_historial_ui, admin_delivery_ui

# Datos base (corregidos y actualizados)
productos_por_categoria = {
    "Impulsivo": {
        "Caja almendrado": 0,
        "Unidad Almendrado": 0,
        "Caja Bombon Crocante": 0,
        "Unidad Bombon Crocante": 0,
        "Caja Bombon Escoces": 0,
        "Unidad Bombon Escoces": 0,
        "Caja de bombon Suizo": 0,
        "Unidad bombon Suizo": 0,
        "Caja Bombon Cookies and Crema": 0,
        "Unidad Bombon Cookies and Crema": 0,
        "Caja Bombon Vainilla": 0,
        "Unidad Bombon Vainilla": 0,
        "Caja Casatta": 0,
        "Unidad Casatta": 0,
        "Crocantino": 0,
        "Delicia": 0,
        "Pizza": 0,
        "Familiar 1": 0,
        "Familiar 2": 0,
        "Familiar 3": 0,
        "Familiar 4": 0,
        "Caja palito Bombon": 0,
        "Unidad Palito Bombon": 0,
        "Caja Palito Crema Americana": 0,
        "Unidad Palito Crema Americana": 0,
        "Caja Palito Crema Frutilla": 0,
        "Unidad Palito Crema Frutilla": 0,
        "Caja Palito Frutal Frutilla": 0,
        "Unidad Palito Frutal Frutilla": 0,
        "Caja Palito Frutal Limon": 0,
        "Unidad Palito Frutal Limon": 0,
        "Caja Palito Frutal Naranja": 0,
        "Unidad Palito Frutal Naranja": 0,
        "Tentacion Chocolate": 0,
        "Tentacion Chocolate con Almendra": 0,
        "Tentacion Cookies": 0,
        "Tentacion Crema Americana": 0,
        "Tentacion Dulce de Leche Granizado": 0,
        "Tentacion Dulce de Leche": 0,
        "Tentacion Frutilla": 0,
        "Tentacion Granizado": 0,
        "Tentacion Menta Granizada": 0,
        "Tentacion Mascarpone": 0,
        "Tentacion Vainilla": 0,
        "Tentacion Limon": 0,
        "Tentacion Toddy": 0,
        "Yogurt Helado Frutilla sin Tacc": 0,
        "Yogurt Helado Mango Maracuya": 0,
        "Yogurt Helado Frutos del Bosque sin Tacc": 0,
        "Helado sin Azucar Frutilla a la Crema": 0,
        "Helado sin Azucar Durazno a la Crema": 0,
        "Helado sin Azucar chocolate sin Tacc": 0,
        "Torta con Oreo": 0,
        "Torta Grido Rellena": 0,
        "Torta Milka": 0
    },
    "Por Kilos": {
        "Vainilla": 0.0,
        "Chocolate": 0.0,
        "Fresa": 0.0,
        "Anana a la crema": 0.0,
        "Banana con Dulce de leche": 0.0,
        "Capuccino Granizado": 0.0,
        "Cereza": 0.0,
        "Chocolate Blanco": 0.0,
        "Chocolate con Almendra": 0.0,
        "Chocolate Dark": 0.0,
        "Chocolate Mani Crunch": 0.0,
        "Chocolate Suizo": 0.0,
        "Crema Americana": 0.0,
        "Crema Cookie": 0.0,
        "Crema Rusa": 0.0,
        "Dulce de Leche": 0.0,
        "Dulce de Leche con Brownie": 0.0,
        "Dulce de Leche con Nuez": 0.0,
        "Dulce de Leche Especial": 0.0,
        "Dulce de Leche Granizado": 0.0,
        "Durazno a la Crema": 0.0,
        "Flan": 0.0,
        "Frutos Rojos al Agua": 0.0,
        "Granizado": 0.0,
        "Kinotos al Whisky": 0.0,
        "Limon al Agua": 0.0,
        "Maracuya": 0.0,
        "Marroc Grido": 0.0,
        "Mascarpone con Frutos del Bosque": 0.0,
        "Menta Granizada": 0.0,
        "Naranja Helado al Agua": 0.0,
        "Pistacho": 0.0,
        "Super Gridito": 0.0,
        "Tiramisu": 0.0,
        "Tramontana": 0.0,
        "Candy": 0.0
    },
    "Extras": {
        "Cinta Grido": 0,
        "Cobertura Chocolate": 0,
        "Bolsa 40x50": 0,
        "Cobertura Frutilla": 0,
        "Cobertura Dulce de Leche": 0,
        "Leche": 0,
        "Cuchara Sunday": 0,
        "Cucharita Grido": 0,
        "Cucurucho Biscoito Dulce x300": 0,
        "Cucurucho Cascao x120": 0,
        "Cucurucho Nacional x54": 0,
        "Garrafita de Gas": 0,
        "Isopor 1 kilo": 0,
        "Isopor 1/2 kilo": 0,
        "Isopor 1/4": 0,
        "Mani tostado": 0,
        "Pajita con Funda": 0,
        "Servilleta Grido": 0,
        "Tapa Burbuja Capuccino": 0,
        "Tapa Burbuja Batido": 0,
        "Vaso capuccino": 0,
        "Vaso Batido": 0,
        "Vasito de una Bocha": 0,
        "Vaso Termico 240gr": 0,
        "Vaso Sundae": 0,
        "Rollo Termico": 0
    }
}

# Opciones de valde como texto literal
opciones_valde = {
    "Vacío": "Vacío",
    "Casi lleno": "Casi lleno",
    "Medio lleno": "Medio lleno",
    "Valde lleno": "Valde lleno"
}

def main():
    st.set_page_config(page_title="Heladería - Inventario y Delivery", page_icon="🍦", layout="wide")
    
    # Cargar CSS personalizado
    load_css()
    
    # Inicializar el estado de la sesión
    if "usuario" not in st.session_state:
        st.session_state.usuario = None
        st.session_state.rol = None
    
    # Botón de cierre de sesión
    if st.session_state.usuario:
        if st.sidebar.button("Cerrar sesión"):
            # Actualizar las variables en auth.py
            logout()
            
            # Actualizar también las variables locales
            st.session_state.usuario = None
            st.session_state.rol = None
            
            st.rerun()  # Recargar la página para mostrar el login
    
    # Si no hay usuario en la sesión, mostrar login
    if not st.session_state.usuario:
        usuario, rol = login()
        if usuario and rol:
            st.session_state.usuario = usuario
            st.session_state.rol = rol
            st.rerun()  # Reiniciar la app para cargar con el usuario logueado
        return  # Salir si no hay usuario autenticado

    # A partir de aquí, el usuario está autenticado
    st.sidebar.success(f"Usuario: {st.session_state.usuario} ({st.session_state.rol})")
    
    # Mostrar el encabezado HTML personalizado
    header_html = load_html('header.html')
    if header_html:
        st.markdown(header_html, unsafe_allow_html=True)
    
    inventario = cargar_inventario(productos_por_categoria)

    if st.session_state.rol == 'empleado':
        tab_inv, tab_deliv = st.tabs(["🧊 Inventario", "🚚 Delivery"])
        with tab_inv:
            empleado_inventario_ui(
                inventario, st.session_state.usuario, opciones_valde,
                guardar_inventario, guardar_historial
            )
        with tab_deliv:
            empleado_delivery_ui(
                st.session_state.usuario, cargar_catalogo_delivery, guardar_venta_delivery, cargar_ventas_delivery
            )

    elif st.session_state.rol == 'administrador':
        tab_inv, tab_hist, tab_deliv = st.tabs(["📦 Inventario", "📅 Historial", "🛠️ Delivery"])
        with tab_inv:
            # Mostrar dashboard HTML para el administrador
            dashboard_html = load_html('dashboard.html')
            if dashboard_html:
                st.markdown(dashboard_html, unsafe_allow_html=True)
                
            admin_inventario_ui(inventario)
        with tab_hist:
            admin_historial_ui(cargar_historial())
        with tab_deliv:
            # Mostrar formulario personalizado para delivery
            forms_html = load_html('forms.html')
            if forms_html:
                st.markdown(forms_html, unsafe_allow_html=True)
                
            admin_delivery_ui(
                cargar_catalogo_delivery, guardar_catalogo_delivery, cargar_ventas_delivery
            )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Se ha producido un error: {str(e)}")
        if st.button("Reintentar"):
            st.rerun()
