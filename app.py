import streamlit as st
import pandas as pd
import glob

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Reporte Ejecutivo Kioscos IA", layout="wide")

# ESTILO CSS PARA REPLICAR DOCUMENTO FORMAL
st.markdown("""
    <style>
    .stApp { background-color: #030712; color: #cbd5e1; }
    .report-section {
        background-color: #0f172a;
        padding: 30px;
        border-radius: 10px;
        border-left: 5px solid #00d4ff;
        margin-bottom: 25px;
        line-height: 1.6;
    }
    .report-header { 
        color: #00d4ff; 
        font-family: 'Poppins', sans-serif;
        font-size: 1.5em;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .highlight-ok { color: #2ecc71; font-weight: bold; }
    .highlight-fail { color: #e74c3c; font-weight: bold; }
    .label-bold { color: #f8fafc; font-weight: 600; }
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
    # Identificadores
    col_ub = [c for c in df.columns if 'UBICAC' in c.upper()][0]
    col_fe = [c for c in df.columns if 'HORA' in c.upper() or 'FECHA' in c.upper()][0]
    
    # Sidebar
    st.sidebar.markdown("<h2 style='color:#00d4ff;'>AUDITORÍA</h2>", unsafe_allow_html=True)
    sel_ub = st.sidebar.selectbox("Seleccionar Módulo", df[col_ub].unique())
    df_filtrado = df[df[col_ub] == sel_ub].sort_values(by=col_fe, ascending=False)
    sel_fe = st.sidebar.selectbox("Fecha del Informe", df_filtrado[col_fe].unique())
    reporte = df_filtrado[df_filtrado[col_fe] == sel_fe].iloc[0]

    st.markdown(f"<h1 style='color:#f8fafc;'>INFORME DE INSPECCIÓN TÉCNICA: {sel_ub}</h1>", unsafe_allow_html=True)
    st.write(f"**Generado el:** {sel_fe}")
    st.divider()

    # --- ESTRUCTURA BASADA EN EL DOCUMENTO WORD ---
    
    # 1. Resumen de Infraestructura (Párrafo narrativo)
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="report-header">1. Infraestructura y Fachada</div>', unsafe_allow_html=True)
    
    campos_infra = ['DELANTERA', 'POSTERIOR', 'MUEBLES', 'PINTURA', 'LIMPIEZA']
    infra_txt = "Durante la inspección visual de la estructura externa, se determinó lo siguiente: "
    
    detalles = []
    for c in [cat for cat in campos_infra if cat in df.columns]:
        val = str(reporte.get(c, 'N/A')).upper()
        status_class = "highlight-ok" if "OK" in val or "PERFECTO" in val else "highlight-fail"
        detalles.append(f"la parte <span class='label-bold'>{c.lower()}</span> se encuentra en estado <span class='{status_class}'>{val}</span>")
    
    st.markdown(f"{infra_txt} {', '.join(detalles)}. " , unsafe_allow_html=True)
    
    # Observaciones específicas de infraestructura
    obs_infra = [c for c in df.columns if 'OBSERVACION' in c.upper() and ('INFRA' in c.upper() or 'ESTRUCTURA' in c.upper() or 'PUERTA' in c.upper())]
    for o in obs_infra:
        txt = str(reporte.get(o, '')).strip()
        if txt.lower() not in ['nan', '', '.']:
            st.markdown(f"<br>**Nota Adicional:** {txt}", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Sistemas y Maquinaria (Párrafo narrativo)
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="report-header">2. Sistemas y Componentes Tecnológicos</div>', unsafe_allow_html=True)
    
    campos_sys = ['ENERGIA', 'INTERNET', 'CABLEADO', 'CAMARAS SEGURIDAD', 'ILUMINACIÓN', 'LOCKERS']
    sys_txt = "En cuanto a los sistemas operativos y conectividad del módulo, se reporta que "
    
    detalles_sys = []
    for s in [sys for sys in campos_sys if sys in df.columns]:
        val_s = str(reporte.get(s, 'N/A')).upper()
        status_s = "highlight-ok" if "OK" in val_s or "PERFECTO" in val_s else "highlight-fail"
        detalles_sys.append(f"el sistema de <span class='label-bold'>{s.lower()}</span> opera como <span class='{status_s}'>{val_s}</span>")
    
    st.markdown(f"{sys_txt} {', '.join(detalles_sys)}. ", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Pantallas y Multimedia (Párrafo narrativo)
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="report-header">3. Gestión de Pantallas y Pilotos</div>', unsafe_allow_html=True)
    
    campos_pan = ['TOTEM IZQUIERDO', 'TOTEM DERECHO', 'TV IZQUIERDO', 'TV DERECHO', 'PILOTO IZQUIERDO', 'COPILOTO DERECHO']
    pan_txt = "El estado de las unidades de visualización y monitores indica que "
    
    detalles_pan = []
    for p in [pan for pan in campos_pan if pan in df.columns]:
        val_p = str(reporte.get(p, 'N/A')).upper()
        status_p = "highlight-ok" if "OK" in val_p or "PERFECTO" in val_p else "highlight-fail"
        detalles_pan.append(f"el <span class='label-bold'>{p.lower()}</span> está <span class='{status_p}'>{val_p}</span>")
    
    st.markdown(f"{pan_txt} {', '.join(detalles_pan)}. ", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Galería de Evidencia
    foto_cols = [c for c in df.columns if 'FOTO' in c.upper() or 'IMAGEN' in c.upper()]
    if foto_cols:
        st.subheader("📸 Registro Fotográfico del Informe")
        f_cols = st.columns(len(foto_cols))
        for i, f in enumerate(foto_cols):
            link = str(reporte.get(f, ''))
            if "http" in link:
                with f_cols[i]:
                    st.image(link.split(';')[0], caption=f, use_container_width=True)

    # 5. Anexo: Todos los campos restantes
    columnas_mostradas = campos_infra + campos_sys + campos_pan + foto_cols + [col_ub, col_fe]
    sobrantes = [c for c in df.columns if c not in columnas_mostradas and 'OBSERV' not in c.upper()]
    
    if sobrantes:
        with st.expander("📂 Datos adicionales del registro"):
            for s in sobrantes:
                val = reporte.get(s)
                if pd.notna(val):
                    st.write(f"**{s}:** {val}")

else:
    st.error("Por favor, asegúrate de que el archivo Excel esté en la carpeta del proyecto.")
