import streamlit as st
import pandas as pd
import glob

# Configuración visual de la página
st.set_page_config(page_title="Visor de Kioscos IA", layout="wide")

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

if df is None:
    st.error("⚠️ No se encontró el archivo de datos.")
    st.stop()

# --- DISEÑO DEL VISUALIZADOR ---

st.title("📱 Visor de Estado por Kiosco")
st.markdown("Selecciona una ubicación para ver el estado detallado de su infraestructura.")

# 1. Selector principal
kioscos_disponibles = df["UBICACIÓN DEL MODULO"].dropna().unique()
kiosco_seleccionado = st.selectbox("🎯 Elige el Kiosco a revisar:", kioscos_disponibles)

# Filtrar datos del kiosco seleccionado
df_kiosco = df[df["UBICACIÓN DEL MODULO"] == kiosco_seleccionado].copy()

# Tomar el reporte más reciente (la última fila de ese kiosco)
ultimo_reporte = df_kiosco.iloc[-1]

st.header(f"📍 {kiosco_seleccionado}")
st.caption(f"📅 Fecha del último reporte registrado: {ultimo_reporte.get('FECHA', 'No disponible')}")
st.divider()

# Función para convertir el texto en indicadores visuales
def estado_visual(valor):
    valor = str(valor).upper().strip()
    if valor == "PERFECTO": return "🟢 Perfecto"
    if valor == "CON PROBLEMAS": return "🟡 Con Problemas"
    if valor in ["NO FUNCIONA", "SUCIO/ROTO"]: return f"🔴 {valor}"
    if valor == "NAN": return "⚪ No evaluado"
    return f"⚪ {valor}"

# 2. Tarjetas visuales por áreas
st.subheader("Estado de Componentes")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🚪 Puertas y Estructura")
    st.write(f"**Delantera:** {estado_visual(ultimo_reporte.get('DELANTERA'))}")
    st.write(f"**Posterior:** {estado_visual(ultimo_reporte.get('POSTERIOR'))}")
    st.write(f"**Muebles:** {estado_visual(ultimo_reporte.get('MUEBLES'))}")
    st.info(f"📝 Observaciones: {ultimo_reporte.get('OBSERVACIONES PUERTAS', 'Ninguna')}")

with col2:
    st.markdown("### 🖥️ Pantallas")
    st.write(f"**Totem Izq:** {estado_visual(ultimo_reporte.get('TOTEM IZQUIERDO'))}")
    st.write(f"**Totem Der:** {estado_visual(ultimo_reporte.get('TOTEM DERECHO'))}")
    st.write(f"**TV Izq:** {estado_visual(ultimo_reporte.get('TV IZQUIERDO'))}")
    st.write(f"**TV Der:** {estado_visual(ultimo_reporte.get('TV DERECHO'))}")
    st.info(f"📝 Observaciones: {ultimo_reporte.get('OBSERVACIONES PANTALLAS', 'Ninguna')}")

with col3:
    st.markdown("### 🔌 Conectividad y Energía")
    st.write(f"**Energía:** {estado_visual(ultimo_reporte.get('ENERGIA'))}")
    st.write(f"**Internet:** {estado_visual(ultimo_reporte.get('INTERNET'))}")
    st.write(f"**Cámaras:** {estado_visual(ultimo_reporte.get('CAMARAS SEGURIDAD'))}")
    st.write(f"**Lockers:** {estado_visual(ultimo_reporte.get('LOCKERS'))}")
    st.info(f"📝 Observaciones: {ultimo_reporte.get('OBSERVACIONES OTROS', 'Ninguna')}")

st.divider()

# 3. Observaciones Generales del Técnico
st.markdown("### 📋 Diagnóstico General de la Visita")
comentario_general = ultimo_reporte.get('DESCRIBA SUS OBSERVACIONES GENERALES LUEGO DE LA VISITA. PUEDE AMPLIAR O AGREGAR INFORMACIÓN', 'No hay comentarios adicionales.')
st.success(comentario_general)
