import streamlit as st
import pandas as pd
import glob
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Dashboard Kioscos IA", layout="wide")

@st.cache_data
def cargar_datos():
    archivos_csv = glob.glob("*.csv")
    archivos_excel = glob.glob("*.xlsx")
    
    df = None
    try:
        if archivos_csv:
            # Intenta leer con soporte para tildes (utf-8) y si falla usa el estándar de Excel (latin1)
            try:
                df = pd.read_csv(archivos_csv[0], encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(archivos_csv[0], encoding='latin1')
        elif archivos_excel:
            df = pd.read_excel(archivos_excel[0])
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return None
        
    if df is not None:
        # Limpieza extrema: quitar espacios invisibles y poner todo en mayúsculas
        df.columns = df.columns.str.strip().str.upper()
        
        # Búsqueda dinámica de las columnas clave (evita errores de tildes o espacios)
        for col in df.columns:
            if 'UBICA' in col and 'MODULO' in col:
                df.rename(columns={col: 'UBICACIÓN DEL MODULO'}, inplace=True)
            if 'FECHA' in col:
                df.rename(columns={col: 'FECHA'}, inplace=True)
                
    return df

df = cargar_datos()

if df is not None:
    # Verificación de seguridad
    if 'UBICACIÓN DEL MODULO' not in df.columns or 'FECHA' not in df.columns:
        st.error("⚠️ El archivo cargó, pero no se encontraron las columnas correctas. Columnas detectadas: " + ", ".join(df.columns))
        st.stop()
        
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
        
        reporte = df_kiosco[df_kiosco["FECHA"] == fecha_sel].iloc[0]

        # --- PANEL PRINCIPAL ---
        st.title(f"📊 Estado de Infraestructura: {kiosco_sel}")
        st.markdown(f"**Fecha del reporte:** {fecha_sel}")
        
        col_graf, col_met = st.columns([1, 2])
        
        infra_cols = ['DELANTERA', 'POSTERIOR', 'MUEBLES', 'CABLEADO', 'ENERGIA', 'INTERNET', 'CAMARAS SEGURIDAD']
        estados_actuales = [str(reporte.get(c, 'NO EVALUADO')).upper() for c in infra_cols]
        df_resumen = pd.DataFrame({'Componente': infra_cols, 'Estado': estados_actuales})
        
        with col_graf:
            fig = px.pie(df_resumen, names='Estado', title="Distribución de Estados",
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
            
            c1, c2, c3 = st.columns(3)
            
            areas = {
                "Estructura": ['DELANTERA', 'POSTERIOR', 'MUEBLES'],
                "Sistemas": ['ENERGIA', 'INTERNET', 'CABLEADO'],
                "Seguridad": ['CAMARAS SEGURIDAD', 'LOCKERS']
            }
            
            def mostrar_estado(label, val):
                val = str(val).upper().strip()
                if val == "PERFECTO": st.success(f"**{label}:** OK")
                elif val == "CON PROBLEMAS": st.warning(f"**{label}:** Advertencia")
                elif val in ["NAN", "NONE"]: st.write(f"**{label}:** No evaluado")
                else: st.error(f"**{label}:** {val}")

            with c1:
                st.markdown("**Fachada**")
                for item in areas["Estructura"]: mostrar_estado(item, reporte.get(item))
            with c2:
                st.markdown("**Conectividad**")
                for item in areas["Sistemas"]: mostrar_estado(item, reporte.get(item))
            with c3:
                st.markdown("**Otros**")
                for item in areas["Seguridad"]: mostrar_estado(item, reporte.get(item))

        st.divider()
        
        st.subheader("📝 Observaciones del Personal")
        
        # Búsqueda dinámica de la columna de observaciones
        obs_col = [c for c in df.columns if 'OBSERVACIONES GENERALES' in c]
        obs_key = obs_col[0] if obs_col else 'DESCRIBA SUS OBSERVACIONES GENERALES LUEGO DE LA VISITA. PUEDE AMPLIAR O AGREGAR INFORMACIÓN'
        obs = reporte.get(obs_key, 'Sin observaciones reportadas.')
        
        st.info(obs)
    else:
        st.warning("No hay reportes con fechas válidas para esta ubicación.")
else:
    st.error("⚠️ No se encontró el archivo de datos.")
