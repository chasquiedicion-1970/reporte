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

st.set_page_config(page_title="Kioscos IA - Operaciones", layout="wide", page_icon="🚀")

# --- NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'HOME'

def navega(p):
    st.session_state.page = p

# --- CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BLACK}; color: white; }}
    .main-header {{
        background: linear-gradient(90deg, {COLOR_BLUE_SEA} 0%, #1900AF 100%);
        padding: 2.5rem; border-radius: 0 0 35px 35px; border-bottom: 4px solid {COLOR_CIAN};
        text-align: center; margin-bottom: 2rem;
    }}
    .option-card {{
        background: {COLOR_BLUE_SEA}; padding: 40px; border-radius: 20px;
        border: 2px solid #1900AF; text-align: center; height: 300px;
        display: flex; flex-direction: column; justify-content: center;
    }}
    .section-header {{ color: {COLOR_CIAN}; font-weight: bold; text-transform: uppercase; border-bottom: 2px solid {COLOR_CIAN}; padding-bottom: 5px; margin: 20px 0; }}
    .report-card {{ background: {COLOR_BLUE_SEA}; padding: 30px; border-radius: 20px; border: 1px solid #1900AF; }}
    .text-box {{ background: #000; padding: 15px; border-radius: 10px; border: 1px solid #1900AF; white-space: pre-wrap; color: #cbd5e1; }}
    div.stButton > button {{ background: {COLOR_CIAN} !important; color: {COLOR_BLACK} !important; font-weight: bold !important; border-radius: 50px !important; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="main-header"><h1>KIOSCOS IΛ</h1><p style="color:{COLOR_CIAN}; font-weight:bold;">EL FUTURO EN CADA ESQUINA</p></div>', unsafe_allow_html=True)

# --- PANTALLA 1: HOME ---
if st.session_state.page == 'HOME':
    col_l, col_m, col_r = st.columns([1, 4, 1])
    with col_m:
        st.write("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="option-card"><h2>📋 SUPERVISOR</h2><p>Ingreso de inspección técnica</p></div>', unsafe_allow_html=True)
            if st.button("ACCEDER"): navega('SUPERVISOR'); st.rerun()
        with c2:
            st.markdown(f'<div class="option-card"><h2>📊 REPORTES</h2><p>Control e historial de puntos</p></div>', unsafe_allow_html=True)
            if st.button("CONSULTAR"): navega('REPORTES'); st.rerun()

# --- PANTALLA 2: SUPERVISOR ---
elif st.session_state.page == 'SUPERVISOR':
    if st.button("← VOLVER AL MENÚ"): navega('HOME'); st.rerun()
    
    with st.form("form_full"):
        st.subheader("📝 Registro de Inspección")
        c1, c2 = st.columns(2)
        tec = c1.text_input("TÉCNICO RESPONSABLE *")
        ubi = c2.selectbox("KIOSCO", KIOSCOS_OFICIALES)
        
        st.markdown('<div class="section-header">🖥️ Sistemas IT y Pantallas</div>', unsafe_allow_html=True)
        it1, it2, it3, it4, it5 = st.columns(5)
        t_izq = it1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it3.radio("TV Izq", ["OK", "Falla"])
        tv_der = it4.radio("TV Der", ["OK", "Falla"])
        p_360 = it5.radio("Pantallas 360", ["OK", "Falla"])
        obs_it = st.text_area("Notas IT / Pantallas")

        st.markdown('<div class="section-header">🏗️ Infraestructura y Energía</div>', unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        energia, muebles = e1.radio("Energía", ["OK", "Falla"]), e2.radio("Muebles", ["OK", "Falla"])
        cableado, ilumina = e3.radio("Cableado", ["OK", "Falla"]), e4.radio("Luz", ["OK", "Falla"])
        
        st.write("**Puertas:**")
        p1, p2, p3, p4 = st.columns(4)
        p_izq, c_der = p1.radio("Piloto Izq", ["OK", "Falla"]), p2.radio("Copiloto Der", ["OK", "Falla"])
        p_del, p_pos = p3.radio("Delantera", ["OK", "Falla"]), p4.radio("Posterior", ["OK", "Falla"])
        
        st.markdown('<div class="section-header">Finalización</div>', unsafe_allow_html=True)
        obs_gen = st.text_area("COMENTARIOS GENERALES *")
        fotos_u = st.file_uploader("Evidencia", accept_multiple_files=True)
        
        if st.form_submit_button("✅ ENVIAR REPORTE"):
            if not tec: st.error("Nombre obligatorio")
            else:
                with st.spinner("Enviando..."):
                    links = []
                    if fotos_u:
                        for img in fotos_u:
                            try:
                                b64 = base64.b64encode(img.read()).decode('utf-8')
                                res = requests.post("https://api.imgbb.com/1/upload", data={"key": IMGBB_API_KEY, "image": b64})
                                if res.status_code == 200: links.append(res.json()['data']['url'])
                            except: pass
                    
                    payload = {
                        "action": "insertar", "tecnico": tec, "ubicacion": ubi,
                        "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos,
                        "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina,
                        "p_360": p_360, "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der,
                        "obs_pan": obs_it, "obs_gen": obs_gen, "fotos": ";".join(links)
                    }
                    requests.post(URL_BRIDGE, json=payload, timeout=30)
                    st.success("¡Sincronizado!")

# --- PANTALLA 3: REPORTES ---
elif st.session_state.page == 'REPORTES':
    if st.button("← VOLVER AL MENÚ"): navega('HOME'); st.rerun()
    
    st.subheader("📊 Historial de Inspecciones")
    try:
        r = requests.get(URL_BRIDGE, timeout=35)
        df = pd.DataFrame(r.json()[1:], columns=r.json()[0])
        df = df[df['Ubicación'].isin(KIOSCOS_OFICIALES)]
        
        c1, c2 = st.columns(2)
        k_sel = c1.selectbox("Kiosco", df['Ubicación'].unique())
        f_sel = c2.selectbox("Fecha", df[df['Ubicación'] == k_sel]['Fecha'].unique())
        rep = df[(df['Ubicación'] == k_sel) & (df['Fecha'] == f_sel)].iloc[0]
        
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.write(f"### 📍 {k_sel} - {f_sel}")
        st.write(f"👷 **Técnico:** {rep.get('Técnico', 'N/A')}")
        
        st.markdown('<div class="section-header">🖥️ SISTEMAS IT & PANTALLAS</div>', unsafe_allow_html=True)
        it1, it2, it3, it4, it5 = st.columns(5)
        it1.metric("Totem I", rep.get('Totem Izquierdo', 'N/A'))
        it2.metric("Totem D", rep.get('Totem Derecho', 'N/A'))
        it3.metric("TV I", rep.get('TV Izquierdo', 'N/A'))
        it4.metric("TV D", rep.get('TV Derecha', 'N/A'))
        it5.metric("P-360", rep.get('Pantallas 360', 'N/A'))
        st.markdown(f"**Notas IT:** <div class='text-box'>{rep.get('Obs Pantallas', 'N/A')}</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-header">🏗️ INFRAESTRUCTURA & ENERGÍA</div>', unsafe_allow_html=True)
        ei1, ei2, ei3, ei4 = st.columns(4)
        ei1.metric("Energía", rep.get('Energía', 'N/A'))
        ei2.metric("Muebles", rep.get('Muebles', 'N/A'))
        ei3.metric("Luz", rep.get('Iluminación', 'N/A'))
        ei4.metric("Cableado", rep.get('Cableado', 'N/A'))
        
        st.write(f"**Puertas:** P.Izq: {rep.get('Piloto Izquierdo')} | C.Der: {rep.get('Copiloto Derecho')} | Del: {rep.get('Delantera')} | Post: {rep.get('Posterior')}")
        
        st.markdown('<div class="section-header">📝 COMENTARIOS GENERALES</div>', unsafe_allow_html=True)
        st.markdown(f"<div class='text-box'>{rep.get('Obs Generales', 'N/A')}</div>", unsafe_allow_html=True)
        
        if rep.get('Fotos'):
            st.image(str(rep['Fotos']).split(";"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    except: st.error("Error al cargar datos. Verifica la conexión.")
