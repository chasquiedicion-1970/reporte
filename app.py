import streamlit as st
import requests
import base64
import pandas as pd

# --- CONFIGURACIÓN DE IDENTIDAD (BASADO EN BRANDBOOK) ---
# Paleta de Colores Oficial 
COLOR_BLACK = "#000000"       # Backgrounds 20%
COLOR_BLUE_SEA = "#000059"    # Main Color / Backgrounds 40%
COLOR_ROYAL_BLUE = "#1900AF"  # Secondary Color / Backgrounds 20%
COLOR_KING_VIOLET = "#7431D8" # Secondary Color / Backgrounds 10%
COLOR_CIAN = "#66FBFC"        # Logo Elements / Accents 5% 
COLOR_SMOKE_SKY = "#EIEDFF"   # Text Backgrounds 5%

URL_BRIDGE = "https://script.google.com/macros/s/AKfycbzfsGoonaLWGVimiPS_v6ZPI_X3RiBQwNFZmJnpSoG0IWBwgLYsIOP_MFAyWHPQG2GZ/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

KIOSCOS_OFICIALES = [
    "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
    "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", 
    "PASTIPAN JAVIER PRADO", "UNIVERSIDAD RICARDO PALMA", "SURCO WONG"
]

st.set_page_config(page_title="Kioscos IA - Gestión Central", layout="wide", page_icon="🚀")

