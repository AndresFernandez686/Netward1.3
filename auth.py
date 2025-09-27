# Lógica y datos de usuarios
import streamlit as st

usuarios = {
    'empleado1': 'empleado',
    'empleado2': 'empleado',
    'empleado3': 'empleado',
    'admin1': 'administrador'
}

def login():
    # Inicializar variables de sesión si no existen
    if 'usuario_autenticado' not in st.session_state:
        st.session_state.usuario_autenticado = None
        st.session_state.rol_usuario = None
    
    # Si el usuario ya está autenticado, retornar la información de sesión
    if st.session_state.usuario_autenticado:
        return st.session_state.usuario_autenticado, st.session_state.rol_usuario
    
    # Usar columnas para centrar el formulario
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("Netward")
        st.subheader("Inicio de sesión")
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        login_button = st.button("Ingresar")
        
        if login_button:
            if usuario in usuarios:
                rol = usuarios[usuario]
                st.success(f"Hola {usuario}, rol: {rol}")
                # Guardar en session_state
                st.session_state.usuario_autenticado = usuario
                st.session_state.rol_usuario = rol
                # Retornar inmediatamente para recargar la página con sesión activa
                return usuario, rol
            else:
                st.error("Usuario no reconocido")
        
    return st.session_state.usuario_autenticado, st.session_state.rol_usuario

def logout():
    # Función para cerrar sesión
    st.session_state.usuario_autenticado = None
    st.session_state.rol_usuario = None
    # También actualizamos las variables que usa main.py para mantener coherencia
    if 'usuario' in st.session_state:
        st.session_state.usuario = None
    if 'rol' in st.session_state:
        st.session_state.rol = None