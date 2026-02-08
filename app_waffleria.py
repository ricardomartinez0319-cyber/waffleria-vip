import streamlit as st
import pandas as pd
import urllib.parse

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="La Waffleria VIP", page_icon="🧇", layout="wide")

# --- ESTILOS (Rosado, Café, Amarillo) ---
st.markdown("""
<style>
    :root { --rosado: #FFC0CB; --cafe: #5D4037; --amarillo: #FFD700; }
    .stApp { background-color: #FFF9FB; }
    [data-testid="stSidebar"] { background-color: var(--rosado) !important; }
    .product-card {
        background-color: white; border: 2px solid var(--amarillo); border-radius: 15px;
        padding: 15px; text-align: center; margin-bottom: 10px;
    }
    .product-card img { width: 100%; border-radius: 10px; height: 160px; object-fit: cover; }
    .price-tag { background-color: var(--amarillo); color: var(--cafe); font-weight: bold; border-radius: 5px; padding: 5px; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS INICIAL ---
if 'productos_db' not in st.session_state:
    st.session_state.productos_db = [
        {"n": "Waffle Oreo", "p": 15000, "f": "https://shoppedifacil.app/lawaffleriavip/uploads/carousel/waffle-oreo-3.png", "c": "Waffles"},
        {"n": "Crepe Pollo", "p": 18000, "f": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400", "c": "Crepes"},
        {"n": "Malteada", "p": 12000, "f": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400", "c": "Malteadas"}
    ]

# --- MENÚ LATERAL ---
st.sidebar.image("https://yourfiles.cloud/uploads/9caa7594996bc50a02d6f45917143c9f/LOGO%202.png", width=120)
opcion = st.sidebar.radio("IR A:", ["🛒 Hacer Pedido", "⚙️ Admin"])

if opcion == "🛒 Hacer Pedido":
    # Banner Fijo (Elegante y sin errores)
    st.image("https://images.unsplash.com/photo-1551024601-bec78aea704b?q=80&w=1200", use_container_width=True)
    st.title("🧇 La Waffleria VIP")
    
    tabs = st.tabs(["Waffles 🧇", "Crepes 🥞", "Malteadas 🥤", "Bebidas 🍹"])
    carrito = []

    def mostrar_seccion(cat, t_idx):
        prods = [x for x in st.session_state.productos_db if x['c'] == cat]
        cols = tabs[t_idx].columns(3)
        for i, p in enumerate(prods):
            with cols[i % 3]:
                st.markdown(f'<div class="product-card"><img src="{p["f"]}"><h4>{p["n"]}</h4><span class="price-tag">${p["p"]:,}</span></div>', unsafe_allow_html=True)
                if st.checkbox(f"Llevar {p['n']}", key=f"{cat}{i}"):
                    carrito.append(p)

    mostrar_seccion("Waffles", 0); mostrar_seccion("Crepes", 1); mostrar_seccion("Malteadas", 2); mostrar_seccion("Bebidas", 3)

    if carrito:
        st.markdown("---")
        with st.form("pedido_final"):
            st.subheader("Finalizar Orden")
            nom = st.text_input("Tu Nombre")
            tel = st.text_input("Tu WhatsApp")
            if st.form_submit_button("PEDIR POR WHATSAPP ✅"):
                if nom and tel:
                    res = ", ".join([x['n'] for x in carrito])
                    tot = sum([x['p'] for x in carrito])
                    msg = f"*ORDEN VIP*\n*Cliente:* {nom}\n*Pedido:* {res}\n*Total:* ${tot:,}"
                    url = f"https://wa.me/573152926973?text={urllib.parse.quote(msg)}"
                    st.markdown(f'<meta http-equiv="refresh" content="0;URL={url}">', unsafe_allow_html=True)
                else:
                    st.error("Pon tu nombre y WhatsApp para continuar.")

elif opcion == "⚙️ Admin":
    st.title("Panel de Control")
    clave = st.text_input("Contraseña", type="password")
    if clave == "1234":
        st.success("¡Hola Ricardo! Aquí podrás agregar fotos y precios nuevos pronto.")
