import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
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

tab1, tab2 = st.tabs(["REGISTRO DE INSPECCION", "DASHBOARD TECNICO"])

# --- PARTE 1: INGRESO DE DATOS ---
with tab1:
    st.title("Reporte Integral de Visita")
    
    with st.form("main_form", clear_on_submit=True):
        # 1. INFO GENERAL
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("1. Informacion General")
        c1, c2 = st.columns(2)
        tecnico = c1.text_input("Nombre del Tecnico *")
        ubicacion = c2.selectbox("Ubicacion del Modulo *", [
            "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
            "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", 
            "PASTIPAN JAVIER PRADO", "U: RICARDO PALMA", "CHACARILLA"
        ])
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. ESTRUCTURA
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("2. Estructura y Puertas")
        cp1, cp2, cp3, cp4 = st.columns(4)
        p_izq = cp1.radio("Piloto Izquierdo", ["Perfecto", "Problemas", "Falla"])
        c_der = cp2.radio("Copiloto Derecho", ["Perfecto", "Problemas", "Falla"])
        p_del = cp3.radio("Delantera", ["Perfecto", "Problemas", "Falla"])
        p_pos = cp4.radio("Posterior", ["Perfecto", "Problemas", "Falla"])
        obs_p = st.text_input("Observaciones Puertas")
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. INTERIORES
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("3. Interiores")
        ci1, ci2, ci3, ci4 = st.columns(4)
        muebles = ci1.radio("Muebles", ["OK", "Falla"])
        cableado = ci2.radio("Cableado", ["OK", "Falla"])
        energia = ci3.radio("Energia", ["OK", "Falla"])
        ilumina = ci4.radio("Iluminacion", ["OK", "Falla"])
        obs_int = st.text_input("Observaciones Interiores")
        st.markdown('</div>', unsafe_allow_html=True)

        # 4. IT PANTALLAS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("4. Pantallas IT")
        it1, it2, it3, it4, it5 = st.columns(5)
        leds_s = it1.radio("Leds Sup", ["OK", "Falla"])
        t_izq = it2.radio("Totem Izq", ["OK", "Falla"])
        t_der = it3.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it4.radio("TV Izq", ["OK", "Falla"])
        tv_der = it5.radio("TV Der", ["OK", "Falla"])
        obs_pan = st.text_input("Observaciones Pantallas")
        st.markdown('</div>', unsafe_allow_html=True)

        # 5. SISTEMAS Y MAQUINAS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("5. Sistemas y Maquinas")
        o1, o2, o3, o4, o5 = st.columns(5)
        internet = o1.radio("Internet", ["OK", "Falla"])
        wifi = o2.radio("Wifi", ["OK", "Falla"])
        lockers = o3.radio("Lockers", ["OK", "Falla"])
        camaras = o4.radio("Camaras", ["OK", "Falla"])
        boton = o5.radio("Boton Panico", ["OK", "Falla"])
        m_izq = st.radio("Maquina Izquierda", ["OK", "Falla"], horizontal=True)
        m_der = st.radio("Maquina Derecha", ["OK", "Falla"], horizontal=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 6. BRANDING Y LIMPIEZA
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("6. Branding y Limpieza")
        b1, b2, b3, b4 = st.columns(4)
        branding = b1.radio("Branding", ["Perfecto", "Danado", "Urge Cambio"])
        l_int = b2.radio("Limpieza Interna", ["OK", "Sucio"])
        l_ext = b3.radio("Limpieza Externa", ["OK", "Sucio"])
        l_vis = b4.radio("Leds Visuales", ["OK", "Falla"])
        obs_mod = st.text_input("Observaciones Modulo")
        st.markdown('</div>', unsafe_allow_html=True)

        # 7. FINAL
        st.subheader("Evidencia Fotografica")
        obs_gen = st.text_area("Observaciones Generales *")
        uploaded_images = st.file_uploader("Fotos (Max 10)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

        # EL BOTON DE ENVIO
        submit = st.form_submit_button("ENVIAR REPORTE")

    if submit:
        if not tecnico or not uploaded_images:
            st.warning("Nombre y fotos son obligatorios.")
        else:
            links_fotos = []
            with st.spinner("Enviando reporte..."):
                for file in uploaded_images[:10]:
                    try:
                        payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(file.read()).decode('utf-8')}
                        res = requests.post("https://api.imgbb.com/1/upload", payload)
                        if res.status_code == 200:
                            links_fotos.append(res.json()['data']['url'])
                    except: pass
                
                # Diccionario de datos para Google Sheets
                data_json = {
                    "action": "insertar",
                    "tecnico": tecnico,
                    "ubicacion": ubicacion,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina, "obs_int": obs_int,
                    "leds_s": leds_s, "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der, "obs_pan": obs_pan,
                    "internet": internet, "wifi": wifi, "lockers": lockers, "camaras": camaras, "m_izq": m_izq, "m_der": m_der,
                    "branding": branding, "l_int": l_int, "l_ext": l_ext, "l_vis": l_vis, "obs_mod": obs_mod,
                    "obs_gen": obs_gen, "fotos": ";".join(links_fotos), "boton": boton
                }
                
                try:
                    r = requests.post(URL_BRIDGE, json=data_json)
                    if r.status_code == 200:
                        st.success("Reporte guardado con exito!")
                        st.balloons()
                except:
                    st.error("Error de conexion con la base de datos.")

# --- PESTAÑA 2: DASHBOARD ---
with tab2:
    st.title("Gestion de Reportes")
    if st.button("Sincronizar"):
        try:
            r = requests.get(URL_BRIDGE)
            data = r.json()
            if len(data) > 1:
                df = pd.DataFrame(data[1:], columns=data[0])
                for idx, row in df.iterrows():
                    with st.expander(f"{row['Ubicación']} - {row['Fecha']}"):
                        st.write(f"Tecnico: {row['Técnico']}")
                        if row['Fotos']:
                            st.image(str(row['Fotos']).split(";"), width=200)
            else: st.info("Sin registros.")
        except: st.error("Error al leer datos.")
