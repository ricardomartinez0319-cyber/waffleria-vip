import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
from streamlit_image_carousel import ImageCarousel

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="La Waffleria VIP", page_icon="🧇", layout="wide")

# --- ESTILOS PROFESIONALES (Rosado, Café, Amarillo) ---
st.markdown("""
<style>
    :root { --rosado: #FFC0CB; --cafe: #5D4037; --amarillo: #FFD700; }
    .stApp { background-color: #FFF9FB; }
    [data-testid="stSidebar"] { background-color: var(--rosado) !important; }
    h1, h2, h3, h4 { color: var(--cafe) !important; font-family: 'Verdana', sans-serif; }
    
    .product-card {
        background-color: white; border: 2px solid var(--amarillo); border-radius: 15px;
        padding: 10px; text-align: center; margin-bottom: 10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.05);
    }
    .product-card img { width: 100%; border-radius: 10px; height: 140px; object-fit: cover; }
    .price-tag { background-color: var(--amarillo); color: var(--cafe); font-weight: bold; border-radius: 5px; padding: 2px 8px; }
    
    .stTabs [aria-selected="true"] { background-color: var(--amarillo) !important; color: var(--cafe) !important; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS ---
if 'productos_db' not in st.session_state:
    st.session_state.productos_db = [
        {"nombre": "Waffle Oreo", "precio": 15000, "foto": "https://shoppedifacil.app/lawaffleriavip/uploads/carousel/waffle-oreo-3.png", "cat": "Waffles"},
        {"nombre": "Crepe Pollo", "precio": 18000, "foto": "https://via.placeholder.com/150", "cat": "Crepes"},
        {"nombre": "Malteada", "precio": 12000, "foto": "https://via.placeholder.com/150", "cat": "Malteadas"}
    ]

# --- NAVEGACIÓN ---
NUMERO_WHATSAPP = "573152926973"
st.sidebar.image("https://yourfiles.cloud/uploads/9caa7594996bc50a02d6f45917143c9f/LOGO%202.png", width=120)
opcion = st.sidebar.radio("MENÚ", ["🛒 Hacer Pedido", "⚙️ Admin", "📈 Ventas"])

if opcion == "🛒 Hacer Pedido":
    # BANNER MÓVIL (Carrusel)
    imagenes = [
        "https://images.unsplash.com/photo-1551024601-bec78aea704b?q=80&w=1200&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1563805001-a47690623a35?q=80&w=1200&auto=format&fit=crop"
    ]
    ImageCarousel(imagenes, height=250)
    
    st.title("🧇 ¡Bienvenido a La Waffleria VIP!")
    tabs = st.tabs(["Waffles 🧇", "Crepes 🥞", "Malteadas 🥤", "Bebidas 🍹"])
    
    carrito = []
    
    def mostrar(cat, t):
        prods = [p for p in st.session_state.productos_db if p['cat'] == cat]
        cols = t.columns(3)
        for i, p in enumerate(prods):
            with cols[i % 3]:
                st.markdown(f'<div class="product-card"><img src="{p["foto"]}"><h4>{p["nombre"]}</h4><span class="price-tag">${p["precio"]:,}</span></div>', unsafe_allow_html=True)
                if st.checkbox(f"Añadir {p['nombre']}", key=f"{cat}_{i}"):
                    carrito.append(p)

    with tabs[0]: mostrar("Waffles", tabs[0])
    with tabs[1]: mostrar("Crepes", tabs[1])
    with tabs[2]: mostrar("Malteadas", tabs[2])
    with tabs[3]: mostrar("Bebidas", tabs[3])

    if carrito:
        st.markdown("---")
        with st.form("pedido"):
            nombre = st.text_input("Nombre")
            tel = st.text_input("WhatsApp")
            sucursal = st.selectbox("Sucursal", ["Barrancas", "Estrada", "Verbenal"])
            if st.form_submit_button("PEDIR TODO POR WHATSAPP ✅"):
                total = sum([x['precio'] for x in carrito])
                resumen = ", ".join([x['nombre'] for x in carrito])
                msg = f"*ORDEN VIP*\n*Cliente:* {nombre}\n*Pedido:* {resumen}\n*Total:* ${total:,}"
                url = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={url}">', unsafe_allow_html=True)
