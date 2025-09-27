# UI y lógica de empleados (Inventario, delivery)
import streamlit as st
from datetime import date
from utils import df_to_csv_bytes

def empleado_inventario_ui(inventario, usuario, opciones_valde, guardar_inventario, guardar_historial):
    st.header("Inventario")
    fecha_carga = st.date_input("Selecciona la fecha de carga", value=date.today(), key="fecha_inv")

    # Inicializar productos cargados en session_state si no existe
    if "productos_cargados" not in st.session_state:
        st.session_state.productos_cargados = {}

    tabs = st.tabs(list(inventario.keys()))
    for i, categoria in enumerate(inventario.keys()):
        with tabs[i]:
            productos = inventario[categoria]
            producto_seleccionado = st.selectbox(
                f"Producto de {categoria}",
                list(productos.keys()),
                key=f"sel_{categoria}"
            )

            # Ya no necesitamos la opción de añadir/reemplazar, siempre será modificar
            
            if categoria == "Por Kilos":
                st.markdown("### Selecciona la cantidad de baldes a registrar:")
                num_baldes = st.number_input(
                    "Cantidad de baldes",
                    min_value=1,
                    max_value=10,  # Cambiado de 6 a 10
                    value=1,       # Cambiado de 6 a 1 para que comience con el mínimo
                    step=1,
                    key=f"num_baldes_{producto_seleccionado}_{fecha_carga}_{usuario}"
                )
                st.markdown(f"### Estado de hasta {num_baldes} baldes:")

                estados_baldes = []
                for n in range(1, num_baldes + 1):
                    key_balde = f"{producto_seleccionado}_balde_{n}_{fecha_carga}_{usuario}"
                    # Inicializa el valor solo si no existe
                    if key_balde not in st.session_state:
                        valor_guardado = None
                        if isinstance(productos[producto_seleccionado], list) and len(productos[producto_seleccionado]) >= n:
                            valor_guardado = productos[producto_seleccionado][n-1]
                        st.session_state[key_balde] = valor_guardado if valor_guardado is not None else "Vacío"
                    opcion = st.selectbox(
                        f"Balde {n}",
                        list(opciones_valde.keys()),
                        index=list(opciones_valde.keys()).index(st.session_state[key_balde]) if st.session_state[key_balde] in opciones_valde else 0,
                        key=key_balde
                    )
                    estados_baldes.append(opcion)

                if st.button(
                    f"Actualizar {producto_seleccionado} ({categoria})",
                    key=f"btn_{categoria}_{producto_seleccionado}"
                ):
                    # Solo guarda los baldes seleccionados
                    productos[producto_seleccionado] = estados_baldes.copy()
                    guardar_inventario(inventario)
                    guardar_historial(
                        fecha_carga, usuario, categoria, producto_seleccionado, estados_baldes, "Modificar"
                    )
                    
                    # Registrar en productos cargados
                    if categoria not in st.session_state.productos_cargados:
                        st.session_state.productos_cargados[categoria] = {}
                    st.session_state.productos_cargados[categoria][producto_seleccionado] = estados_baldes.copy()
                    
                    st.success(f"Actualizado. Estado actual: {', '.join(estados_baldes)}")

            else:
                # Mostrar la cantidad actual del inventario en lugar de empezar en 0
                valor_inicial = productos[producto_seleccionado]
                cantidad = st.number_input(
                    "Cantidad (unidades)", 
                    min_value=0, 
                    value=valor_inicial,  # Usar el valor actual del inventario
                    step=1, 
                    key=f"cant_{categoria}_{producto_seleccionado}"
                )
                
                if st.button(
                    f"Actualizar {producto_seleccionado} ({categoria})",
                    key=f"btn_{categoria}_{producto_seleccionado}"
                ):
                    cantidad = max(0, int(cantidad))
                    productos[producto_seleccionado] = cantidad  # Siempre reemplazar con el nuevo valor
                    guardar_inventario(inventario)
                    guardar_historial(
                        fecha_carga, usuario, categoria, producto_seleccionado, cantidad, "Modificar"
                    )
                    
                    # Registrar en productos cargados
                    if categoria not in st.session_state.productos_cargados:
                        st.session_state.productos_cargados[categoria] = {}
                    st.session_state.productos_cargados[categoria][producto_seleccionado] = cantidad
                    
                    st.success(f"Actualizado. Nuevo stock: {cantidad}")

    # Mostrar solo los productos que ha cargado el empleado en la sesión actual
    st.subheader("Productos que has cargado:")
    if not st.session_state.productos_cargados:
        st.write("Aún no has cargado ningún producto.")
    else:
        for categoria, productos_cat in st.session_state.productos_cargados.items():
            for producto, cantidad in productos_cat.items():
                if isinstance(cantidad, list):  # Para productos por kilos
                    baldes_no_vacios = [x for x in cantidad if x != "Vacío"]
                    baldes_vacios = [x for x in cantidad if x == "Vacío"]
                    if baldes_no_vacios or baldes_vacios:
                        st.write(f"• {producto}: {', '.join(baldes_no_vacios + baldes_vacios)}")
                else:  # Para productos con cantidad numérica
                    st.write(f"• {producto}: {cantidad if cantidad > 0 else 'Vacío'}")

def empleado_delivery_ui(usuario, cargar_catalogo_delivery, guardar_venta_delivery, cargar_ventas_delivery):
    st.header("Delivery")
    catalogo = cargar_catalogo_delivery()
    activos = [item for item in catalogo if item.get("activo", True)]

    if not activos:
        st.info("No hay productos de delivery activos. Pide al administrador que agregue opciones.")
        return

    fecha_venta = st.date_input("Fecha de la venta", value=date.today(), key="fecha_deliv")
    opciones = [f"{it['nombre']} {'(PROMO)' if it.get('es_promocion', False) else ''}" for it in activos]
    seleccion = st.selectbox("Producto de delivery", opciones)
    idx = opciones.index(seleccion)
    item_sel = activos[idx]
    cantidad = st.number_input("Cantidad vendida", min_value=1, step=1)

    if st.button("Registrar venta de delivery"):
        guardar_venta_delivery(
            fecha_venta,
            usuario,
            item_sel["nombre"],
            cantidad,
            item_sel.get("es_promocion", False)
        )
        st.success("Venta registrada con éxito ✅")

    ventas = cargar_ventas_delivery()
    if not ventas.empty:
        ventas_hoy = ventas[(ventas["Usuario"] == usuario) & (ventas["Fecha"].dt.date == date.today())]
        if not ventas_hoy.empty:
            st.subheader("Tus ventas de delivery hoy")
            st.dataframe(ventas_hoy)
