import streamlit as st
import pandas as pd
import glob

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Kioscos IA - Reporte Completo", layout="wide")

# Estilo Neón para máxima visibilidad
st.markdown("""
    <style>
    .stApp { background-color: #030712; color: #f8fafc; }
    .main-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .neon-title { color: #00d4ff; text-shadow: 0 0 10px rgba(0, 212, 255, 0.3); font-family: 'Poppins'; }
    .data-card {
        background: #1e293b;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #334155;
        height: 100%;
    }
    .label-text { color: #94a3b8; font-size: 0.8em; font-weight: bold; text-transform: uppercase; }
    .value-text { color: #f8fafc; font-size: 1.1em; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=30)
def cargar_datos():
    archivos = glob.glob("*.xlsx")
    if not archivos: return None
    df = pd.read_excel(archivos[0])
    df.columns = df.columns.str.strip()
    return df

df = cargar_datos()

if df is not None:
    # Identificar columnas de ubicación y fecha (indispensables para filtrar)
    col_ub = [c for c in df.columns if 'UBICAC' in c.upper()][0]
    col_fe = [c for c in df.columns if 'HORA' in c.upper() or 'FECHA' in c.upper()][0]
    
    # Sidebar
    st.sidebar.markdown("<h2 style='color:#00d4ff;'>PANEL DE CONTROL</h2>", unsafe_allow_html=True)
    sel_ub = st.sidebar.selectbox("Seleccionar Kiosco", df[col_ub].unique())
    df_filtrado = df[df[col_ub] == sel_ub].sort_values(by=col_fe, ascending=False)
    sel_fe = st.sidebar.selectbox("Seleccionar Reporte", df_filtrado[col_fe].unique())
    reporte = df_filtrado[df_filtrado[col_fe] == sel_fe].iloc[0]

    st.markdown(f"<h1 class='neon-title'>REPORTE INTEGRAL: {sel_ub}</h1>", unsafe_allow_html=True)
    st.markdown(f"**Fecha y Hora del Registro:** {sel_fe}")
    st.divider()

    # --- RENDERIZADO DE TODAS LAS CELDAS SIN EXCEPCIÓN ---
    
    # Separamos fotos para el final por estética
    foto_cols = [c for c in df.columns if 'FOTO' in c.upper() or 'IMAGEN' in c.upper()]
    info_cols = [c for c in df.columns if c not in foto_cols]

    # Mostramos toda la información de texto/estado en una rejilla dinámica
    st.subheader("📋 Datos Detallados del Formulario")
    
    # Creamos filas de 4 columnas para que quepan todos los datos
    for i in range(0, len(info_cols), 4):
        cols = st.columns(4)
        for idx, col_name in enumerate(info_cols[i:i+4]):
            with cols[idx]:
                valor = reporte.get(col_name)
                # Solo mostramos si no está vacío
                if pd.notna(valor) and str(valor).strip() != "":
                    st.markdown(f"""
                        <div class="data-card">
                            <div class="label-text">{col_name}</div>
                            <div class="value-text">{valor}</div>
                        </div>
                    """, unsafe_allow_html=True)
        st.write("") # Espaciador

    st.divider()

    # --- SECCIÓN DE FOTOS ---
    if foto_cols:
        st.subheader("📸 Evidencia Fotográfica")
        for f_col in foto_cols:
            link = str(reporte.get(f_col, ''))
            if "http" in link:
                st.markdown(f"**{f_col}**")
                # Manejo de múltiples fotos separadas por ';'
                for img_url in link.split(';'):
                    if img_url.strip():
                        st.image(img_url.strip(), use_container_width=True)
    
else:
    st.error("⚠️ No se encontró el archivo Excel (.xlsx) en la carpeta del proyecto.")
