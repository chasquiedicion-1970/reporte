import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwYVKV-lDOQau87m7WDEgknpBCBshOJnbhZLaIf4eZa5SsXc_qfNLw150EHvkFaxwok/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

st.set_page_config(page_title="Kioscos IA - Operaciones", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .section-card { background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 REGISTRO", "🛠️ GESTIÓN"])

with tab1:
    st.title("📋 Reporte Integral")
    
    # 1. INICIO DEL FORMULARIO
    with st.form("main_form", clear_on_submit=True):
        
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        tecnico = c1.text_input("Nombre del Técnico *")
        ubicacion = c2.selectbox("Ubicación", ["LA PUNTA", "SALAVERRY", "JESUS MARIA", "MAGDALENA", "SURCO", "CHACARILLA"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Estructura y Puertas")
        cp1, cp2, cp3, cp4 = st.columns(4)
        p_izq = cp1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = cp2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = cp3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = cp4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_input("Obs. Puertas")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("IT y Pantallas")
        it1, it2, it3 = st.columns(3)
        t_izq = it1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it3.radio("TV Izq", ["OK", "Falla"])
        obs_pan = st.text_input("Obs. Pantallas")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Branding y Limpieza")
        b1, b2, b3 = st.columns(3)
        branding = b1.radio("Branding", ["OK", "Dañado"])
        l_int = b2.radio("Limp. Interna", ["OK", "Sucio"])
        l_ext = b3.radio("Limp. Externa", ["OK", "Sucio"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("Evidencia y Notas")
        obs_gen = st.text_area("Observaciones Generales *")
        uploaded_images = st.file_uploader("Fotos (5-10)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

        # EL BOTÓN DEBE ESTAR AQUÍ (DENTRO DEL WITH)
        submit = st.form_submit_button("✅ ENVIAR REPORTE COMPLETO")

    # 2. PROCESAMIENTO (FUERA DEL FORM PERO DISPARADO POR EL SUBMIT)
    if submit:
        if not tecnico or not uploaded_images:
            st.warning("⚠️ Nombre y fotos son obligatorios.")
        else:
            links_fotos = []
            with st.spinner("Subiendo datos..."):
                for file in uploaded_images[:10]:
                    try:
                        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(file.read()).decode('utf-8')}
                        res = requests.post("https://api.imgbb.com/1/upload", payload)
                        if res.status_code == 200: links_fotos.append(res.json()['data']['url'])
                    except: pass
                
                data_final = {
                    "action": "insertar",
                    "tecnico": tecnico, "ubicacion": ubicacion,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "muebles": "OK", "cableado": "OK", "energia": "OK", "iluminacion": "OK", "obs_int": "N/A",
                    "leds_s": "OK", "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": "OK", "obs_pan": obs_pan,
                    "internet": "OK", "wifi": "OK", "lockers": "OK", "camaras": "OK", "boton": "OK", "obs_otros": "N/A",
                    "m_izq": "OK", "m_der": "OK", "obs_maq": "N/A",
                    "branding": branding, "l_int": l_int, "l_ext": l_ext, "l_vis": "OK", "obs_mod": "N/A",
                    "obs_gen": obs_gen, "fotos": ";".join(links_fotos)
                }
                
                try:
                    r = requests.post(URL_BRIDGE, json=data_final)
                    if r.status_code == 200:
                        st.success("¡Reporte guardado!")
                        st.balloons()
                except: st.error("Error de conexión.")

with tab2:
    st.title("Gestión")
    if st.button("Actualizar"):
        r = requests.get(URL_BRIDGE)
        if r.status_code == 200:
            df = pd.DataFrame(r.json()[1:], columns=r.json()[0])
            st.write(df)
