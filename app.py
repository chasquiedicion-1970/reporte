import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE CONEXIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbzvBhp7v71nPCS3-E8QD67OqeK4P4nefxnqA6cXQczbCPlbCuQ1BunSnL2dLN5Yo5ej/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca" 

st.set_page_config(page_title="Kioscos IA - Gestión de Operaciones", layout="wide")

# Estilo Visual Kioscos IA (Dark Mode + Neón)
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #0f172a; border-radius: 5px; color: white; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #00d4ff !important; color: black !important; font-weight: bold; }
    .section-card { background: #0f172a; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 20px; }
    .neon-text { color: #00d4ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 REGISTRO DE INSPECCIÓN", "🛠️ DASHBOARD TÉCNICO"])

# --- PARTE 1: INGRESO DE DATOS (SUPERVISOR) ---
with tab1:
    st.title("📋 Nuevo Reporte de Visita")
    
    with st.form("main_form", clear_on_submit=True):
        # 1. Información General
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📍 Información General")
        c1, c2 = st.columns(2)
        tecnico = c1.text_input("1. Nombre del Técnico / Supervisor")
        ubicacion = c2.selectbox("3. Ubicación del Módulo", [
            "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
            "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", "PASTIPAN JAVIER PRADO",
            "U: RICARDO PALMA", "CHACARILLA", "JESUS MARIA", "MAGDALENA"
        ])
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. Estructura (Puertas y Fachada)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏗️ Estructura y Puertas")
        r1, r2, r3, r4 = st.columns(4)
        p_izq = r1.radio("Piloto Izquierdo", ["Perfecto", "Con Problemas", "No Funciona"])
        c_der = r2.radio("Copiloto Derecho", ["Perfecto", "Con Problemas", "No Funciona"])
        p_del = r3.radio("Delantera", ["Perfecto", "Con Problemas", "No Funciona"])
        p_pos = r4.radio("Posterior", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_p = st.text_input("Observaciones de Puertas / Fachada")
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. Pantallas e IT
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🖥️ Pantallas e IT")
        i1, i2, i3, i4 = st.columns(4)
        t_izq = i1.radio("Totem Izquierdo", ["Perfecto", "Falla"])
        t_der = i2.radio("Totem Derecho", ["Perfecto", "Falla"])
        tv_izq = i3.radio("TV Izquierdo", ["Perfecto", "Falla"])
        tv_der = i4.radio("TV Derecho", ["Perfecto", "Falla"])
        obs_pan = st.text_input("Observaciones de Pantallas")
        st.markdown('</div>', unsafe_allow_html=True)

        # 4. Fotos (Subida de 5 a 10)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📸 Registro Fotográfico")
        uploaded_images = st.file_uploader("Sube la evidencia (Mínimo 5 - Máximo 10)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        st.markdown('</div>', unsafe_allow_html=True)

        # Botón de Envío
        submit = st.form_submit_button("✅ FINALIZAR Y ENVIAR REPORTE")

        if submit:
            if not tecnico or not uploaded_images:
                st.warning("⚠️ Debes ingresar tu nombre y subir las fotos de evidencia.")
            else:
                links_fotos = []
                with st.spinner("Subiendo fotos a la nube..."):
                    for file in uploaded_images[:10]:
                        try:
                            payload = {"key": IMGBB_API_KEY, "image": base64.b64encode(file.read()).decode('utf-8')}
                            res = requests.post("https://api.imgbb.com/1/upload", payload)
                            if res.status_code == 200:
                                links_fotos.append(res.json()['data']['url'])
                        except: pass
                    
                    # Preparación de datos para el Puente de Google
                    data_to_send = {
                        "action": "insertar",
                        "tecnico": tecnico,
                        "ubicacion": ubicacion,
                        "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                        "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der, "obs_pan": obs_pan,
                        "fotos": ";".join(links_fotos)
                    }
                    
                    try:
                        resp = requests.post(URL_BRIDGE, json=data_to_send)
                        if resp.status_code == 200:
                            st.success("✅ ¡Datos y fotos guardados en Google Sheets!")
                            st.balloons()
                    except:
                        st.error("Error al conectar con el servidor de Google.")

# --- PARTE 2: VISUALIZACIÓN TÉCNICA ---
with tab2:
    st.title("🛠️ Panel de Control y Gestión")
    if st.button("🔄 Sincronizar con Base de Datos"):
        try:
            r = requests.get(URL_BRIDGE)
            data = r.json()
            if len(data) > 1:
                df_view = pd.DataFrame(data[1:], columns=data[0])
                for index, row in df_view.iterrows():
                    # Color según estado
                    estado = row['Estado_Gestion']
                    emoji = "🟢" if estado == "RESUELTO" else "🔴"
                    
                    with st.expander(f"{emoji} {row['Ubicacion']} - {row['Fecha']}"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write(f"**Técnico:** {row['Tecnico']}")
                            st.write(f"**Estado:** {estado}")
                            st.write(f"**Puertas:** {row['Piloto_Izquierdo']} / {row['Copiloto_Derecho']}")
                        with col_b:
                            st.write(f"**Obs:** {row['Obs_Puertas']}")
                        
                        if row['Fotos']:
                            st.markdown("---")
                            st.write("**Evidencia Fotográfica:**")
                            f_list = str(row['Fotos']).split(";")
                            st.image(f_list, width=250)
            else:
                st.info("No hay reportes previos.")
        except:
            st.error("Error al leer la base de datos.")
