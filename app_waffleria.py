import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
# Para el carrusel de imágenes (asegúrate de instalarlo si no lo tienes: pip install streamlit-image-carousel)
from streamlit_image_carousel import ImageCarousel

st.set_page_config(page_title="La Waffleria VIP", page_icon="🧇", layout="wide")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
<style>
    :root { --rosado: #FFC0CB; --cafe: #5D4037; --amarillo: #FFD700; }
    .stApp { background-color: #FFF9FB; }
    [data-testid="stSidebar"] { background-color: var(--rosado) !important; }
    
    .product-card {
        background-color: white;
        border: 2px solid var(--amarillo);
        border-radius: 15px;
        padding: 10px;
        text-align: center;
        margin-bottom: 5px;
    }
    .product-card img { width: 100%; border-radius: 10px; height: 130px; object-fit: cover; }
    
    .resumen-box {
        background-color: #fffde7;
        padding: 15px;
        border-radius: 10px;
        border: 1px dashed var(--cafe);
    }

    /* Ocultar el pie de página de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS ---
if 'productos_db' not in st.session_state:
    st.session_state.productos_db = [
        {"nombre": "Waffle Oreo", "precio": 15000, "foto": "https://shoppedifacil.app/lawaffleriavip/uploads/carousel/waffle-oreo-3.png", "cat": "Waffles"},
        {"nombre": "Crepe de Pollo", "precio": 18000, "foto": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400", "cat": "Crepes"},
        {"nombre": "Malteada Vainilla", "precio": 12000, "foto": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400", "cat": "Malteadas"},
        {"nombre": "Limonada Natural", "precio": 8000, "foto": "https://images.unsplash.com/photo-1523472721958-978152f4d69b?w=400", "cat": "Bebidas Frías"}
    ]

if 'pedidos' not in st.session_state: st.session_state.pedidos = []

NUMERO_WHATSAPP = "573152926973"
CLAVE_ADMIN = "1234"

# --- BANNER CARRUSEL (IMÁGENES PARA MOVER) ---
carousel_images = [
    {"image": "https://images.unsplash.com/photo-1551024601-bec78aea704b?q=80&w=1200&auto=format&fit=crop", "link": "https://www.google.com/search?q=waffles"},
    {"image": "https://images.unsplash.com/photo-1563805001-a47690623a35?q=80&w=1200&auto=format&fit=crop", "link": "https://www.google.com/search?q=malteadas"}
]

# --- SIDEBAR ---
st.sidebar.image("https://yourfiles.cloud/uploads/9caa7594996bc50a02d6f45917143c9f/LOGO%202.png", width=120)
opcion = st.sidebar.radio("NAVEGACIÓN", ["🛒 Menú VIP", "⚙️ Admin Productos", "📈 Reporte Ventas"])

# --- VISTA: HACER PEDIDO ---
if opcion == "🛒 Menú VIP":
    # El Carrusel de Imágenes AQUI
    ImageCarousel(carousel_images, width=800, height=250, loop=True, autoplay=True, interval=3000) # Intervalo en milisegundos
    
    st.title("🧇 ¡Bienvenido a La Waffleria VIP!")
    
    st.write("### 1. Selecciona tus productos:")
    t1, t2, t3, t4 = st.tabs(["Waffles 🧇", "Crepes 🥞", "Malteadas 🥤", "Bebidas Frías 🍹"])
    
    carrito = []

    def mostrar_categoria(categoria, tab_st):
        prods = [p for p in st.session_state.productos_db if p['cat'] == categoria]
        c_grid = tab_st.columns(3)
        for i, p in enumerate(prods):
            with c_grid[i % 3]:
                st.markdown(f"""
                    <div class="product-card">
                        <img src="{p['foto']}">
                        <p style="margin:0; font-weight:bold;">{p['nombre']}</p>
                        <p style="margin:0; color:green;">${p['precio']:,}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.checkbox(f"Llevar {p['nombre']}", key=f"chk_{categoria}_{i}"):
                    carrito.append(p)

    with t1: mostrar_categoria("Waffles", t1)
    with t2: mostrar_categoria("Crepes", t2)
    with t3: mostrar_categoria("Malteadas", t3)
    with t4: mostrar_categoria("Bebidas Frías", t4)

    st.markdown("---")
    
    if carrito:
        st.write("### 2. Resumen y Datos de Envío")
        
        nombres_seleccionados = [x['nombre'] for x in carrito]
        total_pago = sum([x['precio'] for x in carrito])
        
        st.markdown(f"""
            <div class="resumen-box">
                <b>Productos seleccionados:</b> {", ".join(nombres_seleccionados)}<br>
                <b>Total estimado: ${total_pago:,}</b>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("unico_formulario"):
            c1, c2 = st.columns(2)
            with c1:
                nombre = st.text_input("Nombre Completo")
                tel = st.text_input("WhatsApp")
            with c2:
                sucursal = st.selectbox("Sucursal", ["Barrancas", "Estrada", "Verbenal"])
                metodo = st.radio("Entrega", ["Domicilio", "Retiro en local", "En mesa"])
            
            pago = st.selectbox("Método de Pago", ["Nequi", "Efectivo", "Datafono"])
            notas = st.text_area("Comentarios (ej: sin azúcar, extras)")
            
            if st.form_submit_button("ENVIAR TODO POR WHATSAPP ✅"):
                if not nombre or not tel:
                    st.error("Por favor completa tu nombre y WhatsApp")
                else:
                    resumen_txt = ", ".join(nombres_seleccionados)
                    msg = f"*ORDEN VIP*\n*Cliente:* {nombre}\n*Pedido:* {resumen_txt}\n*Total:* ${total_pago:,}\n*Sucursal:* {sucursal}\n*Notas:* {notas}"
                    url_wa = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                    
                    st.success("¡Redirigiendo!")
                    st.markdown(f'<meta http-equiv="refresh" content="0;URL={url_wa}">', unsafe_allow_html=True)
    else:
        st.info("👆 Selecciona al menos un producto arriba para ver el formulario de envío.")

# --- VISTA ADMIN (IGUAL QUE ANTES) ---
elif opcion == "⚙️ Admin Productos":
    st.title("Gestión de Productos")
    password = st.text_input("Contraseña Admin", type="password")
    if password == CLAVE_ADMIN:
        with st.expander("➕ Crear Nuevo Producto"):
            n_nombre = st.text_input("Nombre")
            n_cat = st.selectbox("Categoría", ["Waffles", "Crepes", "Malteadas", "Bebidas Frías"])
            n_precio = st.number_input("Precio", min_value=0, step=500)
            n_foto = st.text_input("Link de la foto (URL)")
            if st.button("Guardar Producto"):
                st.session_state.productos_db.append({"nombre": n_nombre, "precio": n_precio, "foto": n_foto, "cat": n_cat})
                st.rerun()
        
        st.subheader("Listado de Productos")
        for i, p in enumerate(st.session_state.productos_db):
            c1, c2, c3 = st.columns([1,3,1])
            c1.image(p['foto'], width=80)
            c2.write(f"**{p['cat']}** | {p['nombre']} - ${p['precio']:,}")
            if c3.button("Eliminar", key=f"del_prod_{i}"):
                st.session_state.productos_db.pop(i)
                st.rerun()

# --- VISTA: VENTAS (IGUAL QUE ANTES) ---
elif opcion == "📈 Reporte Ventas":
    st.title("Historial de Pedidos")
    password = st.text_input("Contraseña Admin", type="password")
    if password == CLAVE_ADMIN:
        if st.session_state.pedidos:
            st.table(pd.DataFrame(st.session_state.pedidos))
        else:
            st.info("No hay pedidos registrados hoy.")
