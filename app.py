import streamlit as st
import requests
import base64
import pandas as pd

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbzfsGoonaLWGVimiPS_v6ZPI_X3RiBQwNFZmJnpSoG0IWBwgLYsIOP_MFAyWHPQG2GZ/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

st.set_page_config(page_title="Kioscos IA - Operaciones", layout="wide")

# Estilo
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .section-card { background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 REGISTRO DE INSPECCIÓN", "🛠️ DASHBOARD TÉCNICO"])

with tab1:
    st.title("Reporte Integral de Visita")
    
    with st.form("main_form", clear_on_submit=True):
        # 1. INFO GENERAL
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("1. Información General")
        c1, c2 = st.columns(2)
        tecnico = c1.text_input("Nombre del Técnico *", key="input_tec")
        ubicacion = c2.selectbox("Ubicación del Módulo *", [
            "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
            "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", 
            "PASTIPAN JAVIER PRADO", "U: RICARDO PALMA", "CHACARILLA"
        ])
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. ESTRUCTURA
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("2. Estructura y Puertas")
        cp1, cp2, cp3, cp4 = st.columns(4)
        p_izq = cp1.radio("Piloto Izquierdo", ["Perfecto", "Falla"])
        c_der = cp2.radio("Copiloto Derecho", ["Perfecto", "Falla"])
        p_del = cp3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = cp4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Observaciones de Puertas", placeholder="Escriba aquí los detalles de las puertas...", key="area_p")
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. INTERIORES
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("3. Interiores")
        ci1, ci2, ci3, ci4 = st.columns(4)
        muebles = ci1.radio("Muebles", ["OK", "Falla"])
        cableado = ci2.radio("Cableado", ["OK", "Falla"])
        energia = ci3.radio("Energía", ["OK", "Falla"])
        ilumina = ci4.radio("Iluminación", ["OK", "Falla"])
        obs_int = st.text_area("Observaciones de Interiores", placeholder="Escriba aquí los detalles del interior...", key="area_int")
        st.markdown('</div>', unsafe_allow_html=True)

        # 4. PANTALLAS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("4. Pantallas IT")
        it1, it2, it3 = st.columns(3)
        t_izq = it1.radio("Tótem Izquierdo", ["OK", "Falla"])
        t_der = it2.radio("Tótem Derecho", ["OK", "Falla"])
        tv_izq = it3.radio("TV principal", ["OK", "Falla"])
        obs_pan = st.text_area("Observaciones de Pantallas", placeholder="Escriba aquí detalles de pantallas...", key="area_pan")
        st.markdown('</div>', unsafe_allow_html=True)

        # 5. OTROS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("5. Otros Sistemas")
        o1, o2, o3 = st.columns(3)
        internet = o1.radio("Internet", ["OK", "Falla"])
        wifi = o2.radio("Wifi Gratuito", ["OK", "Falla"])
        boton = o3.radio("Botón de Pánico", ["OK", "Falla"])
        obs_otros = st.text_area("Otras observaciones técnicas", placeholder="Escriba aquí otros detalles...", key="area_otros")
        st.markdown('</div>', unsafe_allow_html=True)

        # 6. FINAL
        st.subheader("Evidencia Fotográfica")
        obs_gen = st.text_area("Comentarios Finales del Supervisor *", key="area_gen")
        uploaded_images = st.file_uploader("Subir Fotos", accept_multiple_files=True)

        submit = st.form_submit_button("ENVIAR REPORTE AL EXCEL")

    if submit:
        if not tecnico or not obs_gen or not uploaded_images:
            st.warning("⚠️ Nombre, fotos y comentarios generales son obligatorios.")
        else:
            with st.spinner("Enviando reporte completo..."):
                links = []
                for img in uploaded_images[:10]:
                    try:
                        res = requests.post("https://api.imgbb.com/1/upload", 
                                           {"key": IMGBB_API_KEY, "image": base64.b64encode(img.read()).decode('utf-8')})
                        if res.status_code == 200: links.append(res.json()['data']['url'])
                    except: pass
                
                payload = {
                    "action": "insertar", "tecnico": tecnico, "ubicacion": ubicacion,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "muebles": muebles, "cableado": cableado, "energia": energia, "ilumina": ilumina, "obs_int": obs_int,
                    "leds_s": "OK", "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": "OK", "obs_pan": obs_pan,
                    "internet": internet, "wifi": wifi, "lockers": "OK", "camaras": "OK", "m_izq": "OK", "m_der": "OK",
                    "branding": "OK", "l_int": "OK", "l_ext": "OK", "l_vis": "OK", "obs_mod": obs_otros,
                    "obs_gen": obs_gen, "fotos": ";".join(links), "boton": boton
                }
                
                try:
                    r = requests.post(URL_BRIDGE, json=payload)
                    if r.status_code == 200:
                        st.success("¡Reporte guardado exitosamente!")
                        st.balloons()
                except: st.error("Error al conectar con la base de datos.")

with tab2:
    st.title("Gestión de Reportes")
    if st.button("🔄 Sincronizar con Excel"):
        try:
            r = requests.get(URL_BRIDGE)
            data = r.json()
            if data and len(data) > 1:
                df = pd.DataFrame(data[1:], columns=data[0])
                
                # Mapeo seguro de columnas para evitar el IndexError
                def get_col(name_list):
                    for name in name_list:
                        for col in df.columns:
                            if name.lower() in col.lower():
                                return col
                    return None

                c_ubi = get_col(['Ubicación', 'Ubicacion'])
                c_fec = get_col(['Fecha'])
                c_tec = get_col(['Técnico', 'Tecnico'])
                c_obs = get_col(['Generales', 'Comentarios'])
                c_fot = get_col(['Fotos'])

                if c_ubi and c_fec:
                    for idx, row in df.iterrows():
                        with st.expander(f"📍 {row[c_ubi]} - {row[c_fec]}"):
                            if c_tec: st.write(f"**Técnico:** {row[c_tec]}")
                            if c_obs: st.write(f"**Notas:** {row[c_obs]}")
                            if c_fot and row[c_fot]:
                                imgs = str(row[c_fot]).split(";")
                                st.image(imgs, width=200)
                else:
                    st.error("No se encontraron las columnas básicas en el Excel.")
            else:
                st.info("No hay datos suficientes en la hoja de cálculo.")
        except Exception as e:
            st.error(f"Error al cargar el Dashboard: {e}")
