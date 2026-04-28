import streamlit as st
import requests
import base64
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbzvBhp7v71nPCS3-E8QD67OqeK4P4nefxnqA6cXQczbCPlbCuQ1BunSnL2dLN5Yo5ej/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

st.set_page_config(page_title="Kioscos IA - Operaciones", layout="wide")

# Estilo Dark Neón
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .section-card { background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 20px; }
    .stTabs [aria-selected="true"] { background-color: #00d4ff !important; color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 REGISTRO DE INSPECCIÓN", "🛠️ DASHBOARD TÉCNICO"])

# --- PARTE 1: REGISTRO ---
with tab1:
    st.title("📋 Reporte Integral de Visita")
    
    with st.form("main_form", clear_on_submit=True):
        
        # 1. INFO GENERAL
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📍 Información General")
        c1, c2 = st.columns(2)
        tecnico = c1.text_input("1. TU NOMBRE *")
        ubicacion = c2.selectbox("3. UBICACIÓN DEL MODULO *", [
            "LA PUNTA", "SALAVERRY REAL PLAZA (JESUS MARIA)", "PERSHING - DOMINGO ORUE (JESUS MARIA)", 
            "ARENALES - DOMINGO CUETO (JESUS MARIA)", "VIVANDA JAVIER PRADO (MAGDALENA)", 
            "PASTIPAN JAVIER PRADO (MAGDALENA)", "U: RICARDO PALMA (SURCO)", "CHACARILLA (SURCO)"
        ])
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. ESTRUCTURA Y PUERTAS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏗️ 4. ESTRUCTURA - PUERTAS")
        cp1, cp2, cp3, cp4 = st.columns(4)
        p_izq = cp1.radio("Piloto Izquierdo", ["Perfecto", "Con Problemas", "No Funciona"])
        c_der = cp2.radio("Copiloto Derecho", ["Perfecto", "Con Problemas", "No Funciona"])
        p_del = cp3.radio("Delantera", ["Perfecto", "Con Problemas", "No Funciona"])
        p_pos = cp4.radio("Posterior", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_p = st.text_input("5. OBSERVACIONES PUERTAS")
        
        st.subheader("🏠 6. INTERIORES")
        ci1, ci2, ci3, ci4 = st.columns(4)
        muebles = ci1.radio("Muebles", ["Perfecto", "Con Problemas", "No Funciona"])
        cableado = ci2.radio("Cableado", ["Perfecto", "Con Problemas", "No Funciona"])
        energia = ci3.radio("Energía", ["Perfecto", "Con Problemas", "No Funciona"])
        ilumina = ci4.radio("Iluminación", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_int = st.text_input("7. OBSERVACIONES INTERIORES")
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. PANTALLAS (IT)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🖥️ 8. PANTALLAS (IT)")
        it1, it2, it3, it4, it5 = st.columns(5)
        leds_s = it1.radio("Leds Superiores", ["Perfecto", "Con Problemas", "No Funciona"])
        t_izq = it2.radio("Totem Izquierdo", ["Perfecto", "Con Problemas", "No Funciona"])
        t_der = it3.radio("Totem Derecho", ["Perfecto", "Con Problemas", "No Funciona"])
        tv_izq = it4.radio("TV Izquierdo", ["Perfecto", "Con Problemas", "No Funciona"])
        tv_der = it5.radio("TV Derecho", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_pan = st.text_input("9. OBSERVACIONES PANTALLAS")
        st.markdown('</div>', unsafe_allow_html=True)

        # 4. OTROS Y MAQUINAS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("⚙️ 10. OTROS")
        o1, o2, o3, o4, o5 = st.columns(5)
        internet = o1.radio("Internet", ["Perfecto", "Con Problemas", "No Funciona"])
        wifi = o2.radio("Wi-Fi Gratuito", ["Perfecto", "Con Problemas", "No Funciona"])
        lockers = o3.radio("Lockers", ["Perfecto", "Con Problemas", "No Funciona"])
        camaras = o4.radio("Cámaras Seguridad", ["Perfecto", "Con Problemas", "No Funciona"])
        boton = o5.radio("Botón de Pánico", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_otros = st.text_input("11. OBSERVACIONES OTROS")
        
        st.subheader("🥤 12. MAQUINAS EXPENDEDORAS")
        m1, m2 = st.columns(2)
        maq_izq = m1.radio("Máquina Izquierda", ["Perfecto", "Con Problemas", "No Funciona"])
        maq_der = m2.radio("Máquina Derecho", ["Perfecto", "Con Problemas", "No Funciona"])
        obs_maq = st.text_input("13. OBSERVACIONES MAQUINAS")
        st.markdown('</div>', unsafe_allow_html=True)

        # 5. BRANDING Y LIMPIEZA
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("✨ 14. BRANDING Y LIMPIEZA")
        b1, b2, b3, b4 = st.columns(4)
        branding = b1.radio("Branding", ["Perfecto", "Sucio/Roto", "Urge Cambio"])
        l_int = b2.radio("Limpieza Interna", ["Perfecto", "Sucio/Roto", "Urge Cambio"])
        l_ext = b3.radio("Limpieza Externa", ["Perfecto", "Sucio/Roto", "Urge Cambio"])
        l_vis = b4.radio("Leds Visuales", ["Perfecto", "Sucio/Roto", "Urge Cambio"])
        obs_mod = st.text_input("15. OBSERVACIONES ESTADO MODULO")
        st.markdown('</div>', unsafe_allow_html=True)

        # 6. GENERAL Y FOTOS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📝 16. OBSERVACIONES GENERALES")
        obs_gen = st.text_area("Describa sus observaciones generales luego de la visita *")
        
        st.subheader("📸 REGISTRO FOTOGRÁFICO")
        uploaded_images = st.file_uploader("Sube entre 5 y 10 fotos", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        st.markdown('</div>', unsafe_allow_html=True)

        # BOTÓN CORRECTO: st.form_submit_button
        submit = st.form_submit_button("✅ ENVIAR REPORTE COMPLETO")

    # Lógica de procesamiento al enviar
    if submit:
        if not tecnico or not obs_gen or not uploaded_images:
            st.warning("⚠️ Debes completar tu nombre, las observaciones finales y las fotos.")
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
                
                # Datos organizados para Google
                data_json = {
                    "action": "insertar",
                    "tecnico": tecnico, "ubicacion": ubicacion,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina, "obs_int": obs_int,
                    "leds_s": leds_s, "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der, "obs_pan": obs_pan,
                    "internet": internet, "wifi": wifi, "lockers": lockers, "camaras": camaras, "boton": boton, "obs_otros": obs_otros,
                    "m_izq": maq_izq, "m_der": maq_der, "obs_maq": obs_maq,
                    "branding": branding, "l_int": l_int, "l_ext": l_ext, "l_vis": l_vis, "obs_mod": obs_mod,
                    "obs_gen": obs_gen, "fotos": ";".join(links_fotos)
                }
                
                try:
                    r = requests.post(URL_BRIDGE, json=data_json)
                    if r.status_code == 200:
                        st.success("¡Reporte guardado con éxito!")
                        st.balloons()
                except:
                    st.error("Error al conectar con la base de datos.")

# --- PARTE 2: DASHBOARD TÉCNICO ---
with tab2:
    st.title("🛠️ Gestión Técnica")
    if st.button("🔄 Actualizar Datos"):
        try:
            r = requests.get(URL_BRIDGE)
            data = r.json()
            if len(data) > 1:
                df = pd.DataFrame(data[1:], columns=data[0])
                for index, row in df.iterrows():
                    with st.expander(f"📍 {row['Ubicacion']} - {row['Fecha']}"):
                        st.write(f"**Técnico:** {row['Tecnico']}")
                        st.write(f"**Obs:** {row['Obs_Generales']}")
                        if row['Fotos']:
                            st.image(str(row['Fotos']).split(";"), width=200)
            else: st.info("No hay reportes registrados.")
        except: st.error("No se pudo leer la base de datos.")
