import streamlit as st
import pandas as pd
import glob
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Dashboard Integral Kioscos IA", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: #f8fafc; }
    .category-box {
        background-color: #0f172a;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 30px;
        border: 1px solid #1e293b;
    }
    .neon-header { color: #00d4ff; text-shadow: 0 0 10px rgba(0, 212, 255, 0.3); font-family: 'Poppins'; border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 20px; }
    .obs-box { background-color: rgba(0, 212, 255, 0.05); border-left: 3px solid #00d4ff; padding: 10px 15px; margin-top: 15px; font-style: italic; font-size: 0.95em; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def cargar_datos():
    archivos = glob.glob("*.xlsx") + glob.glob("*.csv")
    if not archivos: return None
    try:
        df = pd.read_excel(archivos[0]) if archivos[0].endswith('.xlsx') else pd.read_csv(archivos[0], encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        return df
    except: return None

df = cargar_datos()

if df is not None:
    col_ub = [c for c in df.columns if 'UBICAC' in c.upper()][0]
    col_fe = [c for c in df.columns if 'FECHA' in c.upper()][0]
    
    # Barra Lateral
    st.sidebar.title("📊 Panel de Control")
    sel_ub = st.sidebar.selectbox("📍 Ubicación", df[col_ub].unique())
    df_filtrado = df[df[col_ub] == sel_ub].sort_values(by=col_fe, ascending=False)
    sel_fe = st.sidebar.selectbox("📅 Reporte", df_filtrado[col_fe].unique())
    reporte = df_filtrado[df_filtrado[col_fe] == sel_fe].iloc[0]

    st.markdown(f"<h1 style='color:#00d4ff;'>Reporte Maestro: {sel_ub}</h1>", unsafe_allow_html=True)
    
    # --- MAPEADO DE CATEGORÍAS ---
    # Definimos los campos de estado y sus observaciones relacionadas
    estructuras = {
        "🏗️ INFRAESTRUCTURA": {
            "estados": ['DELANTERA', 'POSTERIOR', 'MUEBLES', 'PINTURA', 'LIMPIEZA'],
            "notas": ['OBSERVACIONES PUERTAS', 'OBSERVACIONES ESTRUCTURA']
        },
        "🤖 MAQUINARIA Y SISTEMAS": {
            "estados": ['ENERGIA', 'INTERNET', 'CABLEADO', 'CAMARAS SEGURIDAD', 'LOCKERS', 'ILUMINACIÓN'],
            "notas": ['OBSERVACIONES OTROS', 'OBSERVACIONES TÉCNICAS']
        },
        "🖥️ PANTALLAS Y MULTIMEDIA": {
            "estados": ['TOTEM IZQUIERDO', 'TOTEM DERECHO', 'TV IZQUIERDO', 'TV DERECHO'],
            "notas": ['OBSERVACIONES PANTALLAS']
        }
    }

    columnas_mostradas = [col_ub, col_fe, 'TU NOMBRE', 'ID', 'HORA DE INICIO', 'HORA DE FINALIZACIÓN', 'CORREO ELECTRÓNICO']

    # Renderizado Dinámico
    for titulo, contenido in estructuras.items():
        st.markdown(f"<div class='category-box'><h2 class='neon-header'>{titulo}</h2>", unsafe_allow_html=True)
        
        # Mostrar Estados (Checks)
        checks = [c for c in contenido["estados"] if c in df.columns]
        if checks:
            cols = st.columns(len(checks))
            for i, c in enumerate(checks):
                val = str(reporte.get(c, 'N/A')).upper()
                with cols[i]:
                    st.write(f"**{c}**")
                    if "PERFECTO" in val or "OK" in val: st.success("🟢 OK")
                    else: st.warning(f"⚠️ {val}")
                columnas_mostradas.append(c)

        # Mostrar Observaciones de esta categoría
        notas = [n for n in contenido["notas"] if n in df.columns]
        for n in notas:
            txt = str(reporte.get(n, '')).strip()
            if txt.lower() not in ['nan', '', 'none', '.']:
                st.markdown(f"<div class='obs-box'><b>Nota de {titulo.lower()}:</b><br>{txt}</div>", unsafe_allow_html=True)
                columnas_mostradas.append(n)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- SECCIÓN DE "MÁS CELDAS" (PARA NO OMITIR NADA) ---
    foto_cols = [c for c in df.columns if 'FOTO' in c.upper()]
    otros_cols = [c for c in df.columns if c not in columnas_usadas and c not in foto_cols]
    
    if otros_cols:
        with st.expander("➕ Ver celdas adicionales y detalles de registro"):
            c1, c2 = st.columns(2)
            for i, col in enumerate(otros_cols):
                target = c1 if i % 2 == 0 else c2
                val = reporte.get(col)
                if pd.notna(val) and str(val).strip() != "":
                    target.write(f"**{col}:** {val}")

    # --- FOTOS AL FINAL ---
    if foto_cols:
        st.subheader("📸 Evidencia Fotográfica")
        for f in foto_cols:
            links = str(reporte.get(f, ''))
            if "http" in links:
                for link in links.split(';'):
                    st.image(link.strip(), caption=f"Evidencia: {f}", use_container_width=True)

else:
    st.error("Esperando archivo de datos...")
