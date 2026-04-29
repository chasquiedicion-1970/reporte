import streamlit as st
import requests
import base64
import pandas as pd

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwZHc5UdHwbx52lgLWL5_LPDEuDjft7_yWbDuR1lDyOZk05h3G4bKfwHjJuHpziNjTS/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

st.set_page_config(page_title="Kioscos IA - Gestión Integral", layout="wide")

# Estilo Visual
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .main-nav { background-color: #0f172a; padding: 20px; border-radius: 15px; border: 1px solid #00d4ff; margin-bottom: 30px; text-align: center; }
    .report-box { background-color: #0f172a; padding: 25px; border-radius: 15px; border-left: 5px solid #00d4ff; border: 1px solid #1e293b; margin-bottom: 20px; }
    .section-header { color: #00d4ff; font-weight: bold; border-bottom: 1px solid #1e293b; margin-top: 15px; margin-bottom: 10px; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-nav"><h1>🚀 SISTEMA KIOSCOS IA</h1></div>', unsafe_allow_html=True)
menu = st.sidebar.radio("MÓDULO SELECCIONADO", ["SUPERVISOR (Ingreso)", "REPORTES (Consulta)"])

# --- MÓDULO 1: SUPERVISOR (TODO EL FORMULARIO) ---
if menu == "SUPERVISOR (Ingreso)":
    st.header("📝 Registro Completo de Inspección")
    with st.form("form_sup_completo", clear_on_submit=True):
        c1, c2 = st.columns(2)
        tec = c1.text_input("Técnico Responsable *")
        ubi = c2.selectbox("Seleccione Kiosco *", ["LA PUNTA", "SALAVERRY", "JESUS MARIA", "MAGDALENA", "SURCO", "CHACARILLA"])
        
        # 1. ESTRUCTURA
        st.markdown('<div class="section-header">🏗️ ESTRUCTURA Y PUERTAS</div>', unsafe_allow_html=True)
        col_p = st.columns(4)
        p_izq = col_p[0].radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = col_p[1].radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = col_p[2].radio("Delantera", ["Perfecto", "Falla"])
        p_pos = col_p[3].radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Notas de Puertas", key="t_p")

        # 2. INTERIORES Y ENERGÍA
        st.markdown('<div class="section-header">🏠 INTERIORES Y ENERGÍA</div>', unsafe_allow_html=True)
        col_i = st.columns(4)
        muebles = col_i[0].radio("Muebles", ["OK", "Falla"])
        cableado = col_i[1].radio("Cableado", ["OK", "Falla"])
        energia = col_i[2].radio("Energía", ["OK", "Falla"])
        ilumina = col_i[3].radio("Iluminación", ["OK", "Falla"])
        obs_int = st.text_area("Notas Interiores", key="t_i")

        # 3. IT PANTALLAS
        st.markdown('<div class="section-header">🖥️ SISTEMAS IT</div>', unsafe_allow_html=True)
        col_it = st.columns(3)
        t_izq = col_it[0].radio("Totem Izq", ["OK", "Falla"])
        t_der = col_it[1].radio("Totem Der", ["OK", "Falla"])
        tv_izq = col_it[2].radio("TV Principal", ["OK", "Falla"])
        obs_pan = st.text_area("Notas IT / Pantallas", key="t_it")

        # 4. LIMPIEZA Y BRANDING
        st.markdown('<div class="section-header">✨ LIMPIEZA Y BRANDING</div>', unsafe_allow_html=True)
        col_l = st.columns(3)
        branding = col_l[0].radio("Branding", ["Perfecto", "Dañado"])
        l_int = col_l[1].radio("Limp. Interna", ["Limpio", "Sucio"])
        l_ext = col_l[2].radio("Limp. Externa", ["Limpio", "Sucio"])
        obs_mod = st.text_area("Notas de Branding/Limpieza", key="t_mod")

        st.subheader("📸 Evidencia y Finalización")
        obs_gen = st.text_area("Comentarios Finales del Supervisor *")
        fotos_u = st.file_uploader("Subir fotos", accept_multiple_files=True)

        if st.form_submit_button("✅ ENVIAR REPORTE AL EXCEL"):
            if not tec or not fotos_u:
                st.error("⚠️ El nombre y las fotos son obligatorios.")
            else:
                with st.spinner("Guardando reporte..."):
                    links = []
                    for img in fotos_u[:10]:
                        try:
                            res = requests.post("https://api.imgbb.com/1/upload", 
                                               data={"key": IMGBB_API_KEY, "image": base64.b64encode(img.read()).decode('utf-8')})
                            if res.status_code == 200: links.append(res.json()['data']['url'])
                        except: pass
                    
                    payload = {
                        "action": "insertar", "tecnico": tec, "ubicacion": ubi,
                        "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                        "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina, "obs_int": obs_int,
                        "leds_s": "OK", "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": "OK", "obs_pan": obs_pan,
                        "internet": "OK", "wifi": "OK", "lockers": "OK", "camaras": "OK", "m_izq": "OK", "m_der": "OK",
                        "branding": branding, "l_int": l_int, "l_ext": l_ext, "l_vis": "OK", "obs_mod": obs_mod,
                        "obs_gen": obs_gen, "fotos": ";".join(links), "boton": "OK"
                    }
                    try:
                        requests.post(URL_BRIDGE, json=payload, timeout=30)
                        st.success("¡Reporte guardado exitosamente!")
                        st.balloons()
                    except: st.error("Error de tiempo: El Excel tardó demasiado en responder.")

# --- MÓDULO 2: REPORTES (MÁS TIEMPO DE ESPERA) ---
else:
    st.header("📊 Historial de Reportes")
    try:
        # Aumentamos el timeout a 30 segundos para evitar el error de conexión
        r = requests.get(URL_BRIDGE, timeout=30)
        data = r.json()
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            f1, f2 = st.columns(2)
            sel_k = f1.selectbox("Filtrar por Kiosco", df['Ubicación'].unique())
            df_k = df[df['Ubicación'] == sel_k]
            sel_f = f2.selectbox("Seleccionar Fecha", df_k['Fecha'].unique())
            
            rep = df_k[df_k['Fecha'] == sel_f].iloc[0]
            
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.subheader(f"📍 REPORTE: {sel_k}")
            st.write(f"**Técnico:** {rep['Técnico']} | **Fecha:** {sel_f}")
            
            # Resumen Visual
            st.markdown('<div class="section-header">⚙️ ESTRUCTURA Y SISTEMAS</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("Energía", rep.get('Energía', 'N/A'))
            c2.metric("Iluminación", rep.get('Iluminación', 'N/A'))
            c3.metric("TV Principal", rep.get('TV Izquierdo', 'N/A'))

            st.markdown('<div class="section-header">📝 OBSERVACIONES GENERALES</div>', unsafe_allow_html=True)
            st.info(rep['Obs Generales'])
            
            if rep['Fotos']:
                st.markdown('<div class="section-header">📸 EVIDENCIA VISUAL</div>', unsafe_allow_html=True)
                st.image(str(rep['Fotos']).split(";"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else: st.warning("Sin datos en el Excel.")
    except Exception as e:
        st.error(f"Error de conexión: {e}. Intenta sincronizar de nuevo.")
