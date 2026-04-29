import streamlit as st
import requests
import base64
import pandas as pd

# --- CONFIGURACIÓN DE IDENTIDAD KIOSCOS IA ---
COLOR_BLUE_SEA = "#000059"
COLOR_CIAN = "#66FBFC"
COLOR_BLACK = "#000000"

URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwZHc5UdHwbx52lgLWL5_LPDEuDjft7_yWbDuR1lDyOZk05h3G4bKfwHjJuHpziNjTS/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

KIOSCOS_OFICIALES = [
    "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
    "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", 
    "PASTIPAN JAVIER PRADO", "UNIVERSIDAD RICARDO PALMA", "SURCO WONG"
]

st.set_page_config(page_title="Kioscos IA - Operaciones", layout="wide", page_icon="🚀")

# --- LÓGICA DE NAVEGACIÓN (SESSION STATE) ---
if 'page' not in st.session_state:
    st.session_state.page = 'HOME'

def change_page(page_name):
    st.session_state.page = page_name

# --- CSS AVANZADO (DISEÑO CORPORATIVO) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BLACK}; color: white; }}
    
    /* Header Principal */
    .main-header {{
        background: linear-gradient(90deg, {COLOR_BLUE_SEA} 0%, #1900AF 100%);
        padding: 3rem; border-radius: 0 0 40px 40px; border-bottom: 4px solid {COLOR_CIAN};
        text-align: center; margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    
    /* Tarjetas de Selección en Home */
    .option-card {{
        background-color: {COLOR_BLUE_SEA};
        padding: 40px; border-radius: 25px; border: 2px solid #1900AF;
        text-align: center; transition: 0.4s; height: 350px;
        display: flex; flex-direction: column; justify-content: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .option-card:hover {{ border-color: {COLOR_CIAN}; transform: translateY(-10px); }}
    
    /* Botones de Navegación */
    div.stButton > button {{
        background: {COLOR_CIAN}; color: {COLOR_BLACK};
        font-weight: 800; border-radius: 50px; border: none;
        padding: 15px 40px; width: 100%; transition: 0.3s;
        text-transform: uppercase; letter-spacing: 1px;
    }}
    div.stButton > button:hover {{ background: white; box-shadow: 0 0 20px {COLOR_CIAN}; }}
    
    /* Botón Volver */
    .back-btn button {{ background: transparent !important; color: {COLOR_CIAN} !important; border: 1px solid {COLOR_CIAN} !important; }}

    /* Estilo de Secciones e Inputs */
    .section-header {{ color: {COLOR_CIAN}; font-weight: bold; text-transform: uppercase; border-bottom: 2px solid {COLOR_CIAN}; padding-bottom: 5px; margin: 25px 0 10px 0; }}
    .report-card {{ background-color: {COLOR_BLUE_SEA}; padding: 30px; border-radius: 20px; border: 1px solid #1900AF; }}
    .text-wrap {{ white-space: pre-wrap; background: #000; padding: 15px; border-radius: 10px; border: 1px solid #1900AF; color: #cbd5e1; }}
    [data-testid="stMetricValue"] {{ color: {COLOR_CIAN} !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA COMPARTIDA ---
st.markdown(f'''
    <div class="main-header">
        <h1>KIOSCOS IΛ</h1>
        <p style="color:{COLOR_CIAN}; font-weight:bold; letter-spacing:2px;">EL FUTURO EN CADA ESQUINA</p>
    </div>
''', unsafe_allow_html=True)

# --- PANTALLA 1: HOME (MENÚ PRINCIPAL) ---
if st.session_state.page == 'HOME':
    st.write("<br><br>", unsafe_allow_html=True)
    col_left, col_mid, col_right = st.columns([1, 4, 1])
    
    with col_mid:
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown(f'''
                <div class="option-card">
                    <h2 style="color:{COLOR_CIAN};">📋 SUPERVISOR</h2>
                    <p>Ingreso técnico de infraestructura,<br>estado de tótems y evidencia.</p>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("INGRESAR DATOS"):
                change_page('SUPERVISOR')
                st.rerun()

        with c2:
            st.markdown(f'''
                <div class="option-card">
                    <h2 style="color:{COLOR_CIAN};">📊 REPORTES</h2>
                    <p>Consulta de historial,<br>métricas y auditoría de puntos.</p>
                </div>
            ''', unsafe_allow_html=True)
            if st.button("CONTROL DE REPORTES"):
                change_page('REPORTES')
                st.rerun()

# --- PANTALLA 2: SUPERVISOR ---
elif st.session_state.page == 'SUPERVISOR':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← VOLVER AL MENÚ"):
        change_page('HOME')
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("📝 Registro Técnico de Módulo")
    
    with st.form("form_sup"):
        f1, f2 = st.columns(2)
        tec = f1.text_input("TÉCNICO RESPONSABLE *")
        ubi = f2.selectbox("KIOSCO", KIOSCOS_OFICIALES)
        
        st.markdown('<div class="section-header">🏗️ Estructura</div>', unsafe_allow_html=True)
        cp1, cp2, cp3, cp4 = st.columns(4)
        p_izq = cp1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = cp2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = cp3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = cp4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Notas Estructura")

        st.markdown('<div class="section-header">🖥️ Sistemas IT & Pantallas</div>', unsafe_allow_html=True)
        it1, it2, it3, it4 = st.columns(4)
        t_izq, t_der = it1.radio("Totem Izq", ["OK", "Falla"]), it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq, tv_der = it3.radio("TV Izq", ["OK", "Falla"]), it4.radio("TV Der", ["OK", "Falla"])
        p_360 = st.radio("PANTALLAS 360", ["OK", "Falla"], horizontal=True)
        obs_it = st.text_area("Notas IT")

        st.markdown('<div class="section-header">🏠 Energía e Interiores</div>', unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        muebles, cableado = e1.radio("Muebles", ["OK", "Falla"]), e2.radio("Cableado", ["OK", "Falla"])
        energia, ilumina = e3.radio("Energía", ["OK", "Falla"]), e4.radio("Iluminación", ["OK", "Falla"])
        
        st.markdown('<div class="section-header">Finalización</div>', unsafe_allow_html=True)
        obs_gen = st.text_area("COMENTARIOS GENERALES")
        fotos_u = st.file_uploader("Evidencia (Opcional)", accept_multiple_files=True)

        submit = st.form_submit_button("✅ GUARDAR REPORTE")

    if submit:
        if not tec:
            st.error("⚠️ El nombre del técnico es obligatorio.")
        else:
            with st.spinner("Sincronizando con base de datos..."):
                links = []
                if fotos_u:
                    for img in fotos_u:
                        try:
                            b64 = base64.b64encode(img.read()).decode('utf-8')
                            res = requests.post("https://api.imgbb.com/1/upload", data={"key": IMGBB_API_KEY, "image": b64})
                            if res.status_code == 200: links.append(res.json()['data']['url'])
                        except: pass
                
                payload = {
                    "
