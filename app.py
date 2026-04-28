import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbzvBhp7v71nPCS3-E8QD67OqeK4P4nefxnqA6cXQczbCPlbCuQ1BunSnL2dLN5Yo5ej/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

st.set_page_config(page_title="Kioscos IA - Operaciones", layout="wide")

# Estilo Kioscos IA
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .section-card { background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 20px; }
    .stTabs [aria-selected="true"] { background-color: #00d4ff !important; color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 REGISTRO DE INSPECCIÓN", "🛠️ DASHBOARD TÉCNICO"])

# --- PARTE 1: INGRESO DE DATOS (SECCIONES 1-16) ---
with tab1:
    st.title("📋 Reporte Integral de Visita")
    
    with st.form("main_form", clear_on_submit=True):
        # 1. INFO GENERAL (Pantallazo 1)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📍 Información General")
        c1, c2 = st.columns(2)
        tecnico = c1.text_input("1. TU NOMBRE *")
        ubicacion = c2.selectbox("3. UBICACIÓN DEL MODULO *", [
            "LA PUNTA", "SALAVERRY REAL PLAZA (JESUS MARIA)", "PERSHING - DOMINGO ORUE (JESUS MARIA)", 
            "ARENALES - DOMINGO CUETO (JESUS MARIA)", "VIVANDA JAVIER PRADO (MAGDALENA)", 
            "PASTIPAN JAVIER PRADO (MAGDALENA)", "U: RICARDO PALMA (SURCO)", "CHACARILLA (SURCO)"
        ])
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. ESTRUCTURA (Pantallazo 2)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏗️ 4. ESTRUCTURA - PUERTAS")
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        p_izq = col_p1.radio("Piloto Izquierdo", ["Perfecto", "Con Problemas", "No Funciona"])
        c_der = col_p2.radio("Copiloto Derecho", ["Perfecto", "Con Problemas", "No Funciona"])
        p_del = col_p3.radio("Delantera", ["Perfecto", "Con Problemas", "No Funciona"])
        p_pos = col_p4.radio("Posterior", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_p = st.text_input("5. OBSERVACIONES PUERTAS")
        
        st.subheader("🏠 6. INTERIORES")
        col_i1, col_i2, col_i3, col_i4 = st.columns(4)
        muebles = col_i1.radio("Muebles", ["Perfecto", "Con Problemas", "No Funciona"])
        cableado = col_i2.radio("Cableado", ["Perfecto", "Con Problemas", "No Funciona"])
        energia = col_i3.radio("Energía", ["Perfecto", "Con Problemas", "No Funciona"])
        ilumina = col_i4.radio("Iluminación", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_int = st.text_input("7. OBSERVACIONES INTERIORES")
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. IT (Pantallazo 3)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🖥️ 8. PANTALLAS (IT)")
        it1, it2, it3, it4, it5 = st.columns(5)
        leds_s = it1.radio("Leds Superiores", ["Perfecto", "Con Problemas", "No Funciona"])
        t_izq = it2.radio("Totem Izquierdo", ["Perfecto", "Con Problemas", "No Funciona"])
        t_der = it3.radio("Totem Derecho", ["Perfecto", "Con Problemas", "No Funciona"])
        tv_izq = it4.radio("TV Izquierdo", ["Perfecto", "Con Problemas", "No Funciona"])
        tv_der = it5.radio("TV Derecho", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_pan = st.text_input("9. OBSERVACIONES PANTALLAS")
        st.markdown('</div>', unsafe_allow_html=True)

        # 4. OTROS (Pantallazo 4)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("⚙️ 10. OTROS")
        o1, o2, o3, o4, o5 = st.columns(5)
        internet = o1.radio("Internet", ["Perfecto", "Con Problemas", "No Funciona"])
        wifi = o2.radio("Wi-Fi Gratuito", ["Perfecto", "Con Problemas", "No Funciona"])
        lockers = o3.radio("Lockers", ["Perfecto", "Con Problemas", "No Funciona"])
        camaras = o4.radio("Cámaras Seguridad", ["Perfecto", "Con Problemas", "No Funciona"])
        boton = o5.radio("Botón de Pánico", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_otros = st.text_input("11. OBSERVACIONES OTROS")
        st.markdown('</div>', unsafe_allow_html=True)

        # 5. MAQUINAS (Pantallazo 5)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🥤 12. MAQUINAS EXPENDEDORAS")
        m1, m2 = st.columns(2)
        maq_izq = m1.radio("Máquina Izquierda", ["Perfecto", "Con Problemas", "No Funciona"])
        maq_der = m2.radio("Máquina Derecha", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_maq = st.text_input("13. OBSERVACIONES MAQUINAS")
        st.markdown('</div>', unsafe_allow_html=True)

        # 6. BRANDING / LIMPIEZA (Pantallazo 6)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("✨ 14. BRANDING Y LIMPIEZA")
        b1, b2, b3, b4 = st.columns(4)
        branding = b1.radio("Branding", ["Perfecto", "Sucio/Roto", "Urge Cambio"])
        l_int = b2.radio("Limpieza Interna", ["Perfecto", "Sucio/Roto", "Urge Cambio"])
        l_ext = b3.radio("Limpieza Externa", ["Perfecto", "Sucio/Roto", "Urge Cambio"])
        l_vis = b4.radio("Leds Visuales", ["Perfecto", "Sucio/Roto", "Urge Cambio"])
        obs_mod = st.text_input("15. OBSERVACIONES ESTADO MODULO")
        st.markdown('</div>', unsafe_allow_html=True)

        # 7. GENERAL Y FOTOS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📝 16. OBSERVACIONES GENERALES")
        obs_gen = st.text_area("Describa sus observaciones generales luego de la visita *")
        st.subheader("📸 REGISTRO FOTOGRÁFICO")
        uploaded_images = st.file_uploader("Sube entre 5 y 10 fotos", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        st.markdown('</div>', unsafe_allow_html=True)

        submit = st.form_submit
