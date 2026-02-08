import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="La Waffleria VIP", page_icon="🧇", layout="wide")

# --- ESTILOS PROFESIONALES (Rosado, Café, Amarillo) ---
st.markdown("""
<style>
    :root { --rosado: #FFC0CB; --cafe: #5D4037; --amarillo: #FFD700; }
    .stApp { background-color: #FFF9FB; }
    [data-testid="stSidebar"] { background-color: var(--rosado) !important; }
    h1, h2, h3, h4 { color: var(--cafe) !important; font-family: 'Verdana', sans-serif; }
    
    /* Banner Movil */
    .banner-container {
        border-radius: 20px; overflow: hidden; border: 4px solid var(--amarillo);
        margin-bottom: 20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    
    .product-card {
        background-color: white; border: 2px solid var(--amarillo); border-radius: 15px;
        padding: 10px; text-align: center; margin-bottom: 10px; height: 320px;
    }
    .product-card img { width: 100%; border-radius: 10px; height: 160px; object-fit: cover; }
    .price-tag { background-color: var(--amarillo); color: var(--cafe); font-weight: bold; border-radius: 5px; padding: 2px 8px; font-size: 20px;}
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS ---
if 'productos_db' not in st.session_state:
    st.session_state.productos_db = [
        {"nombre": "Waffle Oreo", "precio": 15000, "foto": "https://shoppedifacil.app/lawaffleriavip/uploads/carousel/waffle-oreo-3.png", "cat": "Waffles"},
        {"nombre": "Waffle Frutal", "precio": 15000, "foto": "https://shoppedifacil.app/lawaffleriavip/uploads/carousel/waffle-frutal.png", "cat": "Waffles"},
        {"nombre": "Crepe Pollo", "precio": 18000, "foto": "https://via.placeholder.com/400x300?text=Crepe+Delicioso", "cat": "Crepes"},
        {"nombre": "Malteada", "precio": 12000, "foto": "https://via.placeholder.com/400x300?text=Malteada+Fria", "cat": "Malteadas"}
    ]

# --- VARIABLES ---
NUMERO_WHATSAPP = "573152926973"
CLAVE_ADMIN = "1234"

# --- SIDEBAR ---
st.sidebar.image("https://yourfiles.cloud/uploads/9caa7594996bc50a02d6f45917143c9f/LOGO%202.png", width=120)
opcion = st.sidebar.radio("MENÚ", ["🛒 Hacer Pedido", "⚙️ Admin", "📈 Ventas"])

if opcion == "🛒 Hacer Pedido":
    # BANNER DINÁMICO (Sin librerías externas para evitar errores)
    st.markdown('<div class="banner-container">', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1551024601-bec78aea704b?q=80&w=1200&auto=format&fit=crop")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.title("🧇 ¡Bienvenido a La Waffleria VIP!")
    
    tabs = st.tabs(["Waffles 🧇", "Crepes 🥞", "Malteadas 🥤", "Bebidas 🍹"])
    carrito = []
    
    def mostrar_menu(categoria, t_obj):
        prods = [p for p in st.session_state.productos_db if p['cat'] == categoria]
        if not prods:
            t_obj.write("Próximamente más delicias...")
            return
        
        cols = t_obj.columns(3)
        for i, p in enumerate(prods):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="product-card">
                    <img src="{p['foto']}">
                    <h4>{p['nombre']}</h4>
                    <span class="price-tag">${p['precio']:,}</span>
                </div>
                """, unsafe_allow_html=True)
                if st.checkbox(f"Llevar {p['nombre']}", key=f"sel_{categoria}_{i}"):
                    carrito.append(p)

    mostrar_menu("Waffles", tabs[0])
    mostrar_menu("Crepes", tabs[1])
    mostrar_menu("Malteadas", tabs[2])
    mostrar_menu("Bebidas", tabs[3])

    if carrito:
        st.markdown("---")
        with st.form("final"):
            st.subheader("Finalizar mi Orden")
            nombre = st.text_input("Nombre")
            tel = st.text_input("WhatsApp")
            sucursal = st.selectbox("Sucursal", ["Barrancas", "Estrada", "Verbenal"])
            if st.form_submit_button("PEDIR TODO POR WHATSAPP ✅"):
                resumen = ", ".join([x['nombre'] for x in carrito])
                total = sum([x['precio'] for x in carrito])
                msg = f"*ORDEN VIP*\n*Cliente:* {nombre}\n*Pedido:* {resumen}\n*Total:* ${total:,}\n*Sucursal:* {sucursal}"
                url = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.success("¡Redirigiendo a WhatsApp!")
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={url}">', unsafe_allow_html=True)

elif opcion == "⚙️ Admin":
    st.title("Panel Admin")
    pw = st.text_input("Clave", type="password")
    if pw == CLAVE_ADMIN:
        st.success("Acceso concedido")
        # Aquí puedes agregar el código de gestión de productos que teníamos
