import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Dashboard Kioscos IA", layout="wide")

# Tu enlace de Microsoft 365 con la terminación para descarga directa
URL_365 = "https://kiscosia-my.sharepoint.com/:x:/g/personal/gerencia_comunicaciones_kioscosia_com/IQAdKGGmLFJWRKaaAfsAGtqtARwthzhAF0cuds4Yuz_tDlk?download=1" 

@st.cache_data(ttl=300) # El sistema actualizará los datos nuevos cada 5 minutos
def cargar_datos(url):
    try:
        return pd.read_excel(url)
    except Exception as e:
        st.error("⚠️ No se pudo conectar con el Excel. Asegúrate de que el enlace sea público ('Cualquier persona con el vínculo puede ver').")
        st.stop()

df = cargar_datos(URL_365)

if df is not None:
    # Asegurar que la fecha sea válida
    df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce').dt.date
    
    # --- BARRA LATERAL ---
    st.sidebar.header("Filtros de Inspección")
    
    # 1. Selector de Kiosco
    ubicaciones = df["UBICACIÓN DEL MODULO"].dropna().unique()
    kiosco_sel = st.sidebar.selectbox("📍 Seleccionar Ubicación:", ubicaciones)
    
    # 2. Selector de Fecha
    df_kiosco = df[df["UBICACIÓN DEL MODULO"] == kiosco_sel].sort_values(by="FECHA", ascending=False)
    fechas = df_kiosco["FECHA"].dropna().unique()
    
    if len(fechas) > 0:
        fecha_sel = st.sidebar.selectbox("📅 Seleccionar Fecha de Reporte:", fechas)
        
        # Filtrar el reporte específico
        reporte = df_kiosco[df_kiosco["FECHA"] == fecha_sel].iloc[0]

        # --- PANEL PRINCIPAL ---
        st.title(f"📊 Estado de Infraestructura: {kiosco_sel}")
        st.markdown(f"**Fecha del reporte:** {fecha_sel}")
        
        # Gráfico de Salud General
        col_graf, col_met = st.columns([1, 2])
        
        infra_cols = ['DELANTERA', 'POSTERIOR', 'MUEBLES', 'CABLEADO', 'ENERGIA', 'INTERNET', 'CAMARAS SEGURIDAD']
        estados_actuales = [str(reporte.get(c)).upper() for c in infra_cols]
        df_resumen = pd.DataFrame({'Componente': infra_cols, 'Estado': estados_actuales})
        
        with col_graf:
            fig = px.pie(df_resumen, names='Estado', title="Distribución de Estados",
                         color='Estado', color_discrete_map={
                             'PERFECTO': '#2ecc71', 
                             'CON PROBLEMAS': '#f1c40f',
