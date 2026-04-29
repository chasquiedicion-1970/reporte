import streamlit as st
import requests
import base64
import pandas as pd

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbzfsGoonaLWGVimiPS_v6ZPI_X3RiBQwNFZmJnpSoG0IWBwgLYsIOP_MFAyWHPQG2GZ/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

st.set_page_config(page_title="Kioscos IA - Sistema Integral", layout="wide")

# Estilo Neón
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .main-nav { background-color: #0f172a; padding: 20px; border-radius: 15px; border: 1px solid #00d4ff; margin-bottom: 30px; text-align: center; }
    .report-card { background-color: #0f172a; padding: 25px; border-radius: 15px; border: 1px solid #1e293b; border-left: 5px solid #00d4ff; }
    .section-header { color: #00d4ff; font-weight: bold; border-bottom: 1px solid #1e293b; margin-top: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-nav"><h1>🚀 SISTEMA KIOSCOS IA</h1></div>', unsafe_allow_html=True)
menu = st.radio("SELECCIONE MÓDULO:", ["SUPERVISOR (Ingreso)", "REPORTES (Consulta)"], horizontal=True)

# --- MÓDULO 1: SUPERVISOR (INGRESO) ---
if menu == "SUPERVISOR (Ingreso)":
    st.header("📝 Registro de Inspección")
    with st.form("form_supervisor", clear_on_submit=True):
        col1, col2 = st.columns(2)
        tecnico = col1.text_input("Nombre del Técnico *")
        ubicacion = col2.selectbox("Ubicación del Módulo *", ["LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", "PASTIPAN JAVIER PRADO", "U: RICARDO PALMA", "CHACARILLA"])
        
        st.markdown('<div class="section-header">🏗️ Estructura y Puertas</div>', unsafe_allow_html=True)
        p1, p2, p3, p4 = st.columns(4)
        p_izq = p1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = p2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = p3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = p4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Notas Puertas", key="n_p")

        st.markdown('<div class="section-header">🏠 Interiores y Energía</div>', unsafe_allow_html=True)
        i1, i2, i3, i4 = st.columns(4)
        muebles = i1.radio("Muebles", ["OK", "Falla"])
        cableado = i2.radio("Cableado", ["OK", "Falla"])
        energia = i3.radio("Energía", ["OK", "Falla"])
        ilumina = i4.radio("Iluminación", ["OK", "Falla"])
        obs_int = st.text_area("Notas Interiores", key="n_i")

        st.markdown('<div class="section-header">🖥️ Pantallas e IT</div>', unsafe_allow_html=True)
        it1, it2, it3 = st.columns(3)
        t_izq = it1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it3.radio("TV Principal", ["OK", "Falla"])
        obs_pan = st.text_area("Notas IT", key="n_it")

        st.markdown('<div class="section-header">📸 Evidencia Fotografica</div>', unsafe_allow_html=True)
        obs_gen = st.text_area("Comentarios Finales del Supervisor *")
        uploaded_images = st.file_uploader("Subir fotos", accept_multiple_files=True)

        submit = st.form_submit_button("✅ ENVIAR REPORTE")

    if submit:
        if not tecnico or not uploaded_images:
            st.error("⚠️ Nombre y fotos obligatorios.")
        else:
            with st.spinner("Enviando datos..."):
                links = []
                for img in uploaded_images[:10]:
                    try:
                        res = requests.post("https://api.imgbb.com/1/upload", {"key": IMGBB_API_KEY, "image": base64.b64encode(img.read()).decode('utf-8')})
                        if res.status_code == 200: links.append(res.json()['data']['url'])
                    except: pass
                
                payload = {
                    "action": "insertar", "tecnico": tecnico, "ubicacion": ubicacion,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina, "obs_int": obs_int,
                    "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "obs_pan": obs_pan,
                    "obs_gen": obs_gen, "fotos": ";".join(links)
                }
                requests.post(URL_BRIDGE, json=payload)
                st.success("¡Reporte Guardado!")

# --- MÓDULO 2: REPORTES (CONSULTA) ---
else:
    st.header("📊 Consulta Histórica")
    try:
        response = requests.get(URL_BRIDGE, timeout=15)
        if response.text.strip().startswith("<!DOCTYPE"):
            st.error("Error de acceso: El script requiere autorización 'Anyone'.")
        else:
            data = response.json()
            if len(data) > 1:
                df = pd.DataFrame(data[1:], columns=data[0])
                
                # Buscamos columnas de ubicación y fecha (independiente de la tilde)
                col_ubi = [c for c in df.columns if 'Ubic' in c][0]
                col_fec = [c for c in df.columns if 'Fecha' in c][0]

                c1, c2 = st.columns(2)
                sel_k = c1.selectbox("Filtrar por Kiosco:", df[col_ubi].unique())
                df_k = df[df[col_ubi] == sel_k]
                sel_f = c2.selectbox("Seleccionar Fecha de Reporte:", df_k[col_fec].unique())
                
                # Extraer fila seleccionada
                rep = df_k[df_k[col_fec] == sel_f].iloc[0]
                
                # --- DISEÑO DEL INFORME ---
                st.markdown('<div class="report-card">', unsafe_allow_html=True)
                st.subheader(f"📍 REPORTE TÉCNICO: {sel_k}")
                st.write(f"**Técnico:** {rep.get('Técnico', 'N/A')} | **Fecha:** {sel_f}")
                
                # Sección 1: Estructura
                st.markdown('<div class="section-header">⚙️ ESTRUCTURA Y PUERTAS</div>', unsafe_allow_html=True)
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Piloto Izq", rep.get('Piloto Izquierdo', 'N/A'))
                m2.metric("Copiloto Der", rep.get('Copiloto Derecho', 'N/A'))
                m3.metric("Delantera", rep.get('Delantera', 'N/A'))
                m4.metric("Posterior", rep.get('Posterior', 'N/A'))
                st.write(f"**Notas:** {rep.get('Obs Puertas', 'Sin comentarios')}")

                # Sección 2: Interior y Energía
                st.markdown('<div class="section-header">🏠 INTERIORES Y ENERGÍA</div>', unsafe_allow_html=True)
                i1, i2, i3, i4 = st.columns(4)
                i1.metric("Muebles", rep.get('Muebles', 'N/A'))
                i2.metric("Cableado", rep.get('Cableado', 'N/A'))
                i3.metric("Energía", rep.get('Energía', 'N/A'))
                i4.metric("Iluminación", rep.get('Iluminación', 'N/A'))
                st.write(f"**Notas:** {rep.get('Obs Interiores', 'Sin comentarios')}")

                # Sección 3: Pantallas
                st.markdown('<div class="section-header">🖥️ SISTEMAS IT</div>', unsafe_allow_html=True)
                it_c1, it_c2, it_c3 = st.columns(3)
                it_c1.metric("Tótem Izq", rep.get('Totem Izquierdo', 'N/A'))
                it_c2.metric("Tótem Der", rep.get('Totem Derecho', 'N/A'))
                it_c3.metric("TV Principal", rep.get('TV Izquierdo', 'N/A'))

                # Sección 4: Observaciones Finales
                st.markdown('<div class="section-header">📝 CONCLUSIONES DEL SUPERVISOR</div>', unsafe_allow_html=True)
                st.info(rep.get('Obs Generales', 'Sin observaciones finales registrados.'))

                # Sección 5: Galería
                if rep.get('Fotos'):
                    st.markdown('<div class="section-header">📸 EVIDENCIA FOTOGRÁFICA</div>', unsafe_allow_html=True)
                    st.image(str(rep['Fotos']).split(";"), use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("La base de datos está vacía. Ingrese un reporte primero.")
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
