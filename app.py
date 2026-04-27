import streamlit as st
import pandas as pd
import glob
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Kioscos IA - Mantenimiento", layout="wide")

# Título con indicador de versión para saber si Streamlit se actualizó
st.title("📊 Estado de Infraestructura - Kioscos IA (Versión 5)")

# Eliminamos la memoria caché temporalmente para forzar lectura de datos frescos
def cargar_datos_limpios():
    archivos_csv = glob.glob("*.csv")
    if archivos_csv:
        # utf-8-sig elimina cualquier formato invisible de Microsoft Forms
        df = pd.read_csv(archivos_csv[0], encoding='utf-8-sig')
        # Limpiamos todos los nombres de columnas de espacios accidentales
        df.columns = df.columns.str.strip()
        return df
    return None

df = cargar_datos_limpios()

if df is not None:
    # Detectamos las columnas dinámicamente sin importar si tienen espacios o tildes raras
    col_ubicacion = [c for c in df.columns if 'UBICAC' in c.upper()][0]
    col_fecha = [c for c in df.columns if 'FECHA' in c.upper()][0]
    
    # --- BARRA LATERAL ---
    st.sidebar.header("Filtros de Inspección")
    
    ubicaciones = df[col_ubicacion].dropna().unique()
    kiosco_sel = st.sidebar.selectbox("📍 Seleccionar Ubicación:", ubicaciones)
    
    df_kiosco = df[df[col_ubicacion] == kiosco_sel].sort_values(by=col_fecha, ascending=False)
    fechas = df_kiosco[col_fecha].dropna().unique()
    
    if len(fechas) > 0:
        fecha_sel = st.sidebar.selectbox("📅 Seleccionar Fecha de Reporte:", fechas)
        reporte = df_kiosco[df_kiosco[col_fecha] == fecha_sel].iloc[0]

        st.markdown(f"**Fecha del reporte:** {fecha_sel}")
        
        col_graf, col_met = st.columns([1, 2])
        
        # Buscar columnas principales de infraestructura
        infra_cols_esperadas = ['DELANTERA', 'POSTERIOR', 'MUEBLES', 'CABLEADO', 'ENERGIA', 'INTERNET', 'CAMARAS SEGURIDAD']
        infra_cols = [c for c in infra_cols_esperadas if c in df.columns]
        
        estados_actuales = [str(reporte.get(c, 'NO EVALUADO')).upper() for c in infra_cols]
        df_resumen = pd.DataFrame({'Componente': infra_cols, 'Estado': estados_actuales})
        
        with col_graf:
            if not df_resumen.empty:
                fig = px.pie(df_resumen, names='Estado', title="Salud del Kiosco",
                             color='Estado', color_discrete_map={
                                 'PERFECTO': '#2ecc71', 
                                 'CON PROBLEMAS': '#f1c40f', 
                                 'NO FUNCIONA': '#e74c3c',
                                 'SUCIO/ROTO': '#e67e22',
                                 'NO EVALUADO': '#95a5a6'
                             }, hole=0.6)
                st.plotly_chart(fig, use_container_width=True)

        with col_met:
            st.subheader("🛠️ Detalle de Componentes")
            for c in infra_cols:
                val = str(reporte.get(c)).upper().strip()
                if val == "PERFECTO":
                    st.success(f"**{c}:** OK")
                elif val in ["CON PROBLEMAS", "SUCIO/ROTO"]:
                    st.warning(f"**{c}:** {val}")
                elif val == "NO FUNCIONA":
                    st.error(f"**{c}:** {val}")
                else:
                    st.write(f"**{c}:** No evaluado")

        st.divider()
        
        # Búsqueda dinámica de las observaciones
        obs_col = [c for c in df.columns if 'OBSERVACIONES' in c.upper()]
        if obs_col:
            st.subheader("📝 Observaciones del Personal")
            st.info(reporte.get(obs_col[-1], 'Sin observaciones reportadas.'))
    else:
        st.warning("No hay reportes con fechas válidas para esta ubicación.")
else:
    st.error("⚠️ No se encontró el archivo CSV en la carpeta.")
