import streamlit as st
import requests
import base64
import pandas as pd

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwZHc5UdHwbx52lgLWL5_LPDEuDjft7_yWbDuR1lDyOZk05h3G4bKfwHjJuHpziNjTS/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

st.set_page_config(page_title="Kioscos IA - Gestión", layout="wide")

# Estilo Kioscos IA
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .main-nav { background-color: #0f172a; padding: 20px; border-radius: 15px; border: 1px solid #00d4ff; margin-bottom: 30px; text-align: center; }
    .report-box { background-color: #0f172a; padding: 25px; border-radius: 15px; border-left: 5px solid #00d4ff; border: 1px solid #1e293b; margin-bottom: 20px; }
    .section-header { color: #00d4ff; font-weight: bold; border-bottom: 1px solid #1e293b; margin-top: 15px; margin-bottom: 10px; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-nav"><h1>🚀 SISTEMA KIOSCOS IA</h1></div>', unsafe_allow_html=True)

# Menú de selección
menu = st.sidebar.radio("MODULO", ["SUPERVISOR", "REPORTES"])

# --- MODULO 1: SUPERVISOR (INGRESO) ---
if menu == "SUPERVISOR":
    st.header("📝 Registro de Inspección")
    with st.form("form_sup", clear_on_submit=True):
        c1, c2 = st.columns(2)
        tec = c1.text_input("Técnico Responsable")
        ubi = c2.selectbox("Kiosco", ["LA PUNTA", "SALAVERRY", "JESUS MARIA", "MAGDALENA", "SURCO", "CHACARILLA"])
        
        st.markdown('<div class="section-header">🏗️ ESTRUCTURA</div>', unsafe_allow_html=True)
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        p_izq = col_p1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = col_p2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = col_p3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = col_p4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Observaciones Puertas")

        st.markdown('<div class="section-header">🖥️ SISTEMAS IT</div>', unsafe_allow_html=True)
        it1, it2, it3 = st.columns(3)
        t_izq = it1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it3.radio("TV Principal", ["OK", "Falla"])
        obs_pan = st.text_area("Observaciones IT")

        st.subheader("📸 Evidencia")
        obs_gen = st.text_area("Comentarios Finales *")
        fotos = st.file_uploader("Fotos", accept_multiple_files=True)

        if st.form_submit_button("✅ ENVIAR REPORTE"):
            if not tec or not fotos:
                st.error("Nombre y fotos son obligatorios.")
            else:
                with st.spinner("Enviando..."):
                    links = []
                    for img in fotos[:10]:
                        res = requests.post("https://api.imgbb.
