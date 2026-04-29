import streamlit as st
import requests
import base64
import pandas as pd

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwZHc5UdHwbx52lgLWL5_LPDEuDjft7_yWbDuR1lDyOZk05h3G4bKfwHjJuHpziNjTS/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

st.set_page_config(page_title="Kioscos IA - Gestión", layout="wide")

# Estilo Neón Kioscos IA
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .main-nav { background-color: #0f172a; padding: 20px; border-radius: 15px; border: 1px solid #00d4ff; margin-bottom: 30px; text-align: center; }
    .report-box { background-color: #0f172a; padding: 25px; border-radius: 15px; border-left: 5px solid #00d4ff; border: 1px solid #1e293b; margin-bottom: 20px; }
    .section-header { color: #00d4ff; font-weight: bold; border-bottom: 1px solid #1e293b; margin-top: 15px; margin-bottom: 10px; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-nav"><h1>🚀 SISTEMA KIOSCOS IA</h1></div>', unsafe_allow_html=True)

# Menú lateral
menu = st.sidebar.radio("MÓDULO SELECCIONADO", ["SUPERVISOR (Ingreso)", "REPORTES (Consulta)"])

# --- MODULO 1: SUPERVISOR ---
if menu == "SUPERVISOR (Ingreso)":
    st.header("📝 Registro de Inspección")
    with st.form("form_sup", clear_on_submit=True):
        c1, c2 = st.columns(2)
        tec = c1.text_input("Técnico Responsable *")
        ubi = c2.selectbox("Seleccione Kiosco *", ["LA PUNTA", "SALAVERRY", "JESUS MARIA", "MAGDALENA", "SURCO", "CHACARILLA"])
        
        st.markdown('<div class="section-header">🏗️ ESTRUCTURA Y PUERTAS</div>', unsafe_allow_html=True)
        col_p = st.columns(4)
        p_izq = col_p[0].radio("Piloto Izq", ["Perfecto", "Falla"], key="r1")
        c_der = col_p[1].radio("Copiloto Der", ["Perfecto", "Falla"], key="r2")
        p_del = col_p[2].radio("Delantera", ["Perfecto", "Falla"], key="r3")
        p_pos = col_p[3].radio("Posterior", ["Perfecto", "Falla"], key="r4")
        obs_p = st.text_area("Notas de Puertas", key="t1")

        st.markdown('<div class="section-header">🖥️ SISTEMAS IT</div>', unsafe_allow_html=True)
        col_it = st.columns(3)
        t_izq = col_it[0].radio("Totem Izq", ["OK", "Falla"], key="r5")
        t_der = col_it[1].radio("Totem Der", ["OK", "Falla"], key="r6")
        tv_izq = col_it[2].radio("TV Principal", ["OK", "Falla"], key="r7")
        obs_pan = st.text_area("Notas IT / Pantallas", key="t2")

        st.subheader("📸 Evidencia y Finalización")
        obs_gen = st.text_area("Observaciones Generales del Supervisor *", key="t3")
        fotos_u = st.file_uploader("Subir fotos del módulo", accept_multiple_files=True)

        if st.form_submit_button("✅ ENVIAR REPORTE COMPLETO"):
            if not tec or not fotos_u:
                st.error("⚠️ El nombre y las fotos son obligatorios.")
            else:
                with st.spinner("Subiendo datos al sistema..."):
                    links = []
                    for img in fotos_u[:10]:
                        try:
                            # URL dividida para evitar el SyntaxError de línea larga
                            api_url = "https://api.imgbb.com/1/upload"
                            b64_img = base64.b64encode(img.read()).decode('utf-8')
                            res = requests.post(api_url, data={"key": IMGBB_API_KEY, "image": b64_img})
                            if res.status_code == 200:
                                links.append(res.json()['data']['url'])
                        except:
                            pass
                    
                    payload = {
                        "action": "insertar", "tecnico": tec, "ubicacion": ubi,
                        "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                        "muebles": "OK", "cableado": "OK", "energia": "OK", "iluminacion": "OK", "obs_int": "N/A",
                        "leds_s": "OK", "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": "OK", "obs_pan": obs_pan,
                        "internet": "OK", "wifi": "OK", "lockers": "OK", "camaras": "OK", "m_izq": "OK", "m_der": "OK",
                        "branding": "OK", "l_int": "OK", "l_ext": "OK", "l_vis": "OK", "obs_mod": "N/A",
                        "obs_gen": obs_gen, "fotos": ";".join(links), "boton": "OK"
                    }
                    try:
                        requests.post(URL_BRIDGE, json=payload, timeout=20)
                        st.success("¡Reporte guardado exitosamente en el Excel!")
                        st.balloons()
                    except:
                        st.error("Error al conectar con la base de datos.")

# --- MODULO 2: REPORTES ---
else:
    st.header("📊 Consulta de Reportes")
    try:
        r = requests.get(URL_BRIDGE, timeout=15)
        if r.text.strip().startswith("<!DOCTYPE"):
            st.error("Error de permisos en Google Sheets. Revisa la configuración 'Anyone'.")
        else:
            data = r.json()
            if len(data) > 1:
                df = pd.DataFrame(data[1:], columns=data[0])
                
                f1, f2 = st.columns(2)
                sel_k = f1.selectbox("Filtrar por Kiosco", df['Ubicación'].unique())
                df_k = df[df['Ubicación'] == sel_k]
                sel_f = f2.selectbox("Seleccionar Fecha", df_k['Fecha'].unique())
                
                rep = df_k[df_k['Fecha'] == sel_f].iloc[0]
                
                st.markdown('<div class="report-box">', unsafe_allow_html=True)
                st.subheader(f"📍 DETALLE DE INSPECCIÓN: {sel_k}")
                st.write(f"**Técnico:** {rep['Técnico']} | **Fecha:** {sel_f}")
                
                st.markdown('<div class="section-header">⚙️ ESTADO MECÁNICO</div>', unsafe_allow_html=True)
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Piloto Izq", rep['Piloto Izquierdo'])
                m2.metric("Copiloto Der", rep['Copiloto Derecho'])
                m3.metric("Delantera", rep['Delantera'])
                m4.metric("Posterior", rep['Posterior'])
                
                st.markdown('<div class="section-header">🖥️ SISTEMAS DIGITALES</div>', unsafe_allow_html=True)
                i1, i2, i3 = st.columns(3)
                i1.metric("Totem Izq", rep['Totem Izquierdo'])
                i2.metric("Totem Der", rep['Totem Derecho'])
                i3.metric("TV Principal", rep['TV Izquierdo'])

                st.markdown('<div class="section-header">📝 CONCLUSIONES</div>', unsafe_allow_html=True)
                st.info(rep['Obs Generales'])
                
                if rep['Fotos']:
                    st.markdown('<div class="section-header">📸 EVIDENCIA VISUAL</div>', unsafe_allow_html=True)
                    st.image(str(rep['Fotos']).split(";"), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No hay datos registrados aún.")
    except Exception as e:
        st.error(f"Error al cargar reportes: {e}")
