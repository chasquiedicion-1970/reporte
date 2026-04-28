import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE CONEXIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbzvBhp7v71nPCS3-E8QD67OqeK4P4nefxnqA6cXQczbCPlbCuQ1BunSnL2dLN5Yo5ej/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca" 

st.set_page_config(page_title="Kioscos IA - Gestión de Operaciones", layout="wide")

# Estilo Visual Kioscos IA
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .section-card { background: #0f172a; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 20px; }
    .stTabs [aria-selected="true"] { background-color: #00d4ff !important; color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 REGISTRO DE INSPECCIÓN", "🛠️ DASHBOARD TÉCNICO"])

# --- PARTE 1: INGRESO DE DATOS (ORDEN EXACTO SEGÚN PANTALLAZOS) ---
with tab1:
    st.title("📋 Nuevo Reporte de Visita")
    
    with st.form("main_form", clear_on_submit=True):
        # 1. INFO GENERAL
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📍 1. Información General")
        c1, c2 = st.columns(2)
        tecnico = c1.text_input("Nombre del Técnico / Supervisor")
        ubicacion = c2.selectbox("Ubicación del Módulo", [
            "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
            "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", "PASTIPAN JAVIER PRADO",
            "U: RICARDO PALMA", "CHACARILLA", "JESUS MARIA", "MAGDALENA"
        ])
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. ESTRUCTURA (PUERTAS)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏗️ 2. Estructura y Puertas")
        r1, r2, r3, r4 = st.columns(4)
        p_izq = r1.radio("Piloto Izquierdo", ["Perfecto", "Con Problemas", "No Funciona"])
        c_der = r2.radio("Copiloto Derecho", ["Perfecto", "Con Problemas", "No Funciona"])
        p_del = r3.radio("Delantera", ["Perfecto", "Con Problemas", "No Funciona"])
        p_pos = r4.radio("Posterior", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_p = st.text_input("Observaciones Puertas")
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. INTERIORES
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏠 3. Interiores")
        i1, i2, i3, i4 = st.columns(4)
        muebles = i1.radio("Muebles", ["Perfecto", "Sucio/Roto"])
        cableado = i2.radio("Cableado", ["Perfecto", "Desordenado"])
        energia = i3.radio("Energía", ["Perfecto", "Falla"])
        ilumina = i4.radio("Iluminación", ["Perfecto", "Falla"])
        obs_int = st.text_input("Observaciones Interiores")
        st.markdown('</div>', unsafe_allow_html=True)

        # 4. IT (PANTALLAS)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🖥️ 4. IT y Pantallas")
        it1, it2, it3, it4, it5 = st.columns(5)
        leds_s = it1.radio("Leds Superiores", ["Perfecto", "Falla"])
        t_izq = it2.radio("Totem Izquierdo", ["Perfecto", "Falla"])
        t_der = it3.radio("Totem Derecho", ["Perfecto", "Falla"])
        tv_izq = it4.radio("TV Izquierdo", ["Perfecto", "Falla"])
        tv_der = it5.radio("TV Derecho", ["Perfecto", "Falla"])
        obs_pan = st.text_input("Observaciones Pantallas")
        st.markdown('</div>', unsafe_allow_html=True)

        # 5. OTROS / MAQUINAS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("⚙️ 5. Otros y Máquinas")
        o1, o2, o3, o4 = st.columns(4)
        internet = o1.radio("Internet", ["Perfecto", "Falla"])
        camaras = o2.radio("Cámaras Seguridad", ["Perfecto", "Falla"])
        m_izq = o3.radio("Máquina Izquierda", ["Perfecto", "Falla"])
        m_der = o4.radio("Máquina Derecha", ["Perfecto", "Falla"])
        obs_gen = st.text_area("Observaciones Generales / Otros")
        st.markdown('</div>', unsafe_allow_html=True)

        # 6. BRANDING Y LIMPIEZA
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("✨ 6. Branding y Limpieza")
        b1, b2, b3 = st.columns(3)
        branding = b1.radio("Branding", ["Perfecto", "Dañado"])
        l_int = b2.radio("Limpieza Interna", ["Perfecto", "Sucio"])
        l_ext = b3.radio("Limpieza Externa", ["Perfecto", "Sucio"])
        st.markdown('</div>', unsafe_allow_html=True)

        # 7. FOTOS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📸 7. Registro Fotográfico")
        uploaded_images = st.file_uploader("Sube entre 5 y 10 fotos", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        st.markdown('</div>', unsafe_allow_html=True)

        submit = st.form_submit_button("✅ ENVIAR REPORTE COMPLETO")

        if submit:
            if not tecnico or not uploaded_images:
                st.warning("⚠️ Debes ingresar tu nombre y subir las fotos.")
            else:
                links_fotos = []
                with st.spinner("Subiendo fotos y guardando reporte..."):
                    for file in uploaded_images[:10]:
                        try:
                            payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(file.read()).decode('utf-8')}
                            res = requests.post("https://api.imgbb.com/1/upload", payload)
                            if res.status_code == 200:
                                links_fotos.append(res.json()['data']['url'])
                        except: pass
                    
                    data_to_send = {
                        "action": "insertar",
                        "tecnico": tecnico, "ubicacion": ubicacion,
                        "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                        "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina, "obs_int": obs_int,
                        "leds_s": leds_s, "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der, "obs_pan": obs_pan,
                        "internet": internet, "camaras": camaras
