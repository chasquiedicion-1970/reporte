import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE CONEXIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbzfsGoonaLWGVimiPS_v6ZPI_X3RiBQwNFZmJnpSoG0IWBwgLYsIOP_MFAyWHPQG2GZ/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

st.set_page_config(page_title="Kioscos IA - Operaciones", layout="wide")

# Estilo Dark Neón
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .section-card { background: #0f172a; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 20px; }
    .stTabs [aria-selected="true"] { background-color: #00d4ff !important; color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 REGISTRO DE INSPECCIÓN", "🛠️ DASHBOARD TÉCNICO"])

# --- PARTE 1: INGRESO DE DATOS ---
with tab1:
    st.title("📋 Reporte Integral de Visita")
    
    with st.form("main_form", clear_on_submit=True):
        # 1. INFO GENERAL
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📍 Información General")
        c1, c2 = st.columns(2)
        tecnico = c1.text_input("1. TU NOMBRE *")
        ubicacion = c2.selectbox("3. UBICACIÓN DEL MODULO *", [
            "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
            "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", 
            "PASTIPAN JAVIER PRADO", "U: RICARDO PALMA", "CHACARILLA"
        ])
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. ESTRUCTURA Y PUERTAS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏗️ ESTRUCTURA Y PUERTAS")
        cp1, cp2, cp3, cp4 = st.columns(4)
        p_izq = cp1.radio("Piloto Izquierdo", ["Perfecto", "Problemas", "Falla"])
        c_der = cp2.radio("Copiloto Derecho", ["Perfecto", "Problemas", "Falla"])
        p_del = cp3.radio("Delantera", ["Perfecto", "Problemas", "Falla"])
        p_pos = cp4.radio("Posterior", ["Perfecto", "Problemas", "Falla"])
        obs_p = st.text_input("5. Observaciones Puertas")
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. INTERIORES
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏠 INTERIORES")
        ci1, ci2, ci3, ci4 = st.columns(4)
        muebles = ci1.radio("Muebles", ["OK", "Falla"])
        cableado = ci2.radio("Cableado", ["OK", "Falla"])
        energia = ci3.radio("Energía", ["OK", "Falla"])
        ilumina = ci4.radio("Iluminación", ["OK", "Falla"])
        obs_int = st.text_input("7. Observaciones Interiores")
        st.markdown('</div>', unsafe_allow_html=True)

        # 4. IT PANTALLAS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🖥️ PANTALL
