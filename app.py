import streamlit as st
import pandas as pd
import glob

# Configuración de la página
st.set_page_config(page_title="Dashboard Mantenimiento - Kioscos IA", layout="wide")
st.title("🛠️ Panel de Mantenimiento y Supervisión - Kioscos IA")

# 1. Cargar los datos automáticamente sin pedir el nombre exacto
@st.cache_data
def cargar_datos():
    archivos_csv = glob.glob("*.csv")
    archivos_excel = glob.glob("*.xlsx")
    
    if archivos_csv:
        return pd.read_csv(archivos_csv[0])
    elif archivos_excel:
        return pd.read_excel(archivos_excel[0])
    else:
        return None

df = cargar_datos()

# Si no encuentra nada, avisa
if df is None:
    st.error("⚠️ No se encontró el archivo de datos. Asegúrate de haber subido el archivo con los reportes a GitHub.")
    st.stop()

# 2. Barra lateral para filtros
st.sidebar.header("Filtros de Búsqueda")
ubicacion = st.sidebar.multiselect(
    "Selecciona el Kiosco / Ubicación:",
    options=df["UBICACIÓN DEL MODULO"].dropna().unique()
)

# Aplicar filtro
if ubicacion:
    df_filtrado = df[df["UBICACIÓN DEL MODULO"].isin(ubicacion)]
else:
    df_filtrado = df

# 3. Transformar los datos para identificar problemas rápidamente
columnas_infra = ['PILOTO IZQUIERDO', 'COPILOTO DERECHO', 'DELANTERA', 'POSTERIOR', 
                  'MUEBLES', 'CABLEADO', 'ENERGIA', 'ILUMINACIÓN', 'INTERNET', 
                  'WI FI GRATUITO', 'LOCKERS', 'CAMARAS SEGURIDAD']

# 4. Tarjetas de Resumen (Métricas)
st.subheader("Resumen de Estado Operativo")
col1, col2, col3 = st.columns(3)

total_reportes = len(df_filtrado)
reportes_criticos = df_filtrado[df_filtrado.isin(['NO FUNCIONA', 'SUCIO/ROTO']).any(axis=1)].shape[0]
reportes_advertencia = df_filtrado[df_filtrado.isin(['CON PROBLEMAS']).any(axis=1)].shape[0]

col1.metric("Total de Reportes Revisados", total_reportes)
col2.metric("Kioscos en Estado CRÍTICO 🔴", reportes_criticos)
col3.metric("Kioscos con Advertencias 🟡", reportes_advertencia)

st.divider()

# 5. Lista de Acción
st.subheader("📋 Lista de Incidentes para Solucionar")

fallas = []
for index, row in df_filtrado.iterrows():
    for col in columnas_infra:
        estado = str(row.get(col, ""))
        if estado in ['CON PROBLEMAS', 'NO FUNCIONA', 'SUCIO/ROTO']:
            fallas.append({
                "Fecha": row.get("FECHA", ""),
                "Ubicación": row.get("UBICACIÓN DEL MODULO", ""),
                "Componente": col,
                "Estado": estado,
                "Observación Gral": row.get("DESCRIBA SUS OBSERVACIONES GENERALES LUEGO DE LA VISITA. PUEDE AMPLIAR O AGREGAR INFORMACIÓN", "")
            })

if fallas:
    df_fallas = pd.DataFrame(fallas)
    
    def color_estado(val):
        if val in ['NO FUNCIONA', 'SUCIO/ROTO']:
            return 'background-color: #ffcccc; color: #990000' 
        elif val == 'CON PROBLEMAS':
            return 'background-color: #fff0b3; color: #997300' 
        return ''
    
    st.dataframe(df_fallas.style.map(color_estado, subset=['Estado']), use_container_width=True)
else:
    st.success("¡Excelente! No se encontraron problemas de infraestructura en la selección actual.")

st.divider()

# 6. Tabla Completa
with st.expander("Ver Base de Datos Completa de Observaciones de Kioscos"):
    st.dataframe(df_filtrado)
