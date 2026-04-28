import streamlit as st
import pandas as pd
import glob

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Reporte de Inspección Kioscos IA", layout="wide")

# ESTILO PROFESIONAL INSPIRADO EN DOCUMENTO CORPORATIVO
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; color: #1e293b; }
    
    /* Encabezado de Sección Estilo Word */
    .section-header {
        background-color: #1e293b;
        color: #ffffff;
        padding: 10px 20px;
        font-family: 'Arial', sans-serif;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 15px;
        border-radius: 4px;
    }
    
    /* Fila de Datos */
    .data-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 15px;
        border-bottom: 1px solid #e2e8f0;
        background-color: #ffffff;
    }
    
    .data-label {
        font-weight: 600;
        color: #475569;
        width: 60%;
    }
    
    .data-value {
        width: 35%;
        text-align: right;
        font-weight: 500;
    }

    /* Colores de Estado */
    .status-ok { color: #16a34a; font-weight: bold; }
    .status-fail { color: #dc2626; font-weight: bold; }
    .status-neutral { color: #2563eb; }

    /* Contenedor de Observaciones */
    .obs-container {
        margin: 10px 0;
        padding: 15px;
        background-color: #f8fafc;
        border-left: 4px solid #cbd5e1;
        font-style: italic;
    }
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
    # Identificadores de ubicación y fecha
    col_ub = [c for c in df.columns if 'UBICAC' in c.upper()][0]
    col_fe = [c for c in df.columns if 'HORA' in c.upper() or 'FECHA' in c.upper()][0]
    
    # Sidebar de Navegación
    st.sidebar.header("Selección de Informe")
    sel_ub = st.sidebar.selectbox("Módulo / Ubicación", df[col_ub].unique())
    df_filtrado = df[df[col_ub] == sel_ub].sort_values(by=col_fe, ascending=False)
    sel_fe = st.sidebar.selectbox("Fecha y Hora", df_filtrado[col_fe].unique())
    reporte = df_filtrado[df_filtrado[col_fe] == sel_fe].iloc[0]

    # Encabezado Principal del Reporte
    st.title(f"Informe Técnico: {sel_ub}")
    st.caption(f"Registro oficial correspondiente al {sel_fe}")
    
    # --- DEFINICIÓN DE CATEGORÍAS (Basado en el orden del Word) ---
    categorias = {
        "1. INFRAESTRUCTURA Y EXTERIORES": [
            "DELANTERA", "POSTERIOR", "LATERAL IZQUIERDO", "LATERAL DERECHO", 
            "MUEBLES", "PINTURA", "LIMPIEZA", "FACHADA", "PUERTA"
        ],
        "2. COMPONENTES TÉCNICOS Y MAQUINARIA": [
            "ENERGIA", "INTERNET", "CABLEADO", "CAMARAS SEGURIDAD", 
            "ILUMINACIÓN", "LOCKERS", "SISTEMA SOLAR"
        ],
        "3. PANTALLAS Y UNIDADES DE PILOTO": [
            "TOTEM IZQUIERDO", "TOTEM DERECHO", "TV IZQUIERDO", "TV DERECHO", 
            "PILOTO IZQUIERDO", "COPILOTO DERECHO", "MONITOR"
        ]
    }

    columnas_ya_vistas = [col_ub, col_fe, 'ID', 'Hora de inicio', 'Hora de finalización', 'Correo electrónico', 'Nombre']
    foto_cols = [c for c in df.columns if 'FOTO' in c.upper() or 'IMAGEN' in c.upper()]

    # Renderizado siguiendo el orden del Word
    for titulo_sec, palabras_clave in categorias.items():
        # Filtramos las columnas que pertenecen a este bloque
        cols_en_bloque = [c for c in df.columns if any(k in c.upper() for k in palabras_clave) and c not in columnas_ya_vistas and c not in foto_cols]
        
        if cols_en_bloque:
            st.markdown(f'<div class="section-header">{titulo_sec}</div>', unsafe_allow_html=True)
            
            for col in cols_en_bloque:
                valor = str(reporte.get(col, 'N/A'))
                
                # Lógica de color según el valor
                clase_status = "status-neutral"
                if any(ok in valor.upper() for ok in ["OK", "PERFECTO", "BUENO"]): clase_status = "status-ok"
                elif any(err in valor.upper() for err in ["FALLA", "MALO", "REVISAR", "SUCIO"]): clase_status = "status-fail"
                
                st.markdown(f"""
                    <div class="data-row">
                        <div class="data-label">{col}</div>
                        <div class="data-value <span class='{clase_status}'>{valor}</span></div>
                    </div>
                """, unsafe_allow_html=True)
                columnas_ya_vistas.append(col)

            # Agregar observaciones específicas del bloque si existen
            obs_del_bloque = [c for c in df.columns if 'OBSERV' in c.upper() and any(k in c.upper() for k in titulo_sec.split())]
            for obs_col in obs_del_bloque:
                texto_obs = str(reporte.get(obs_col, '')).strip()
                if texto_obs.lower() not in ['nan', '', '.']:
                    st.markdown(f'<div class="obs-container"><b>Observaciones:</b> {texto_obs}</div>', unsafe_allow_html=True)
                    columnas_ya_vistas.append(obs_col)

    # --- SECCIÓN DE FOTOS (Visualización limpia) ---
    if foto_cols:
        st.markdown('<div class="section-header">4. REGISTRO FOTOGRÁFICO</div>', unsafe_allow_html=True)
        # Mostramos fotos en columnas de 2 para mantener tamaño grande tipo Word
        for i in range(0, len(foto_cols), 2):
            cols_img = st.columns(2)
            for idx, f_col in enumerate(foto_cols[i:i+2]):
                link = str(reporte.get(f_col, ''))
                if "http" in link:
                    with cols_img[idx]:
                        st.image(link.split(';')[0], caption=f_col, use_container_width=True)
                columnas_ya_vistas.append(f_col)

    # --- DATOS ADICIONALES (Cualquier columna que sobre) ---
    sobrantes = [c for c in df.columns if c not in columnas_ya_vistas]
    if sobrantes:
        with st.expander("Ver otros datos del sistema"):
            for s in sobrantes:
                val = reporte.get(s)
                if pd.notna(val):
                    st.write(f"**{s}:** {val}")

else:
    st.error("No se encontró el archivo .xlsx en la carpeta.")
