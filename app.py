import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN CRÍTICA ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwYVKV-lDOQau87m7WDEgknpBCBshOJnbhZLaIf4eZa5SsXc_qfNLw150EHvkFaxwok/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

st.set_page_config(page_title="Kioscos IA - Gestión de Operaciones", layout="wide")

# Estilo Dark Neón
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .section-card { background: #0f172a; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 20px; }
    .stTabs [aria-selected="true"] { background-color: #00d4ff !important; color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 REGISTRO DE INSPECCIÓN", "🛠️ DASHBOARD TÉCNICO"])

# --- PESTAÑA 1: INGRESO DE DATOS (Supervisor) ---
with tab1:
    st.title("📋 Nuevo Reporte de Visita")
    
    with st.form("form_registro", clear_on_submit=True):
        # 1. INFO GENERAL
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📍 Información General")
        c1, c2 = st.columns(2)
        tecnico = c1.text_input("Nombre del Técnico / Supervisor")
        ubicacion = c2.selectbox("Ubicación del Módulo", ["LA PUNTA", "SALAVERRY", "JESUS MARIA", "MAGDALENA", "BENAVIDES", "SURCO", "CHACARILLA"])
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. ESTRUCTURA
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏗️ Estructura y Puertas")
        r1, r2, r3, r4 = st.columns(4)
        p_izq = r1.radio("Piloto Izquierdo", ["Perfecto", "Problemas", "Falla"])
        c_der = r2.radio("Copiloto Derecho", ["Perfecto", "Problemas", "Falla"])
        p_del = r3.radio("Delantera", ["Perfecto", "Problemas", "Falla"])
        p_pos = r4.radio("Posterior", ["Perfecto", "Problemas", "Falla"])
        obs_p = st.text_input("Observaciones Puertas")
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. INTERIORES
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏠 Interiores")
        i1, i2, i3, i4 = st.columns(4)
        muebles = i1.radio("Muebles", ["Perfecto", "Sucio/Roto"])
        cableado = i2.radio("Cableado", ["Perfecto", "Desordenado"])
        energia = i3.radio("Energía", ["Perfecto", "Falla"])
        ilumina = i4.radio("Iluminación", ["Perfecto", "Falla"])
        obs_int = st.text_input("Observaciones Interiores")
        st.markdown('</div>', unsafe_allow_html=True)

        # 4. IT PANTALLAS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🖥️ Pantallas (IT)")
        it1, it2, it3, it4, it5 = st.columns(5)
        leds_s = it1.radio("Leds Sup", ["OK", "Falla"])
        t_izq = it2.radio("Totem Izq", ["OK", "Falla"])
        t_der = it3.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it4.radio("TV Izq", ["OK", "Falla"])
        tv_der = it5.radio("TV Der", ["OK", "Falla"])
        obs_pan = st.text_input("Observaciones Pantallas")
        st.markdown('</div>', unsafe_allow_html=True)

        #
