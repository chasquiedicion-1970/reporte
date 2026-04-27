import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Dashboard Mantenimiento - Kioscos IA", layout="wide")
st.title("🛠️ Panel de Mantenimiento y Supervisión - Kioscos IA")

# 1. Cargar los datos
@st.cache_data
def cargar_datos():
    # Asegúrate de que el archivo CSV o Excel esté en la misma carpeta
    # Si es Excel, cambia read_csv por read_excel
    df = pd.read_csv("REPORTE INCIDENCIAS MODULOS(1-21).xlsx - Sheet1.csv")
    return df

df = cargar_datos()

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
# Agrupamos las columnas de infraestructura para buscar errores
columnas_infra = ['PILOTO IZQUIERDO', 'COPILOTO DERECHO', 'DELANTERA', 'POSTERIOR', 
                  'MUEBLES', 'CABLEADO', 'ENERGIA', 'ILUMINACIÓN', 'INTERNET', 
                  'WI FI GRATUITO', 'LOCKERS', 'CAMARAS SEGURIDAD']

# 4. Tarjetas de Resumen (Métricas)
st.subheader("Resumen de Estado Operativo")
col1, col2, col3 = st.columns(3)

total_reportes = len(df_filtrado)
# Contar reportes que tengan algún "NO FUNCIONA" o "CON PROBLEMAS"
reportes_criticos = df_filtrado[df_filtrado.isin(['NO FUNCIONA', 'SUCIO/ROTO']).any(axis=1)].shape[0]
reportes_advertencia = df_filtrado[df_filtrado.isin(['CON PROBLEMAS']).any(axis=1)].shape[0]

col1.metric("Total de Reportes Revisados", total_reportes)
col2.metric("Kioscos en Estado CRÍTICO 🔴", reportes_criticos)
col3.metric("Kioscos con Advertencias 🟡", reportes_advertencia)

st.divider()

# 5. Lista de Acción: Infraestructura que requiere mantenimiento
st.subheader("📋 Lista de Incidentes para Solucionar")

# Creamos una tabla limpia solo con las fallas
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
    
    # Colorear según gravedad
    def color_estado(val):
        if val in ['NO FUNCIONA', 'SUCIO/ROTO']:
            return 'background-color: #ffcccc; color: #990000' # Rojo
        elif val == 'CON PROBLEMAS':
            return 'background-color: #fff0b3; color: #997300' # Amarillo
        return ''
    
    st.dataframe(df_fallas.style.map(color_estado, subset=['Estado']), use_container_width=True)
else:
    st.success("¡Excelente! No se encontraron problemas de infraestructura en la selección actual. Todos los sistemas están en estado PERFECTO.")

st.divider()

# 6. Tabla Completa de Observaciones
with st.expander("Ver Base de Datos Completa de Observaciones de Kioscos"):
    st.dataframe(df_filtrado)