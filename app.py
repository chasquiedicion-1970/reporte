import streamlit as st
import requests
import base64
import pandas as pd

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwZHc5UdHwbx52lgLWL5_LPDEuDjft7_yWbDuR1lDyOZk05h3G4bKfwHjJuHpziNjTS/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

# Lista Maestra Actualizada
KIOSCOS_OFICIALES = [
    "LA PUNTA", 
    "SALAVERRY REAL PLAZA", 
    "PERSHING - DOMINGO ORUE", 
    "ARENALES - DOMINGO CUETO", 
    "VIVANDA JAVIER PRADO", 
    "PASTIPAN JAVIER PRADO", 
    "UNIVERSIDAD RICARDO PALMA", 
    "SURCO WONG"
]

st.set_page_config(page_title="Kioscos IA - Gestión Central", layout="wide")

# Estilo con soporte para saltos de línea
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .main-nav { background-color: #0f172a; padding: 20px; border-radius: 15px; border: 1px solid #00d4ff; margin-bottom: 30px; text-align: center; }
    .report-box { background-color: #0f172a; padding: 25px; border-radius: 15px; border-left: 5px solid #00d4ff; border: 1px solid #1e293b; margin-bottom: 20px; }
    .section-header { color: #00d4ff; font-weight: bold; border-bottom: 1px solid #1e293b; margin-top: 20px; margin-bottom: 10px; font-size: 1.1rem; text-transform: uppercase; }
    .text-wrap { white-space: pre-wrap; font-family: sans-serif; background: #1e293b; padding: 12px; border-radius: 8px; border: 1px solid #334155; color: #cbd5e1; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-nav"><h1>🚀 SISTEMA INTEGRAL KIOSCOS IA</h1></div>', unsafe_allow_html=True)
menu = st.sidebar.radio("MÓDULO SELECCIONADO", ["SUPERVISOR (Ingreso)", "REPORTES (Consulta)"])

# --- MÓDULO 1: SUPERVISOR (INGRESO TOTAL) ---
if menu == "SUPERVISOR (Ingreso)":
    st.header("📝 Registro de Inspección Oficial")
    with st.form("form_sup_final", clear_on_submit=True):
        c1, c2 = st.columns(2)
        tec = c1.text_input("Técnico Responsable *")
        ubi = c2.selectbox("Seleccione Kiosco Oficial *", KIOSCOS_OFICIALES)
        
        # SECCIÓN 1: ESTRUCTURA
        st.markdown('<div class="section-header">🏗️ Estructura y Puertas</div>', unsafe_allow_html=True)
        cp1, cp2, cp3, cp4 = st.columns(4)
        p_izq = cp1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = cp2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = cp3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = cp4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Observaciones Puertas")

        # SECCIÓN 2: INTERIORES
        st.markdown('<div class="section-header">🏠 Interiores y Energía</div>', unsafe_allow_html=True)
        ci1, ci2, ci3, ci4 = st.columns(4)
        muebles = ci1.radio("Muebles", ["OK", "Falla"])
        cableado = ci2.radio("Cableado", ["OK", "Falla"])
        energia = ci3.radio("Energía", ["OK", "Falla"])
        ilumina = ci4.radio("Iluminación", ["OK", "Falla"])
        obs_int = st.text_area("Observaciones Interiores")

        # SECCIÓN 3: IT COMPLETO
        st.markdown('<div class="section-header">🖥️ Sistemas IT y Pantallas</div>', unsafe_allow_html=True)
        it_c1, it_c2, it_c3, it_c4 = st.columns(4)
        t_izq = it_c1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it_c2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it_c3.radio("TV Izquierda", ["OK", "Falla"])
        tv_der = it_c4.radio("TV Derecha", ["OK", "Falla"])
        leds_s = st.radio("LEDs Superiores", ["OK", "Falla"], horizontal=True)
        obs_pan = st.text_area("Observaciones IT")

        # SECCIÓN 4: OTROS COMPONENTES
        st.markdown('<div class="section-header">⚙️ Conectividad y Seguridad</div>', unsafe_allow_html=True)
        co1, co2, co3, co4 = st.columns(4)
        internet = co1.radio("Internet", ["OK", "Falla"])
        wifi = co2.radio("Wifi Gratuito", ["OK", "Falla"])
        camaras = co3.radio("Cámaras", ["OK", "Falla"])
        boton = co4.radio("Botón Pánico", ["OK", "Falla"])

        # SECCIÓN 5: ESTÉTICA
        st.markdown('<div class="section-header">✨ Branding y Limpieza</div>', unsafe_allow_html=True)
        cl1, cl2, cl3 = st.columns(3)
        branding = cl1.radio("Branding", ["OK", "Dañado"])
        l_int = cl2.radio("Limpieza Int.", ["OK", "Sucio"])
        l_ext = cl3.radio("Limpieza Ext.", ["OK", "Sucio"])
        obs_mod = st.text_area("Observaciones Módulo / Limpieza")

        st.subheader("📸 Evidencia Final")
        obs_gen = st.text_area("Comentarios Generales del Supervisor *")
        fotos_u = st.file_uploader("Fotos de Inspección", accept_multiple_files=True)

        if st.form_submit_button("✅ ENVIAR REPORTE COMPLETO"):
            with st.spinner("Sincronizando con Excel..."):
                links = []
                for img in fotos_u[:10]:
                    res = requests.post("https://api.imgbb.com/1/upload", data={"key": IMGBB_API_KEY, "image": base64.b64encode(img.read()).decode('utf-8')})
                    if res.status_code == 200: links.append(res.json()['data']['url'])
                
                payload = {
                    "action": "insertar", "tecnico": tec, "ubicacion": ubi,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina, "obs_int": obs_int,
                    "leds_s": leds_s, "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der, "obs_pan": obs_pan,
                    "internet": internet, "wifi": wifi, "lockers": "OK", "camaras": camaras, "boton": boton,
                    "branding":