# --- DISEÑO UI CORPORATIVO (CSS) ---
# Se utiliza 'Plus Jakarta Sans' para títulos  y 'Artegra Sans' para cuerpo [cite: 164]
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&display=swap');
    
    .stApp {{ background-color: {COLOR_BLACK}; color: white; }}
    
    /* Encabezado Principal Estilo Brandbook */
    .main-header {{
        background: linear-gradient(135deg, {COLOR_BLUE_SEA} 0%, {COLOR_ROYAL_BLUE} 100%);
        padding: 3rem;
        border-radius: 0px 0px 30px 30px;
        border-bottom: 3px solid {COLOR_CIAN};
        margin-bottom: 2.5rem;
        text-align: center;
        box-shadow: 0 15px 30px rgba(0,0,0,0.5);
    }}
    
    h1 {{ font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; color: white; letter-spacing: -1px; }}
    
    /* Secciones Estilo Tarjeta */
    .stForm, .report-box {{
        background-color: {COLOR_BLUE_SEA} !important;
        padding: 40px !important;
        border-radius: 20px !important;
        border: 1px solid {COLOR_ROYAL_BLUE} !important;
        margin-bottom: 30px !important;
    }}
    
    /* Subtítulos de Sección [cite: 161] */
    .section-header {{
        color: {COLOR_CIAN};
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        border-bottom: 2px solid {COLOR_CIAN};
        padding-bottom: 8px;
        margin-top: 25px;
        margin-bottom: 15px;
    }}
    
    /* Botones Estilo Corporativo */
    div.stButton > button:first-child {{
        background: {COLOR_CIAN};
        color: {COLOR_BLACK};
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        border: none;
        padding: 12px 0px;
        border-radius: 50px;
        width: 100%;
        transition: 0.4s;
    }}
    div.stButton > button:hover {{
        background: white;
        box-shadow: 0 0 25px {COLOR_CIAN};
        transform: translateY(-2px);
    }}
    
    /* Cajas de texto y métricas */
    .text-wrap {{ white-space: pre-wrap; background: {COLOR_BLACK}; padding: 15px; border-radius: 12px; border: 1px solid {COLOR_ROYAL_BLUE}; }}
    [data-testid="stMetricValue"] {{ color: {COLOR_CIAN} !important; }}
    </style>
    """, unsafe_allow_html=True)

# Logo / Título Principal
st.markdown(f'<div class="main-header"><h1>KIOSCOS IΛ</h1><p style="color:{COLOR_CIAN}; font-weight:700;">EL FUTURO EN CADA ESQUINA</p></div>', unsafe_allow_html=True)

menu = st.sidebar.radio("MENÚ DE OPERACIONES", ["📋 SUPERVISOR (Registro)", "📊 REPORTES (Historial)"])

# --- MÓDULO 1: SUPERVISOR ---
if menu == "📋 SUPERVISOR (Registro)":
    st.subheader("📝 Nueva Inspección Técnica")
    
    with st.form("form_oficial"):
        c1, c2 = st.columns(2)
        tec = c1.text_input("NOMBRE DEL TÉCNICO *")
        ubi = c2.selectbox("UBICACIÓN DEL KIOSCO", KIOSCOS_OFICIALES)
        
        st.markdown('<div class="section-header">Infraestructura y Accesos</div>', unsafe_allow_html=True)
        p1, p2, p3, p4 = st.columns(4)
        p_izq = p1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = p2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = p3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = p4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Observaciones de Estructura", height=80)

        st.markdown('<div class="section-header">Sistemas IT y Conectividad</div>', unsafe_allow_html=True)
        it1, it2, it3, it4 = st.columns(4)
        t_izq = it1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it3.radio("TV Izq", ["OK", "Falla"])
        tv_der = it4.radio("TV Der", ["OK", "Falla"])
        obs_pan = st.text_area("Observaciones IT", height=80)

        st.markdown('<div class="section-header">Branding y Limpieza</div>', unsafe_allow_html=True)
        cl1, cl2, cl3 = st.columns(3)
        branding = cl1.radio("Branding", ["OK", "Dañado"])
        l_int = cl2.radio("Limp. Interna", ["Limpio", "Sucio"])
        l_ext = cl3.radio("Limp. Externa", ["Limpio", "Sucio"])

        st.markdown('<div class="section-header">Evidencia Final</div>', unsafe_allow_html=True)
        obs_gen = st.text_area("COMENTARIOS GENERALES *")
        fotos_u = st.file_uploader("Adjuntar Evidencia (Opcional)", accept_multiple_files=True)

        submit = st.form_submit_button("SINCRONIZAR CON BASE DE DATOS")

    if submit:
        if not tec:
            st.error("⚠️ El nombre del técnico es requerido para la validez del reporte.")
        else:
            with st.spinner("Procesando envío corporativo..."):
                links = []
                if fotos_u:
                    for img in fotos_u[:10]:
                        try:
                            b64 = base64.b64encode(img.read()).decode('utf-8')
                            r_img = requests.post("https://api.imgbb.com/1/upload", data={"key": IMGBB_API_KEY, "image": b64})
                            if r_img.status_code == 200: links.append(r_img.json()['data']['url'])
                        except: pass
                
                payload = {
                    "action": "insertar", "tecnico": tec, "ubicacion": ubi,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der, "obs_pan": obs_pan,
                    "branding": branding, "l_int": l_int, "l_ext": l_ext, "obs_gen": obs_gen, "fotos": ";".join(links)
                }
                try:
                    requests.post(URL_BRIDGE, json=payload, timeout=30)
                    st.success("✅ Reporte almacenado exitosamente.")
                    st.balloons()
                except: st.error("❌ Error de sincronización.")

# --- MÓDULO 2: REPORTES ---
else:
    st.subheader("📊 Historial de Inspecciones")
    try:
        r = requests.get(URL_BRIDGE, timeout=35)
        # Validación de integridad de datos (Corrige Error Char 0)
        if r.text.strip().startswith("<!DOCTYPE"):
            st.error("Error: Acceso denegado al Script. Verifique permisos 'Anyone'.")
        else:
            data = r.json()
            if len(data) > 1:
                df = pd.DataFrame(data[1:], columns=data[0])
                df = df[df['Ubicación'].isin(KIOSCOS_OFICIALES)]
                
                f1, f2 = st.columns(2)
                k_sel = f1.selectbox("FILTRAR KIOSCO", df['Ubicación'].unique())
                f_sel = f2.selectbox("SELECCIONAR FECHA", df[df['Ubicación']==k_sel]['Fecha'].unique())
                
                rep = df[(df['Ubicación']==k_sel) & (df['Fecha']==f_sel)].iloc[0]
                
                st.markdown(f'<div class="report-box">', unsafe_allow_html=True)
                st.markdown(f'<h2 style="color:{COLOR_CIAN};">📍 {k_sel}</h2>', unsafe_allow_html=True)
                st.write(f"👷 **Técnico:** {rep.get('Técnico')} | 📅 **Fecha:** {f_sel}")
                
                st.markdown('<div class="section-header">Estado de Infraestructura</div>', unsafe_allow_html=True)
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Piloto Izq", rep.get('Piloto Izquierdo'))
                m2.metric("Copiloto Der", rep.get('Copiloto Derecho'))
                m3.metric("Delantera", rep.get('Delantera'))
                m4.metric("Posterior", rep.get('Posterior'))
                
                st.markdown('<div class="section-header">Sistemas Digitales</div>', unsafe_allow_html=True)
                i1, i2, i3, i4 = st.columns(4)
                i1.metric("Totem Izq", rep.get('Totem Izquierdo'))
                i2.metric("Totem Der", rep.get('Totem Derecho'))
                i3.metric("TV Izq", rep.get('TV Izquierdo'))
                i4.metric("TV Der", rep.get('TV Derecha'))

                st.markdown('<div class="section-header">Observaciones Finales</div>', unsafe_allow_html=True)
                st.markdown(f"<div class='text-wrap'>{rep.get('Obs Generales')}</div>", unsafe_allow_html=True)
                
                if rep.get('Fotos'):
                    st.markdown('<div class="section-header">Evidencia Fotográfica</div>', unsafe_allow_html=True)
                    st.image(str(rep['Fotos']).split(";"), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
