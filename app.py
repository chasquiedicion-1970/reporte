import streamlit as st
import requests
import base64
import pandas as pd

# --- IDENTIDAD CORPORATIVA (BRANDBOOK) ---
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

st.set_page_config(page_title="Kioscos IA - Dashboard", layout="wide", page_icon="🚀")

# --- LÓGICA DE NAVEGACIÓN ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'INICIO'

def navegar(nombre_pagina):
    st.session_state.pagina = nombre_pagina

# --- CSS DE ALTO IMPACTO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BLACK}; color: white; }}
    
    /* Header */
    .main-header {{
        background: linear-gradient(90deg, {COLOR_BLUE_SEA} 0%, #1900AF 100%);
        padding: 2.5rem; border-radius: 0 0 30px 30px; border-bottom: 4px solid {COLOR_CIAN};
        text-align: center; margin-bottom: 2rem;
    }}

    /* Tarjetas de Menú Central */
    .menu-card {{
        background: {COLOR_BLUE_SEA};
        padding: 50px 30px;
        border-radius: 20px;
        border: 2px solid #1900AF;
        text-align: center;
        transition: 0.3s;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .menu-card:hover {{ border-color: {COLOR_CIAN}; transform: translateY(-5px); }}

    /* Botones Neón */
    div.stButton > button {{
        background: {COLOR_CIAN} !important; color: {COLOR_BLACK} !important;
        font-weight: 800 !important; border-radius: 50px !important;
        border: none !important; padding: 15px 30px !important; width: 100%;
    }}
    
    /* Secciones */
    .section-header {{ color: {COLOR_CIAN}; font-weight: bold; text-transform: uppercase; border-bottom: 2px solid {COLOR_CIAN}; padding-bottom: 5px; margin-bottom: 15px; }}
    .text-box {{ background: #000; padding: 15px; border-radius: 10px; border: 1px solid #1900AF; white-space: pre-wrap; }}
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown(f"""
    <div class="main-header">
        <h1>KIOSCOS IΛ</h1>
        <p style="color:{COLOR_CIAN}; letter-spacing:3px; font-weight:bold;">EL FUTURO EN CADA ESQUINA</p>
    </div>
""", unsafe_allow_html=True)

# --- PANTALLA 1: INICIO ---
if st.session_state.pagina == 'INICIO':
    st.write("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        c_left, c_right = st.columns(2)
        
        with c_left:
            st.markdown(f'<div class="menu-card"><h2>📋 SUPERVISOR</h2><p>Ingreso de inspección técnica y evidencia fotográfica.</p></div>', unsafe_allow_html=True)
            if st.button("ACCEDER A INGRESO"):
                navegar('SUPERVISOR')
                st.rerun()

        with c_right:
            st.markdown(f'<div class="menu-card"><h2>📊 REPORTES</h2><p>Control de historial y auditoría de puntos instalados.</p></div>', unsafe_allow_html=True)
            if st.button("CONTROL DE REPORTES"):
                navegar('REPORTES')
                st.rerun()

# --- PANTALLA 2: SUPERVISOR ---
elif st.session_state.pagina == 'SUPERVISOR':
    if st.button("← VOLVER AL MENÚ PRINCIPAL"):
        navegar('INICIO')
        st.rerun()
    
    st.subheader("📝 Nuevo Registro Técnico")
    with st.form("form_registro"):
        f1, f2 = st.columns(2)
        tec = f1.text_input("NOMBRE DEL TÉCNICO (OBLIGATORIO) *")
        ubi = f2.selectbox("UBICACIÓN", KIOSCOS_OFICIALES)
        
        st.markdown('<div class="section-header">Infraestructura y Pantallas</div>', unsafe_allow_html=True)
        it1, it2, it3, it4, it5 = st.columns(5)
        t_izq = it1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it3.radio("TV Izq", ["OK", "Falla"])
        tv_der = it4.radio("TV Der", ["OK", "Falla"])
        p_360 = it5.radio("Pantallas 360", ["OK", "Falla"])
        obs_it = st.text_area("Notas IT")

        st.markdown('<div class="section-header">Estructura y Energía</div>', unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        energia, ilumina = e1.radio("Energía", ["OK", "Falla"]), e2.radio("Luz", ["OK", "Falla"])
        muebles, branding = e3.radio("Muebles", ["OK", "Falla"]), e4.radio("Branding", ["OK", "Falla"])
        obs_gen = st.text_area("Comentarios Finales *")
        fotos_u = st.file_uploader("Evidencia (Opcional)", accept_multiple_files=True)

        if st.form_submit_button("✅ GUARDAR EN BASE DE DATOS"):
            if not tec:
                st.error("⚠️ El nombre es obligatorio.")
            else:
                with st.spinner("Sincronizando..."):
                    links = []
                    if fotos_u:
                        for img in fotos_u:
                            b64 = base64.b64encode(img.read()).decode('utf-8')
