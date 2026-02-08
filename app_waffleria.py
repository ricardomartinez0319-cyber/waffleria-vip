import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="La Waffleria VIP - Pedidos", page_icon="🧇")

# Simulador de base de datos
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = []

st.sidebar.title("Menú de Control")
modo = st.sidebar.radio("Navegar a:", ["Hacer Pedido", "Panel de Administración"])

if modo == "Hacer Pedido":
    st.image("https://yourfiles.cloud/uploads/9caa7594996bc50a02d6f45917143c9f/LOGO%202.png", width=200)
    st.title("🧇 ¡Bienvenido a La Waffleria VIP!")
    
    with st.form("form_pedido"):
        st.subheader("1. Selecciona tu sucursal")
        sucursal = st.selectbox("Sucursal", ["Barrancas / San Cristóbal", "Estrada", "Verbenal"])
        
        st.subheader("2. ¿Qué vas a pedir?")
        productos = st.multiselect("Selecciona tus productos", 
                                  ["Waffle Oreo", "Waffle Pie de Limón", "Waffle Chocolate", "Waffle Frutal", "Bebida"])
        
        st.subheader("3. Datos de entrega")
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo")
            telefono = st.text_input("Teléfono (WhatsApp)")
        with col2:
            entrega = st.radio("Forma de entrega", ["Envío", "Retiro en local", "Consumo en lugar"])
            direccion = st.text_input("Dirección (si es envío)")

        st.subheader("4. Información adicional")
        mensaje = st.text_area("¿Quieres un mensaje personalizado en la caja?")
        cubiertos = st.radio("¿Incluir cubiertos desechables?", ["No", "Sí"])
        pago = st.selectbox("Medio de pago", ["Efectivo", "Nequi", "Datafono"])
        
        enviar = st.form_submit_button("Confirmar Pedido 🚀")

    if enviar:
        pedido_data = {
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "Sucursal": sucursal,
            "Cliente": nombre,
            "Pedido": ", ".join(productos),
            "Entrega": entrega,
            "Pago": pago,
            "Cubiertos": cubiertos,
            "Mensaje": mensaje
        }
        st.session_state.pedidos.append(pedido_data)
        st.success("¡Pedido enviado con éxito! Pronto nos comunicaremos contigo.")

elif modo == "Panel de Administración":
    st.title("👨‍🍳 Panel de Pedidos (Admin)")
    if st.session_state.pedidos:
        df = pd.DataFrame(st.session_state.pedidos)
        st.dataframe(df)
        
        if st.button("Marcar todos como despachados"):
            st.session_state.pedidos = []
            st.rerun()
    else:
        st.write("No hay pedidos nuevos por ahora.")