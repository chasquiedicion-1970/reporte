import streamlit as st
import pandas as pd
import glob
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Dashboard Total - Kioscos IA", layout="wide")

# Estilo Neón Profesional
st.markdown("""
    <style>
    .stApp { background-color: #030712; color: #f8fafc; }
    .kiosco-card {
        background-color: #0f172a;
        border: 1px solid #00d4ff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
        margin-bottom: 20px;
    }
    .neon-text { color: #00d4ff; text-shadow: 0 0 8px rgba(0, 212, 255, 0.5); }
    [data-testid="stMetricValue"] { color: #00d4ff !important; font-family: 'Courier New', monospace; }
    .data-label { color: #94a3b8; font-weight: bold; text-transform: uppercase; font-size: 0.85em; }
    .data-value { color: #f8fafc; margin-bottom: 10px; }
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
    # Identificación dinámica de columnas de control
    col_ub = [c for c in df.columns if 'UBICAC' in c.upper()][0]
    col_fe = [c for c in df.columns if 'FECHA' in c.upper()][0]
    
    # Barra Lateral
    st.sidebar.markdown("<h2 class='neon-text'>CONTROLES</h2>", unsafe_allow_html=True)
    sel_ub = st.sidebar.selectbox("📍 Seleccionar Kiosco", df[col_ub].unique())
    df_filtrado = df[df[col_ub] == sel_ub].sort_values(by=col_fe, ascending=False)
    sel_fe = st.sidebar.selectbox("📅 Fecha de Reporte", df_filtrado[col_fe].unique())
    reporte = df_filtrado[df_filtrado[col_fe] == sel_fe].iloc[0]

    st.markdown(f"<h1 class='neon-text'>SISTEMA DE GESTIÓN TOTAL: {sel_ub}</h1>", unsafe_allow_html=True)
    st.divider()

    # 1. BLOQUE VISUAL (Gráficos y Resumen)
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown('<div class="kiosco-card">', unsafe_allow_html=True)
        # Definimos qué columnas queremos ver en el gráfico (las de infraestructura)
        infra_esperada = ['DELANTERA', 'POSTERIOR', 'MUEBLES', 'ENERGIA', 'INTERNET', 'CABLEADO', 'CAMARAS SEGURIDAD', 'ILUMINACIÓN']
        infra_existente = [c for c in infra_esperada if c in df.columns]
        
        estados = [str(reporte.get(c, 'N/A')).upper() for c in infra_existente]
        fig = px.bar(x=infra_existente, y=[1]*len(infra_existente), color=estados,
                     title="Salud de Infraestructura Principal",
                     color_discrete_map={'PERFECTO': '#2ecc71', 'CON PROBLEMAS': '#f1c40f', 'NO FUNCIONA': '#e74c3c', 'SUCIO/ROTO': '#e67e22'})
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#f8fafc", height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        # Aquí mostramos columnas de "Identificación" (Nombre, Hora, etc.)
        st.subheader("📋 Información del Registro")
        columnas_usadas = [col_ub, col_fe] + infra_existente
        
        # Columnas de identificación típicas
        id_cols = ['ID', 'HORA DE INICIO', 'HORA DE FINALIZACIÓN', 'CORREO ELECTRÓNICO', 'NOMBRE', 'TU NOMBRE']
        for c in df.columns:
            if c.upper() in id_cols:
                st.markdown(f"<div class='data-label'>{c}</div><div class='data-value'>{reporte.get(c)}</div>", unsafe_allow_html=True)
                columnas_usadas.append(c)

    st.divider()

    # 2. BLOQUE DE "DATOS ADICIONALES" (Aquí capturamos todo lo demás del Excel)
    st.subheader("🔍 Detalle Completo de Campos")
    
    # Buscamos columnas que no hayan sido mostradas arriba y que no sean fotos
    fotos_cols = [c for c in df.columns if 'FOTO' in c.upper()]
    cols_restantes = [c for c in df.columns if c not in columnas_usadas and c not in fotos_cols]
    
    if cols_restantes:
        # Dividimos en 3 columnas para que sea fácil de leer
        filas = st.columns(3)
        for i, col in enumerate(cols_restantes):
            with filas[i % 3]:
                valor = reporte.get(col)
                if pd.notna(valor) and str(valor).strip() != "":
                    st.markdown(f"<div class='data-label'>{col}</div><div class='data-value'>{valor}</div>", unsafe_allow_html=True)
    
    st.divider()

    # 3. BLOQUE DE FOTOS
    if fotos_cols:
        st.subheader("📸 Evidencia Multimedia")
        for f_col in fotos_cols:
            links = str(reporte.get(f_col, ''))
            if "http" in links:
                st.write(f"**Archivo: {f_col}**")
                for link in links.split(';'):
                    st.image(link.strip(), use_container_width=True)
    
else:
    st.error("No se encontró el archivo de datos.")
