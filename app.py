import streamlit as st
import requests
import base64
import pandas as pd

# --- IDENTIDAD KIOSCOS IA (BRANDBOOK) ---
COLOR_BLUE_SEA = "#000059"
COLOR_CIAN = "#66FBFC"
COLOR_BLACK = "#000000"

URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwZHc5UdHwbx52lgLWL5_LPDEuDjft7_yWbDuR1lDyOZk05h3G4bKfwHjJuHpziNjTS/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

KIOSCOS_OFICIALES = [
    "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
    "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", 
    "PASTIPAN JAVIER PRADO", "UNIVERSIDAD RICARDO PALMA", "SURCO WONG"
]

st.set_page_config(page_title="Kioscos IA - Gestión Total", layout="wide", page_icon="🚀")

# --- CSS CORPORATIVO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BLACK}; color: white; }}
    .main-header {{
        background: linear-gradient(135deg, {COLOR_BLUE_SEA} 0%, #1900AF 100%);
        padding: 2rem; border-radius: 0 0 25px 25px; border-bottom: 3px solid {COLOR_CIAN};
        text-align: center; margin-bottom: 2rem;
    }}
    .section-header {{
        color: {COLOR_CIAN}; font-weight: bold; text-transform: uppercase;
        border-bottom: 2px solid {COLOR_CIAN}; padding-bottom: 5px; margin: 25px 0 10px 0;
    }}
    .report-card {{ 
        background-color: {COLOR_BLUE_SEA} !important; 
        padding: 20px; border-radius: 15px; border: 1px solid #1900AF; margin-bottom: 15px;
    }}
    .text-wrap {{ white-space: pre-wrap; background: #000000; padding: 12px; border-radius: 8px; border: 1px solid #1900AF; color: #cbd5e1; }}
    [data-testid="stMetricValue"] {{ color: {COLOR_CIAN} !important; font-size: 1.5rem !important; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="main-header"><h1>KIOSCOS IΛ</h1><p style="color:{COLOR_CIAN}; font-weight:bold;">EL FUTURO EN CADA ESQUINA</p></div>', unsafe_allow_html=True)

menu = st.sidebar.radio("MODALIDAD", ["📋 SUPERVISOR (Ingreso)", "📊 REPORTES (Consulta)"])

# --- MÓDULO 1: SUPERVISOR ---
if menu == "📋 SUPERVISOR (Ingreso)":
    st.subheader("📝 Registro Técnico Completo")
    with st.form("form_total", clear_on_submit=False):
        c1, c2 = st.columns(2)
        tec = c1.text_input("TÉCNICO RESPONSABLE (OBLIGATORIO) *")
        ubi = c2.selectbox("KIOSCO", KIOSCOS_OFICIALES)
        
        st.markdown('<div class="section-header">🏗️ Estructura y Accesos</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        p_izq = col1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = col2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = col3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = col4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Notas Estructura")

        st.markdown('<div class="section-header">🖥️ Sistemas IT y Pantallas</div>', unsafe_allow_html=True)
        it1, it2, it3, it4 = st.columns(4)
        t_izq = it1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it3.radio("TV Izquierda", ["OK", "Falla"])
        tv_der = it4.radio("TV Derecha", ["OK", "Falla"])
        leds_sel = st.radio("LEDS SUPERIORES", ["OK", "Falla"], horizontal=True)
        obs_it = st.text_area("Notas IT / Pantallas")

        st.markdown('<div class="section-header">🏠 Energía e Interiores</div>', unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        muebles = e1.radio("Muebles", ["OK", "Falla"])
        cableado = e2.radio("Cableado", ["OK", "Falla"])
        energia = e3.radio("Energía", ["OK", "Falla"])
        ilumina = e4.radio("Iluminación", ["OK", "Falla"])
        obs_int = st.text_area("Notas Interiores")

        st.markdown('<div class="section-header">✨ Estética y Seguridad</div>', unsafe_allow_html=True)
        cl1, cl2, cl3, cl4 = st.columns(4)
        branding = cl1.radio("Branding", ["OK", "Dañado"])
        l_int = cl2.radio("Limp. Int", ["Limpio", "Sucio"])
        l_ext = cl3.radio("Limp. Ext", ["Limpio", "Sucio"])
        camaras = cl4.radio("Cámaras", ["OK", "Falla"])

        st.markdown('<div class="section-header">Finalización</div>', unsafe_allow_html=True)
        obs_gen = st.text_area("COMENTARIOS GENERALES")
        fotos_u = st.file_uploader("Evidencia (Opcional)", accept_multiple_files=True)

        submit = st.form_submit_button("✅ GUARDAR REPORTE COMPLETO")

    if submit:
        if not tec:
            st.error("⚠️ El nombre del técnico es obligatorio.")
        else:
            with st.spinner("Sincronizando con Excel..."):
                links = []
                if fotos_u:
                    for img in fotos_u:
                        try:
                            b64 = base64.b64encode(img.read()).decode('utf-8')
                            res_img = requests.post("https://api.imgbb.com/1/upload", data={"key": IMGBB_API_KEY, "image": b64})
                            if res_img.status_code == 200:
                                links.append(res_img.json()['data']['url'])
                        except:
                            pass
                
                # Diccionario Payload Reconstruido para evitar SyntaxError
                payload = {
                    "action": "insertar",
                    "tecnico": tec,
                    "ubicacion": ubi,
                    "p_izq": p_izq,
                    "c_der": c_der,
                    "p_del": p_del,
                    "p_pos": p_pos,
                    "obs_p": obs_p,
                    "muebles": muebles,
                    "cableado": cableado,
                    "energia": energia,
                    "iluminacion": ilumina,
                    "obs_int": obs_int,
                    "leds_s": leds_sel,
                    "t_izq": t_izq,
                    "t_der": t_der,
                    "tv_izq": tv_izq,
                    "tv_der": tv_der,
                    "obs_pan": obs_it,
                    "branding": branding,
                    "l_int": l_int,
                    "l_ext": l_ext,
                    "obs_mod": "OK",
                    "obs_gen": obs_gen,
                    "fotos": ";".join(links)
                }
                
                try:
                    requests.post(URL_BRIDGE, json=payload, timeout=30)
                    st.success("✅ Reporte enviado con éxito.")
                    st.balloons()
                except:
                    st.error("❌ Error de comunicación.")

# --- MÓDULO 2: REPORTES ---
else:
    st.subheader("📊 Consulta de Historial")
    try:
        response = requests.get(URL_BRIDGE, timeout=30)
        data_json = response.json()
        if len(data_json) > 1:
            df = pd.DataFrame(data_json[1:], columns=data_json[0])
            df = df[df['Ubicación'].isin(KIOSCOS_OFICIALES)]
            
            c1, c2 = st.columns(2)
            k_sel = c1.selectbox("Filtrar Kiosco", df['Ubicación'].unique())
            df_k = df[df['Ubicación'] == k_sel]
            f_sel = c2.selectbox("Seleccionar Fecha", df_k['Fecha'].unique())
            
            rep = df_k[df_k['Fecha'] == f_sel].iloc[0]
            
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.write(f"### 📍 {k_sel} - {f_sel}")
            st.write(f"👷 **Responsable:** {rep.get('Técnico')}")
            
            # FILA 1: IT & LEDS
            st.markdown('<div class="section-header">🖥️ SISTEMAS IT & PANTALLAS</div>', unsafe_allow_html=True)
            it1, it2, it3, it4, it5 = st.columns(5)
            it1.metric("Totem Izq", rep.get('Totem Izquierdo', 'N/A'))
            it2.metric("Totem Der", rep.get('Totem Derecho', 'N/A'))
            it3.metric("TV Izq", rep.get('TV Izquierdo', 'N/A'))
            it4.metric("TV Der", rep.get('TV Derecha', 'N/A'))
            it5.metric("LEDS", rep.get('Leds Superiores', 'N/A'))
            st.markdown(f"**Notas IT:** <div class='text-wrap'>{rep.get('Obs Pantallas', 'N/A')}</div>", unsafe_allow_html=True)

            # FILA 2: ESTRUCTURA & ENERGÍA
            st.markdown('<div class="section-header">🏠 ESTRUCTURA E INTERIORES</div>', unsafe_allow_html=True)
            ei1, ei2, ei3, ei4 = st.columns(4)
            ei1.metric("Muebles", rep.get('Muebles', 'N/A'))
            ei2.metric("Energía", rep.get('Energía', 'N/A'))
            ei3.metric("Iluminación", rep.get('Iluminación', 'N/A'))
            ei4.metric("Cámaras", rep.get('Cámaras Seguridad', 'N/A'))
            st.write(f"**Accesos:** P.Izq: {rep.get('Piloto Izquierdo')} | C.Der: {rep.get('Copiloto Derecho')} | Del: {rep.get('Delantera')} | Post: {rep.get('Posterior')}")
            st.markdown(f"**Notas Estructura:** <div class='text-wrap'>{rep.get('Obs Puertas', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-header">📝 COMENTARIOS GENERALES</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='text-wrap'>{rep.get('Obs Generales', 'N/A')}</div>", unsafe_allow_html=True)
            
            if rep.get('Fotos'):
                st.markdown('<div class="section-header">📸 EVIDENCIA</div>', unsafe_allow_html=True)
                st.image(str(rep['Fotos']).split(";"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("Error al cargar datos. Verifica la conexión.")
