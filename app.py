import streamlit as st
import pandas as pd
import glob
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Kioscos IA - Mantenimiento", layout="wide")

st.title("📊 Estado de Infraestructura - Kioscos IA (Versión 7)")

def cargar_datos_limpios():
    archivos_excel = glob.glob("*.xlsx")
    archivos_csv = glob.glob("*.csv")
    
    df = None
    try:
        if archivos_excel:
            df = pd.read_excel(archivos_excel[0])
        elif archivos_csv:
            df = pd.read_csv(archivos_csv[0], encoding='utf-8-sig')
            
        if df is not None:
            df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        
    return df

df = cargar_datos_limpios()

if df is not None:
    col_ubicacion = [c for c in df.columns if 'UBICAC' in c.upper()][0]
    col_fecha = [c for c in df.columns if 'FECHA' in c.upper()][0]
    
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
        
        # --- OBSERVACIONES GENERALES ---
        obs_col = [c for c in df.columns if 'OBSERVACIONES' in c.upper()]
        if obs_col:
            st.subheader("📝 Observaciones del Personal")
            st.info(reporte.get(obs_col[-1], 'Sin observaciones reportadas.'))

        st.divider()

        # --- SECCIÓN DE FOTOGRAFÍAS ---
        st.subheader("📸 Evidencia Fotográfica")
        col_fotos = [c for c in df.columns if 'FOTO' in c.upper()]
        
        if col_fotos:
            fotos_str = str(reporte.get(col_fotos[0], ''))
            # Comprobamos que existan fotos adjuntas
            if fotos_str.lower() not in ['nan', 'none', '']:
                # Separamos los enlaces por el punto y coma
                urls = [url.strip() for url in fotos_str.split(';') if url.strip()]
                
                if urls:
                    st.write(f"Se encontraron **{len(urls)} foto(s)** para este reporte:")
                    cols_img = st.columns(min(len(urls), 3)) # Máximo 3 columnas para organizar
                    
                    for i, url in enumerate(urls):
                        with cols_img[i % 3]:
                            # 1. Enlace seguro en caso de bloqueo de Microsoft
                            st.markdown(f"**[🔍 Clic para abrir Foto {i+1} en pantalla completa]({url})**")
                            # 2. Intento de previsualización en el panel
                            try:
                                st.image(url, use_container_width=True)
                            except:
                                st.caption("Previsualización protegida por Microsoft. Usa el enlace de arriba.")
            else:
                st.write("No se adjuntaron fotografías en esta inspección.")
        else:
            st.write("Columna de fotos no detectada en la base de datos.")

    else:
        st.warning("No hay reportes con fechas válidas para esta ubicación.")
else:
    st.error("⚠️ No se encontró ningún archivo Excel (.xlsx) ni CSV (.csv) en GitHub.")
