import streamlit as st
import requests
import base64
import pandas as pd

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbzfsGoonaLWGVimiPS_v6ZPI_X3RiBQwNFZmJnpSoG0IWBwgLYsIOP_MFAyWHPQG2GZ/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

st.set_page_config(page_title="Kioscos IA - Sistema Integral", layout="wide")

# Estilo Neón Kioscos IA
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .main-nav { background-color: #0f172a; padding: 20px; border-radius: 15px; border: 1px solid #00d4ff; margin-bottom: 30px; text-align: center; }
    .report-box { background-color: #0f172a; padding: 25px; border-radius: 15px; border-left: 5px solid #00d4ff; margin-bottom: 20px; }
    .section-header { color: #00d4ff; font-weight: bold; border-bottom: 1px solid #1e293b; margin-top: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN PRINCIPAL ---
st.markdown('<div class="main-nav"><h1>🚀 SISTEMA KIOSCOS IA</h1></div>', unsafe_allow_html=True)
menu = st.radio("SELECCIONE MÓDULO:", ["SUPERVISOR (Ingreso)", "REPORTES (Visualización)"], horizontal=True)

# --- MÓDULO 1: SUPERVISOR ---
if menu == "SUPERVISOR (Ingreso)":
    st.header("📝 Registro de Inspección")
    with st.form("form_supervisor", clear_on_submit=True):
        col1, col2 = st.columns(2)
        tecnico = col1.text_input("Nombre del Técnico *")
        ubicacion = col2.selectbox("Ubicación del Kiosco *", [
            "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
            "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", 
            "PASTIPAN JAVIER PRADO", "U: RICARDO PALMA", "CHACARILLA"
        ])
        
        st.subheader("🏗️ Estructura y Puertas")
        p1, p2, p3, p4 = st.columns(4)
        p_izq = p1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = p2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = p3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = p4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Observaciones Puertas", key="obs_p")

        st.subheader("🖥️ Pantallas e IT")
        it1, it2, it3 = st.columns(3)
        t_izq = it1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it3.radio("TV Principal", ["OK", "Falla"])
        obs_pan = st.text_area("Observaciones Pantallas", key="obs_pan")

        st.subheader("📸 Evidencia Fotografica")
        obs_gen = st.text_area("Observaciones Generales *")
        uploaded_images = st.file_uploader("Subir fotos (Máx 10)", accept_multiple_files=True)

        if st.form_submit_button("✅ ENVIAR REPORTE"):
            if not tecnico or not uploaded_images:
                st.error("Faltan datos obligatorios.")
            else:
                with st.spinner("Subiendo datos..."):
                    links = []
                    for img in uploaded_images[:10]:
                        res = requests.post("https://api.imgbb.com/1/upload", {"key": IMGBB_API_KEY, "image": base64.b64encode(img.read()).decode('utf-8')})
                        if res.status_code == 200: links.append(res.json()['data']['url'])
                    
                    payload = {
                        "action": "insertar", "tecnico": tecnico, "ubicacion": ubicacion,
                        "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                        "muebles": "OK", "cableado": "OK", "energia": "OK", "ilumina": "OK", "obs_int": "N/A",
                        "leds_s": "OK", "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": "OK", "obs_pan": obs_pan,
                        "internet": "OK", "wifi": "OK", "lockers": "OK", "camaras": "OK", "m_izq": "OK", "m_der": "OK",
                        "branding": "OK", "l_int": "OK", "l_ext": "OK", "l_vis": "OK", "obs_mod": "N/A",
                        "obs_gen": obs_gen, "fotos": ";".join(links), "boton": "OK"
                    }
                    requests.post(URL_BRIDGE, json=payload)
                    st.success("¡Reporte Guardado!")

# --- MÓDULO 2: REPORTES (Estilo V9) ---
else:
    st.header("📊 Consulta de Reportes")
    
    # Intentar cargar datos del Excel
    try:
        r = requests.get(URL_BRIDGE)
        data = r.json()
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            
            # Filtros de búsqueda
            col_filt1, col_filt2 = st.columns(2)
            kiosco_sel = col_filt1.selectbox("Seleccione Kiosco:", df['Ubicación'].unique())
            
            # Filtrar fechas disponibles para ese kiosco
            df_kiosco = df[df['Ubicación'] == kiosco_sel]
            fecha_sel = col_filt2.selectbox("Seleccione Fecha de Reporte:", df_kiosco['Fecha'].unique())
            
            # Obtener el reporte específico
            reporte = df_kiosco[df_kiosco['Fecha'] == fecha_sel].iloc[0]
            
            # DESPLIEGUE ESTILO REPORTE V9
            st.markdown(f'<div class="report-box">', unsafe_allow_html=True)
            st.write(f"### REPORTE: {kiosco_sel}")
            st.write(f"**Fecha:** {fecha_sel} | **Técnico Responsable:** {reporte['Técnico']}")
            
            st.markdown('<div class="section-header">ESTRUCTURA Y PUERTAS</div>', unsafe_allow_html=True)
            c
