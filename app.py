import streamlit as st
import pandas as pd
import glob
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Dashboard Categorizado - Kioscos IA", layout="wide")

# Estilo Neón Profesional
st.markdown("""
    <style>
    .stApp { background-color: #030712; color: #f8fafc; }
    .category-box {
        background-color: #0f172a;
        border-left: 5px solid #00d4ff;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .neon-text { color: #00d4ff; text-shadow: 0 0 8px rgba(0, 212, 255, 0.4); font-family: 'Poppins', sans-serif; }
    .status-label { font-weight: bold; font-size: 0.9em; color: #94a3b8; }
    </style>
    """, unsafe_allow_html=True)

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
    
    # Barra Lateral
    st.sidebar.markdown("<h2 class='neon-text'>FILTROS</h2>", unsafe_allow_html=True)
    sel_ub = st.sidebar.selectbox("📍 Ubicación", df[col_ub].unique())
    df_filtrado = df[df[col_ub] == sel_ub].sort_values(by=col_fe, ascending=False)
    sel_fe = st.sidebar.selectbox("📅 Fecha", df_filtrado[col_fe].unique())
    reporte = df_filtrado[df_filtrado[col_fe] == sel_fe].iloc[0]

    st.markdown(f"<h1 class='neon-text'>REPORTE CATEGORIZADO: {sel_ub}</h1>", unsafe_allow_html=True)
    
    # Definición de Categorías
    categorias = {
        "🏗️ INFRAESTRUCTURA Y FACHADA": ['DELANTERA', 'POSTERIOR', 'MUEBLES', 'ILUMINACIÓN', 'PINTURA', 'LIMPIEZA'],
        "🤖 MAQUINARIA Y SISTEMAS": ['ENERGIA', 'INTERNET', 'CABLEADO', 'CAMARAS SEGURIDAD', 'LOCKERS', 'ENERGÍA'],
        "🖥️ GESTIÓN DE PANTALLAS": ['TOTEM IZQUIERDO', 'TOTEM DERECHO', 'TV IZQUIERDO', 'TV DERECHO', 'PANTALLAS'],
    }

    # 1. KPIs Rápidos
    k1, k2, k3 = st.columns(3)
    k1.metric("Inspector", reporte.get('TU NOMBRE', 'N/A'))
    k2.metric("Fecha", str(sel_fe))
    k3.metric("Ubicación", sel_ub)

    st.divider()

    # 2. Renderizado por Categorías
    cols_usadas = [col_ub, col_fe, 'TU NOMBRE']
    
    for titulo, campos in categorias.items():
        campos_presentes = [c for c in campos if c in df.columns]
        if campos_presentes:
            st.markdown(f"<div class='category-box'><h3 class='neon-text'>{titulo}</h3>", unsafe_allow_html=True)
            c_cols = st.columns(len(campos_presentes))
            for i, campo in enumerate(campos_presentes):
                val = str(reporte.get(campo, 'N/A')).upper()
                with c_cols[i]:
                    st.markdown(f"<span class='status-label'>{campo}</span>", unsafe_allow_html=True)
                    if "PERFECTO" in val or "OK" in val: st.success("✅ OK")
                    elif "PROBLEMA" in val or "SUCIO" in val: st.warning(f"⚠️ {val}")
                    elif "NO FUNCIONA" in val: st.error("❌ FALLA")
                    else: st.info(val)
                cols_usadas.append(campo)
            st.markdown("</div>", unsafe_allow_html=True)

    # 3. Observaciones y Fotos (Todo lo que tenga la palabra 'OBSERVACIÓN' o 'FOTO')
    obs_cols = [c for c in df.columns if 'OBSERV' in c.upper()]
    foto_cols = [c for c in df.columns if 'FOTO' in c.upper()]

    st.markdown("<div class='category-box'><h3 class='neon-text'>📝 AUDITORÍA Y OBSERVACIONES</h3>", unsafe_allow_html=True)
    for o in obs_cols:
        txt = str(reporte.get(o, '')).strip()
        if txt.lower() not in ['nan', '', 'none', '.']:
            st.write(f"**{o}:**")
            st.info(txt)
    st.markdown("</div>", unsafe_allow_html=True)

    if foto_cols:
        st.markdown("<div class='category-box'><h3 class='neon-text'>📸 EVIDENCIA FOTOGRÁFICA</h3>", unsafe_allow_html=True)
        for f in foto_cols:
            links = str(reporte.get(f, ''))
            if "http" in links:
                for link in links.split(';'):
                    st.image(link.strip(), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("Esperando datos...")
