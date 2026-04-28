import streamlit as st
import pandas as pd
import glob
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Monitor Kioscos IA", layout="wide")

# 2. INYECCIÓN DE ESTILO CSS (Aquí es donde ocurre la magia visual)
st.markdown("""
    <style>
    /* Fondo general oscuro */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Estilo de las Tarjetas (Cards) */
    .kiosco-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    
    /* Títulos Neón */
    .neon-text {
        color: #00d4ff;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Badges de Estado */
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
        float: right;
    }
    .status-online { background-color: rgba(46, 204, 113, 0.2); color: #2ecc71; border: 1px solid #2ecc71; }
    .status-offline { background-color: rgba(231, 76, 60, 0.2); color: #e74c3c; border: 1px solid #e74c3c; }
    
    /* Ajustes de métricas estándar */
    [data-testid="stMetricValue"] { color: #00d4ff !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE CARGA DE DATOS
@st.cache_data(ttl=300)
def cargar_datos():
    archivos = glob.glob("*.xlsx") + glob.glob("*.csv")
    if not archivos: return None
    try:
        if archivos[0].endswith('.xlsx'): return pd.read_excel(archivos[0])
        return pd.read_csv(archivos[0], encoding='utf-8-sig')
    except: return None

df = cargar_datos()

if df is not None:
    df.columns = df.columns.str.strip()
    col_ub = [c for c in df.columns if 'UBICAC' in c.upper()][0]
    col_fe = [c for c in df.columns if 'FECHA' in c.upper()][0]
    
    # --- BARRA LATERAL ---
    st.sidebar.markdown("<h2 class='neon-text'>CENTRO DE CONTROL</h2>", unsafe_allow_html=True)
    sel_ub = st.sidebar.selectbox("📍 Seleccionar Kiosco", df[col_ub].unique())
    
    df_filtrado = df[df[col_ub] == sel_ub].sort_values(by=col_fe, ascending=False)
    sel_fe = st.sidebar.selectbox("📅 Fecha de Reporte", df_filtrado[col_fe].unique())
    reporte = df_filtrado[df_filtrado[col_fe] == sel_fe].iloc[0]

    # --- ENCABEZADO DE KPIs ---
    st.markdown(f"<h1 class='neon-text'>ESTADO OPERATIVO: {sel_ub}</h1>", unsafe_allow_html=True)
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("ESTADO RED", "ONLINE 🟢")
    k2.metric("ENERGÍA", "98% ⚡")
    k3.metric("PANTALLAS", "4 ACTIVAS")
    k4.metric("ÚLTIMO PING", "Hace 2 min")

    st.markdown("---")

    # --- DISEÑO DE TARJETA PRINCIPAL (TIPO IMAGEN DE REFERENCIA) ---
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown(f"""
        <div class="kiosco-card">
            <span class="status-badge status-online">● ONLINE</span>
            <h2 style="margin-top:0;">{sel_ub}</h2>
            <hr style="border-color:#334155;">
            <div style="display: flex; justify-content: space-between; color: #94a3b8;">
                <span><b>ID:</b> K-{sel_ub[:3].upper()}</span>
                <span><b>IP:</b> 192.168.1.{st.session_state.get('ip', '105')}</span>
            </div>
            <br>
            <p style="color:#00d4ff;">📝 <b>DIAGNÓSTICO DEL TÉCNICO:</b></p>
            <p style="font-style: italic;">{reporte.get('DESCRIBA SUS OBSERVACIONES GENERALES LUEGO DE LA VISITA. PUEDE AMPLIAR O AGREGAR INFORMACIÓN', 'Sin observaciones.')}</p>
        </div>
        """, unsafe_allow
