import streamlit as st
import pandas as pd
import glob
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Dashboard Kioscos IA", layout="wide", initial_sidebar_state="expanded")

# Estilo personalizado para las tarjetas (Métrica)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 24px; color: #00d4ff; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

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
    
    # Identificar columnas
    col_ub = [c for c in df.columns if 'UBICAC' in c.upper()][0]
    col_fe = [c for c in df.columns if 'FECHA' in c.upper()][0]
    col_nom = [c for c in df.columns if 'NOMBRE' in c.upper() or 'TU NOMBRE' in c.upper()][0]

    # --- SIDEBAR ---
    st.sidebar.image("https://via.placeholder.com/150?text=Kioscos+IA", width=100) # Aquí podrías poner tu logo
    st.sidebar.title("Panel de Control")
    
    sel_ub = st.sidebar.selectbox("📍 Ubicación", df[col_ub].unique())
    df_filtrado = df[df[col_ub] == sel_ub].sort_values(by=col_fe, ascending=False)
    
    sel_fe = st.sidebar.selectbox("📅 Fecha de Reporte", df_filtrado[col_fe].unique())
    reporte = df_filtrado[df_filtrado[col_fe] == sel_fe].iloc[0]

    # --- CUERPO PRINCIPAL ---
    st.title("🖥️ Monitor de Infraestructura")
    
    # Fila de Indicadores (Tarjetas como en la imagen)
    m1, m2, m3 = st.columns(3)
    m1.metric("Módulo Seleccionado", sel_ub)
    m2.metric("Inspector", reporte[col_nom])
    m3.metric("Fecha", str(sel_fe))

    st.divider()

    # Layout de dos columnas para Gráfico y Detalles
    c1, c2 = st.columns([1.2, 2])

    with c1:
        st.subheader("📊 Estado de Salud")
        items = ['DELANTERA', 'POSTERIOR', 'MUEBLES', 'CABLEADO', 'ENERGIA', 'INTERNET', 'CAMARAS SEGURIDAD']
        infra_cols = [c for c in items if c in df.columns]
        estados = [str(reporte.get(c, 'N/A')).upper() for c in infra_cols]
        
        fig = px.pie(names=estados, values=[1]*len(estados), hole=0.7,
                     color=estados, color_discrete_map={
                         'PERFECTO': '#00CC96', 'CON PROBLEMAS': '#EF553B', 
                         'SUCIO/ROTO': '#AB63FA', 'NO FUNCIONA': '#FFA15A'
                     })
        fig.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("🛠️ Checklist Técnico")
        cols_check = st.columns(2)
        for i, c in enumerate(infra_cols):
            val = str(reporte.get(c)).upper()
            target_col = cols_check[0] if i % 2 == 0 else cols_check[1]
            if "PERFECTO" in val: target_col.success(f"✅ {c}")
            else: target_col.error(f"⚠️ {c}: {val}")

    st.divider()

    # Sección de Observaciones y Fotos (Abajo para que respire el diseño)
    o1, o2 = st.columns(2)
    
    with o1:
        st.subheader("📝 Observaciones Detalladas")
        all_obs = [c for c in df.columns if 'OBSERVACIONES' in c.upper()]
        for obs in all_obs:
            txt = str(reporte.get(obs, '')).strip()
            if txt.lower() not in ['nan', '', 'none', '.']:
                st.info(f"**{obs}:**\n\n{txt}")

    with o2:
        st.subheader("📸 Evidencia")
        col_f = [c for c in df.columns if 'FOTO' in c.upper()]
        if col_f:
            links = str(reporte.get(col_f[0], ''))
            if "http" in links:
                for link in links.split(';'):
                    st.markdown(f"[🔗 Ver Fotografía Directa]({link.strip()})")
            else: st.write("No hay fotos disponibles.")

else:
    st.error("Esperando archivo de datos...")
