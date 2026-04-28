import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Asegúrate de que esta URL sea la de tu última implementación
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbyNH9DuCbxRkAcjeSk_E84wWXWyE7toVZ5aol9E3oUFOpNh5yxe8aqMP8PoX0rbPDLm/exec"
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
        p_izq = cp1.radio("Piloto Izquierdo", ["Perfecto", "Con Problemas", "No Funciona"])
        c_der = cp2.radio("Copiloto Derecho", ["Perfecto", "Con Problemas", "No Funciona"])
        p_del = cp3.radio("Delantera", ["Perfecto", "Con Problemas", "No Funciona"])
        p_pos = cp4.radio("Posterior", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_p = st.text_input("Observaciones Puertas")
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. INTERIORES
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏠 INTERIORES")
        ci1, ci2, ci3, ci4 = st.columns(4)
        muebles = ci1.radio("Muebles", ["Perfecto", "Con Problemas", "No Funciona"])
        cableado = ci2.radio("Cableado", ["Perfecto", "Con Problemas", "No Funciona"])
        energia = ci3.radio("Energía", ["Perfecto", "Con Problemas", "No Funciona"])
        ilumina = ci4.radio("Iluminación", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_int = st.text_input("Observaciones Interiores")
        st.markdown('</div>', unsafe_allow_html=True)

        # 4. IT PANTALLAS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🖥️ PANTALLAS (IT)")
        it1, it2, it3, it4, it5 = st.columns(5)
        leds_s = it1.radio("Leds Superiores", ["Perfecto", "Falla"])
        t_izq = it2.radio("Totem Izquierdo", ["Perfecto", "Falla"])
        t_der = it3.radio("Totem Derecho", ["Perfecto", "Falla"])
        tv_izq = it4.radio("TV Izquierdo", ["Perfecto", "Falla"])
        tv_der = it5.radio("TV Derecho", ["Perfecto", "Falla"])
        obs_pan = st.text_input("Observaciones Pantallas")
        st.markdown('</div>', unsafe_allow_html=True)

        # 5. OTROS Y MÁQUINAS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("⚙️ OTROS Y MÁQUINAS")
        o1, o2, o3, o4 = st.columns(4)
        internet = o1.radio("Internet", ["Perfecto", "Falla"])
        wifi = o2.radio("Wi-Fi Gratuito", ["Perfecto", "Falla"])
        lockers = o3.radio("Lockers", ["Perfecto", "Falla"])
        camaras = o4.radio("Cámaras", ["Perfecto", "Falla"])
        m1, m2 = st.columns(2)
        maq_izq = m1.radio("Máquina Izquierda", ["Perfecto", "Falla"])
        maq_der = m2.radio("Máquina Derecha", ["Perfecto", "Falla"])
        st.markdown('</div>', unsafe_allow_html=True)

        # 6. BRANDING Y LIMPIEZA
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("✨ BRANDING Y LIMPIEZA")
        b1, b2, b3, b4 = st.columns(4)
        branding = b1.radio("Branding", ["Perfecto", "Dañado", "Urge Cambio"])
        l_int = b2.radio("Limpieza Interna", ["Perfecto", "Sucio"])
        l_ext = b3.radio("Limpieza Externa", ["Perfecto", "Sucio"])
        l_vis = b4.radio("Leds Visuales", ["Perfecto", "Falla"])
        st.markdown('</div>', unsafe_allow_html=True)

        # 7. GENERAL Y FOTOS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📝 OBSERVACIONES FINALES")
        obs_gen = st.text_area("Describa sus observaciones generales *")
        uploaded_images = st.file_uploader("Sube entre 5 y 10 fotos", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        st.markdown('</div>', unsafe_allow_html=True)

        # EL BOTÓN DEBE ESTAR AQUÍ DENTRO
        submit = st.form_submit_button("✅ ENVIAR REPORTE COMPLETO")

    # PROCESAMIENTO
    if submit:
        if not tecnico or not uploaded_images:
            st.warning("⚠️ El nombre y las fotos son obligatorios.")
        else:
            links_fotos = []
            with st.spinner("Enviando reporte..."):
                for file in uploaded_images[:10]:
                    try:
                        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(file.read()).decode('utf-8')}
                        res = requests.post("https://api.imgbb.com/1/upload", payload)
                        if res.status_code == 200: links_fotos.append(res.json()['data']['url'])
                    except: pass
                
                data_to_send = {
                    "action": "insertar",
                    "tecnico": tecnico, "ubicacion": ubicacion,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina, "obs_int": obs_int,
                    "leds_s": leds_s, "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der, "obs_pan": obs_pan,
                    "internet": internet, "wifi": wifi, "lockers": lockers, "camaras": camaras, "boton": "N/A", "obs_otros": "N/A",
                    "m_izq": maq_izq, "m_der": maq_der, "obs_maq": "N/A",
                    "branding": branding, "l_int": l_int, "l_ext": l_ext, "l_vis": l_vis, "obs_mod": "N/A",
                    "obs_gen": obs_gen, "fotos": ";".join(links_fotos)
                }
                
                try:
                    resp = requests.post(URL_BRIDGE, json=data_to_send)
                    if resp.status_code == 200:
                        st.success("¡Reporte guardado exitosamente!")
                        st.balloons()
                except: st.error("Error al conectar con la base de datos.")

# --- PARTE 2: DASHBOARD ---
with tab2:
    st.title("🛠️ Panel de Gestión")
    if st.button("🔄 Sincronizar"):
        try:
            r = requests.get(URL_BRIDGE)
            data = r.json()
            if len(data) > 1:
                df = pd.DataFrame(data[1:], columns=data[0])
                for idx, row in df.iterrows():
                    with st.expander(f"📍 {row['Ubicacion']} - {row['Fecha']}"):
                        st.write(f"**Técnico:** {row['Tecnico']}")
                        st.write(f"**Obs:** {row['Obs_Generales']}")
                        if row['Fotos']:
                            st.image(str(row['Fotos']).split(";"), width=300)
            else: st.info("No hay reportes.")
        except: st.error("Error de conexión.")
