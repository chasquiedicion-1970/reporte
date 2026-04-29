import streamlit as st
import requests
import base64
import pandas as pd

# --- IDENTIDAD KIOSCOS IA (BRANDBOOK) ---
COLOR_BLUE_SEA = "#000059"
COLOR_CIAN = "#66FBFC"
COLOR_BLACK = "#000000"

# URL de tu Google Apps Script (Verifica que sea la última generada)
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwZHc5UdHwbx52lgLWL5_LPDEuDjft7_yWbDuR1lDyOZk05h3G4bKfwHjJuHpziNjTS/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

KIOSCOS_OFICIALES = [
    "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
    "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", 
    "PASTIPAN JAVIER PRADO", "UNIVERSIDAD RICARDO PALMA", "SURCO WONG"
]

st.set_page_config(page_title="Kioscos IA - Gestión Central", layout="wide", page_icon="🚀")

# --- ESTILO CORPORATIVO ---
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
        border-bottom: 2px solid {COLOR_CIAN}; padding-bottom: 5px; margin: 20px 0 10px 0;
    }}
    .stForm, .report-box {{ 
        background-color: {COLOR_BLUE_SEA} !important; 
        padding: 25px !important; border-radius: 15px !important; 
        border: 1px solid #1900AF !important; 
    }}
    .text-wrap {{ white-space: pre-wrap; background: #000000; padding: 12px; border-radius: 8px; border: 1px solid #1900AF; color: #cbd5e1; }}
    [data-testid="stMetricValue"] {{ color: {COLOR_CIAN} !important; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="main-header"><h1>KIOSCOS IΛ</h1><p style="color:{COLOR_CIAN}; font-weight:bold;">EL FUTURO EN CADA ESQUINA</p></div>', unsafe_allow_html=True)

menu = st.sidebar.radio("MODALIDAD", ["📋 SUPERVISOR", "📊 REPORTES"])

# --- MÓDULO SUPERVISOR ---
if menu == "📋 SUPERVISOR":
    st.subheader("📝 Registro de Inspección")
    with st.form("form_registro", clear_on_submit=False):
        c1, c2 = st.columns(2)
        tec = c1.text_input("TÉCNICO RESPONSABLE (Obligatorio) *")
        ubi = c2.selectbox("KIOSCO", KIOSCOS_OFICIALES)
        
        st.markdown('<div class="section-header">Infraestructura</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        p_izq = col1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = col2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = col3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = col4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Notas Estructura")

        st.markdown('<div class="section-header">Sistemas IT & Pantallas</div>', unsafe_allow_html=True)
        it1, it2, it3, it4 = st.columns(4)
        t_izq = it1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it3.radio("TV Izquierda", ["OK", "Falla"])
        tv_der = it4.radio("TV Derecha", ["OK", "Falla"])
        obs_it = st.text_area("Notas Sistemas")

        st.markdown('<div class="section-header">Energía y Estética</div>', unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        energia = e1.radio("Energía", ["OK", "Falla"])
        ilumina = e2.radio("Iluminación", ["OK", "Falla"])
        branding = e3.radio("Branding", ["OK", "Dañado"])
        limpieza = e4.radio("Limp. Gral", ["OK", "Sucio"])

        st.markdown('<div class="section-header">Finalización</div>', unsafe_allow_html=True)
        obs_gen = st.text_area("COMENTARIOS GENERALES *")
        fotos_u = st.file_uploader("Evidencia (Opcional)", accept_multiple_files=True)

        submit = st.form_submit_button("✅ GUARDAR REPORTE")

    if submit:
        if not tec:
            st.error("⚠️ El nombre del técnico es obligatorio.")
        else:
            with st.spinner("Sincronizando..."):
                links = []
                if fotos_u:
                    for img in fotos_u:
                        try:
                            res = requests.post("https://api.imgbb.com/1/upload", data={"key": IMGBB_API_KEY, "image": base64.b64encode(img.read()).decode('utf-8')})
                            if res.status_code == 200: links.append(res.json()['data']['url'])
                        except: pass
                
                payload = {
                    "action": "insertar", "tecnico": tec, "ubicacion": ubi,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der, "obs_pan": obs_it,
                    "energia": energia, "iluminacion": ilumina, "branding": branding, "l_int": limpieza,
                    "obs_gen": obs_gen, "fotos": ";".join(links)
                }
                try:
                    r = requests.post(URL_BRIDGE, json=payload, timeout=30)
                    st.success("✅ ¡Reporte enviado correctamente!")
                    st.balloons()
                except: st.error("❌ Error al enviar datos.")

# --- MÓDULO REPORTES ---
else:
    st.subheader("📊 Historial de Reportes")
    try:
        # Petición directa sin validaciones HTML que causan el error
        response = requests.get(URL_BRIDGE, timeout=30)
        data_json = response.json()
        
        if len(data_json) > 1:
            df = pd.DataFrame(data_json[1:], columns=data_json[0])
            # Filtrar solo por nombres oficiales
            df = df[df['Ubicación'].isin(KIOSCOS_OFICIALES)]
            
            c1, c2 = st.columns(2)
            k_sel = c1.selectbox("Kiosco", df['Ubicación'].unique())
            f_sel = c2.selectbox("Fecha", df[df['Ubicación'] == k_sel]['Fecha'].unique())
            
            rep = df[(df['Ubicación'] == k_sel) & (df['Fecha'] == f_sel)].iloc[0]
            
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.write(f"### 📍 {k_sel}")
            st.write(f"👷 **Responsable:** {rep.get('Técnico')} | 📅 **Fecha:** {f_sel}")
            
            st.markdown('<div class="section-header">Sistemas Digitales</div>', unsafe_allow_html=True)
            i1, i2, i3, i4 = st.columns(4)
            i1.metric("Totem Izq", rep.get('Totem Izquierdo', 'N/A'))
            i2.metric("Totem Der", rep.get('Totem Derecho', 'N/A'))
            i3.metric("TV Izq", rep.get('TV Izquierdo', 'N/A'))
            i4.metric("TV Der", rep.get('TV Derecha', 'N/A'))

            st.markdown('<div class="section-header">Infraestructura</div>', unsafe_allow_html=True)
            st.write(f"**Estructura:** P.Izq: {rep.get('Piloto Izquierdo')} | C.Der: {rep.get('Copiloto Derecho')} | Del: {rep.get('Delantera')} | Post: {rep.get('Posterior')}")
            st.markdown(f"**Notas:** <div class='text-wrap'>{rep.get('Obs Puertas', 'Sin notas')}</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="section-header">Conclusiones del Supervisor</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='text-wrap'>{rep.get('Obs Generales', 'N/A')}</div>", unsafe_allow_html=True)
            
            if rep.get('Fotos'):
                st.image(str(rep['Fotos']).split(";"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Aún no hay reportes para los kioscos oficiales.")
    except Exception as e:
        st.error("Sincronizando con la base de datos...")
        st.info("Si el error persiste, asegúrate de que el Script de Google esté publicado como 'Anyone'.")
