import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Waffleria VIP", page_icon="🧇", layout="wide")

# --- ESTILOS PERSONALIZADOS (Rosado, Café, Amarillo) ---
st.markdown("""
<style>
    :root {
        --rosado: #FFC0CB;
        --cafe: #5D4037;
        --amarillo: #FFD700;
        --blanco: #FFFFFF;
    }
    
    .stApp { background-color: #FFF9FB; }
    
    /* Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: var(--rosado) !important;
    }
    
    /* Títulos y Etiquetas */
    h1, h2, h3, label, .stMarkdown {
        color: var(--cafe) !important;
        font-family: 'Verdana', sans-serif;
    }

    /* Tarjetas de Producto */
    .product-card {
        background-color: var(--blanco);
        border: 3px solid var(--amarillo);
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .product-card img {
        width: 100%;
        border-radius: 15px;
        height: 180px;
        object-fit: cover;
    }
    .price-tag {
        background-color: var(--amarillo);
        color: var(--cafe);
        font-weight: bold;
        font-size: 22px;
        border-radius: 8px;
        padding: 5px 10px;
        display: inline-block;
        margin-top: 10px;
    }
    
    /* Botón de WhatsApp */
    .btn-wa {
        background-color: #25D366;
        color: white !important;
        padding: 18px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: bold;
        display: block;
        text-align: center;
        font-size: 22px;
        margin-top: 20px;
        box-shadow: 0px 4px 15px rgba(37, 211, 102, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS TEMPORAL ---
if 'productos_db' not in st.session_state:
    st.session_state.productos_db = [
        {"nombre": "Waffle Oreo", "precio": 15000, "foto": "https://shoppedifacil.app/lawaffleriavip/uploads/carousel/waffle-oreo-3.png"},
        {"nombre": "Waffle Pie de Limón", "precio": 16000, "foto": "https://shoppedifacil.app/lawaffleriavip/uploads/carousel/waffle-pie-limon.png"},
        {"nombre": "Waffle Frutal", "precio": 14000, "foto": "https://shoppedifacil.app/lawaffleriavip/uploads/carousel/waffle-frutal.png"},
        {"nombre": "Waffle Chocolate", "precio": 15500, "foto": "https://shoppedifacil.app/lawaffleriavip/uploads/carousel/waffle-chocolate-2.png"}
    ]

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = []

# --- CONFIGURACIÓN ---
NUMERO_WHATSAPP = "573152926973"
CLAVE_ADMIN = "1234"

# --- SIDEBAR ---
st.sidebar.image("https://yourfiles.cloud/uploads/9caa7594996bc50a02d6f45917143c9f/LOGO%202.png", width=140)
opcion = st.sidebar.radio("MENÚ", ["🛒 Hacer Pedido", "⚙️ Admin Productos", "📈 Registro Ventas"])

# --- VISTA: HACER PEDIDO ---
if opcion == "🛒 Hacer Pedido":
    st.title("🧇 ¡La Waffleria VIP!")
    st.write("Selecciona tus productos favoritos:")

    cols = st.columns(2)
    seleccionados = []
    
    for idx, p in enumerate(st.session_state.productos_db):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="product-card">
                    <img src="{p['foto']}">
                    <h3>{p['nombre']}</h3>
                    <div class="price-tag">${p['precio']:,}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.checkbox(f"Pedir {p['nombre']}", key=f"p_{idx}"):
                seleccionados.append(p)

    st.markdown("---")
    
    with st.form("form_pedido"):
        st.subheader("Finalizar Pedido")
        c1, c2 = st.columns(2)
        with c1:
            nombre = st.text_input("Tu Nombre")
            tel = st.text_input("Tu WhatsApp")
        with c2:
            sucursal = st.selectbox("Sucursal", ["Barrancas / San Cristóbal", "Estrada", "Verbenal"])
            entrega = st.radio("Entrega", ["Domicilio", "Retiro", "Local"])
            
        pago = st.selectbox("Pago", ["Nequi", "Efectivo", "Daviplata"])
        notas = st.text_area("Notas adicionales")
        
        if st.form_submit_button("Generar Orden 🚀"):
            if not nombre or not seleccionados:
                st.error("Completa tu nombre y elige al menos un producto.")
            else:
                total = sum([x['precio'] for x in seleccionados])
                resumen = ", ".join([x['nombre'] for x in seleccionados])
                
                # Guardar para Admin
                st.session_state.pedidos.append({"Fecha": datetime.now().strftime("%d/%m %H:%M"), "Cliente": nombre, "Pedido": resumen, "Total": total})
                
                # Mensaje WhatsApp
                msg = f"*PEDIDO WAFFLERÍA VIP*\n*Cliente:* {nombre}\n*Pedido:* {resumen}\n*Total:* ${total:,}\n*Pago:* {pago}\n*Sucursal:* {sucursal}"
                url = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                
                st.success("¡Pedido listo!")
                st.markdown(f'<a href="{url}" target="_blank" class="btn-wa">ENVIAR POR WHATSAPP ✅</a>', unsafe_allow_html=True)

# --- VISTA: ADMIN ---
elif opcion == "⚙️ Admin Productos":
    st.title("Gestión de Inventario")
    pw = st.text_input("Clave", type="password")
    if pw == CLAVE_ADMIN:
        with st.expander("Añadir Producto"):
            n = st.text_input("Nombre")
            pr = st.number_input("Precio", min_value=0)
            img = st.text_input("URL Imagen")
            if st.button("Agregar"):
                st.session_state.productos_db.append({"nombre": n, "precio": pr, "foto": img})
                st.rerun()
        
        for i, p in enumerate(st.session_state.productos_db):
            col1, col2 = st.columns([3,1])
            col1.write(f"**{p['nombre']}** - ${p['precio']}")
            if col2.button("X", key=f"del_{i}"):
                st.session_state.productos_db.pop(i)
                st.rerun()

# --- VISTA: VENTAS ---
elif opcion == "📈 Registro Ventas":
    st.title("Historial")
    pw = st.text_input("Clave", type="password")
    if pw == CLAVE_ADMIN:
        if st.session_state.pedidos:
            st.table(pd.DataFrame(st.session_state.pedidos))
        else:
            st.write("Sin ventas.")


