import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="La Waffleria VIP - Pedidos", page_icon="🧇", layout="wide")

# --- BASE DE DATOS SIMULADA ---
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = []

if 'productos_db' not in st.session_state:
    # Productos iniciales por defecto
    st.session_state.productos_db = [
        {"nombre": "Waffle Oreo", "precio": 15000, "foto": "https://via.placeholder.com/150"},
        {"nombre": "Waffle Frutal", "precio": 14000, "foto": "https://via.placeholder.com/150"}
    ]

# --- NAVEGACIÓN ---
st.sidebar.title("La Waffleria VIP")
modo = st.sidebar.radio("Ir a:", ["🛍️ Hacer Pedido", "⚙️ Gestionar Productos", "📊 Panel de Ventas"])

# --- WHATSAPP CONFIG ---
NUMERO_WHATSAPP = "573152926973" # <-- REEMPLAZA CON TU NÚMERO (Sin el +)

# --- MODO: HACER PEDIDO ---
if modo == "🛍️ Hacer Pedido":
    st.image("https://yourfiles.cloud/uploads/9caa7594996bc50a02d6f45917143c9f/LOGO%202.png", width=150)
    st.title("¡Pide tus Waffles!")

    with st.form("form_pedido"):
        st.subheader("1. Tus Datos")
        col_a, col_b = st.columns(2)
        with col_a:
            nombre = st.text_input("¿Quién pide?")
            sucursal = st.selectbox("Sucursal", ["Barrancas / San Cristóbal", "Estrada", "Verbenal"])
        with col_b:
            telefono = st.text_input("Tu WhatsApp")
            entrega = st.radio("Entrega", ["Retiro en local", "Envío", "Consumo en lugar"])

        st.subheader("2. Menú")
        # Mostramos los productos que el admin creó
        nombres_productos = [p['nombre'] for p in st.session_state.productos_db]
        seleccionados = st.multiselect("Elige tus favoritos", nombres_productos)
        
        st.subheader("3. Pago y Extras")
        pago = st.selectbox("Medio de pago", ["Efectivo", "Nequi", "Daviplata"])
        notas = st.text_area("Notas especiales (sin cebolla, más chocolate...)")
        
        enviar = st.form_submit_button("Confirmar y Enviar a WhatsApp 🚀")

    if enviar:
        # Calcular Resumen
        resumen_pedido = ", ".join(seleccionados)
        ahora = datetime.now().strftime("%d/%m %H:%M")
        
        # Guardar en el panel (volátil por ahora)
        pedido_data = {"Hora": ahora, "Sucursal": sucursal, "Cliente": nombre, "Pedido": resumen_pedido, "Pago": pago}
        st.session_state.pedidos.append(pedido_data)

        # CREAR MENSAJE PARA WHATSAPP
        texto = f"*NUEVO PEDIDO - LA WAFFLERIA VIP*\n\n" \
                f"*Cliente:* {nombre}\n" \
                f"*Sucursal:* {sucursal}\n" \
                f"*Pedido:* {resumen_pedido}\n" \
                f"*Entrega:* {entrega}\n" \
                f"*Pago:* {pago}\n" \
                f"*Notas:* {notas}"
        
        texto_url = urllib.parse.quote(texto)
        url_wa = f"https://wa.me/{NUMERO_WHATSAPP}?text={texto_url}"
        
        st.success("¡Pedido registrado!")
        st.markdown(f'''
            <a href="{url_wa}" target="_blank">
                <button style="background-color: #25D366; color: white; padding: 15px; border: none; border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold;">
                    CLIC AQUÍ PARA ENVIAR POR WHATSAPP ✅
                </button>
            </a>
            ''', unsafe_allow_html=True)

# --- MODO: GESTIONAR PRODUCTOS ---
elif modo == "⚙️ Gestionar Productos":
    st.title("Crear y Editar Productos")
    
    with st.expander("➕ Añadir Nuevo Producto"):
        nuevo_nombre = st.text_input("Nombre del producto")
        nuevo_precio = st.number_input("Precio", min_value=0, step=500)
        nueva_foto = st.text_input("Link de la foto (URL)")
        if st.button("Guardar Producto"):
            st.session_state.productos_db.append({"nombre": nuevo_nombre, "precio": nuevo_precio, "foto": nueva_foto})
            st.success("Producto añadido!")
            st.rerun()

    st.subheader("Productos Actuales")
    for i, p in enumerate(st.session_state.productos_db):
        col_img, col_txt, col_btn = st.columns([1, 2, 1])
        with col_img:
            st.image(p['foto'], width=80)
        with col_txt:
            st.write(f"**{p['nombre']}** - ${p['precio']}")
        with col_btn:
            if st.button(f"Eliminar", key=f"del_{i}"):
                st.session_state.productos_db.pop(i)
                st.rerun()

# --- MODO: PANEL DE VENTAS ---
elif modo == "📊 Panel de Ventas":
    st.title("Panel de Pedidos")
    if st.session_state.pedidos:
        df = pd.DataFrame(st.session_state.pedidos)
        st.table(df)
        if st.button("Limpiar historial"):
            st.session_state.pedidos = []
            st.rerun()
    else:
        st.info("No hay pedidos registrados en esta sesión.")

