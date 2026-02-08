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
    
    /* Títulos */
    h1, h2, h3, h4, label {
        color: var(--cafe) !important;
        font-family: 'Verdana', sans-serif;
    }

    /* Banner Principal */
    .banner-container {
        width: 100%;
        height: 250px;
        overflow: hidden;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 4px solid var(--amarillo);
    }
    .banner-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f0f0;
        border-radius: 10px 10px 0px 0px;
        padding: 10px 15px;
        color: var(--cafe);
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--amarillo) !important;
        border-bottom: 3px solid var(--cafe);
    }

    /* Tarjetas de Producto */
    .product-card {
        background-color: var(--blanco);
        border: 2px solid var(--amarillo);
        border-radius: 15px;
        padding: 10px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .product-card img {
        width: 100%;
        border-radius: 10px;
        height: 140px;
        object-fit: cover;
    }
    .price-tag {
        background-color: var(--amarillo);
        color: var(--cafe);
        font-weight: bold;
        font-size: 18px;
        border-radius: 5px;
        padding: 2px 8px;
        display: inline-block;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS TEMPORAL ---
if 'productos_db' not in st.session_state:
    st.session_state.productos_db = [
        {"nombre": "Waffle Oreo", "precio": 15000, "foto": "https://shoppedifacil.app/lawaffleriavip/uploads/carousel/waffle-oreo-3.png", "cat": "Waffles"},
        {"nombre": "Crepe de Pollo", "precio": 18000, "foto": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400", "cat": "Crepes"},
        {"nombre": "Malteada Vainilla", "precio": 12000, "foto": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400", "cat": "Malteadas"},
        {"nombre": "Limonada Natural", "precio": 8000, "foto": "https://images.unsplash.com/photo-1523472721958-978152f4d69b?w=400", "cat": "Bebidas Frías"}
    ]

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = []

# --- CONFIGURACIÓN ---
NUMERO_WHATSAPP = "573152926973"
CLAVE_ADMIN = "1234"

# --- SIDEBAR ---
st.sidebar.image("https://yourfiles.cloud/uploads/9caa7594996bc50a02d6f45917143c9f/LOGO%202.png", width=120)
opcion = st.sidebar.radio("NAVEGACIÓN", ["🛒 Menú VIP", "⚙️ Admin Productos", "📈 Reporte Ventas"])

# --- VISTA: HACER PEDIDO ---
if opcion == "🛒 Menú VIP":
    # Banner Principal Genérico de Comida
    st.markdown("""
        <div class="banner-container">
            <img src="https://images.unsplash.com/photo-1551024601-bec78aea704b?q=80&w=1200&auto=format&fit=crop">
        </div>
    """, unsafe_allow_html=True)
    
    st.title("🧇 ¡Bienvenido a La Waffleria VIP!")
    
    # Pestañas de Categorías
    t1, t2, t3, t4 = st.tabs(["Waffles 🧇", "Crepes 🥞", "Malteadas 🥤", "Bebidas Frías 🍹"])
    
    seleccionados = []

    def mostrar_menu(categoria, tab_st):
        prods = [p for p in st.session_state.productos_db if p['cat'] == categoria]
        if not prods:
            tab_st.write("Estamos preparando nuevos platos para esta categoría...")
            return
        
        c_grid = tab_st.columns(2)
        for i, p in enumerate(prods):
            with c_grid[i % 2]:
                st.markdown(f"""
                    <div class="product-card">
                        <img src="{p['foto']}">
                        <h4>{p['nombre']}</h4>
                        <div class="price-tag">${p['precio']:,}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.checkbox(f"Agregar {p['nombre']}", key=f"sel_{categoria}_{i}"):
                    seleccionados.append(p)

    with t1: mostrar_menu("Waffles", t1)
    with t2: mostrar_menu("Crepes", t2)
    with t3: mostrar_menu("Malteadas", t3)
    with t4: mostrar_menu("Bebidas Frías", t4)

    st.markdown("---")
    
    # Formulario de Envío
    if seleccionados:
        with st.form("confirmar_orden"):
            st.subheader("Finalizar mi Pedido")
            col_a, col_b = st.columns(2)
            with col_a:
                nombre = st.text_input("¿A nombre de quién?")
                tel = st.text_input("WhatsApp de contacto")
            with col_b:
                sucursal = st.selectbox("Punto de venta", ["Barrancas", "Estrada", "Verbenal"])
                metodo = st.radio("Entrega", ["Domicilio", "Retiro en local", "Consumo en mesa"])
            
            pago = st.selectbox("Método de Pago", ["Nequi", "Efectivo", "Daviplata", "Datafono"])
            notas = st.text_area("Notas adicionales (Sin azúcar, extras, etc.)")
            
            if st.form_submit_button("PEDIR POR WHATSAPP ✅"):
                if not nombre or not tel:
                    st.error("Por favor completa tu nombre y teléfono.")
                else:
                    total_final = sum([x['precio'] for x in seleccionados])
                    resumen_prods = ", ".join([x['nombre'] for x in seleccionados])
                    
                    # Guardar para reporte
                    st.session_state.pedidos.append({
                        "Fecha": datetime.now().strftime("%d/%m %H:%M"),
                        "Cliente": nombre, "Pedido": resumen_prods, "Total": total_final
                    })
                    
                    # Mensaje WhatsApp
                    mensaje = f"*NUEVO PEDIDO - LA WAFFLERÍA VIP*\n\n" \
                              f"*Cliente:* {nombre}\n" \
                              f"*Sucursal:* {sucursal}\n" \
                              f"*Pedido:* {resumen_prods}\n" \
                              f"*Total:* ${total_final:,}\n" \
                              f"*Pago:* {pago}\n" \
                              f"*Método:* {metodo}\n" \
                              f"*Notas:* {notas}"
                    
                    url_wa = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(mensaje)}"
                    
                    # Redireccionamiento directo
                    st.success("¡Redirigiendo a WhatsApp...!")
                    st.markdown(f'<meta http-equiv="refresh" content="0;URL={url_wa}">', unsafe_allow_html=True)

# --- VISTA: ADMIN ---
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

# --- VISTA: VENTAS ---
elif opcion == "📈 Reporte Ventas":
    st.title("Historial de Pedidos")
    password = st.text_input("Contraseña Admin", type="password")
    if password == CLAVE_ADMIN:
        if st.session_state.pedidos:
            st.table(pd.DataFrame(st.session_state.pedidos))
        else:
            st.info("No hay pedidos registrados hoy.")
