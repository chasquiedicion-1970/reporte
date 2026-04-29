import streamlit as st
import requests
import base64
import pandas as pd

# --- IDENTIDAD CORPORATIVA (BRANDBOOK) ---
COLOR_BLUE_SEA = "#000059"
COLOR_CIAN = "#66FBFC"
COLOR_BLACK = "#000000"
COLOR_SUCCESS = "#22c55e" # Verde
COLOR_DANGER = "#ef4444"  # Rojo

URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwZHc5UdHwbx52lgLWL5_LPDEuDjft7_yWbDuR1lDyOZk05h3G4bKfwHjJuHpziNjTS/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

KIOSCOS_OFICIALES = [
    "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
    "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", 
    "PASTIPAN JAVIER PRADO", "UNIVERSIDAD RICARDO PALMA", "SURCO WONG"
]

st.set_page_config(page_title="Kioscos IA - Operaciones", layout="wide", page_icon="🚀")

if 'page' not in st.session_state:
    st.session_state.page = 'HOME'

def navega(p):
    st.session_state.page = p

# --- CSS PERSONALIZADO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BLACK}; color: white; }}
    .main-header {{
        background: linear-gradient(90deg, {COLOR_BLUE_SEA} 0%, #1900AF 100%);
        padding: 2rem; border-radius: 0 0 35px 35px; border-bottom: 4px solid {COLOR_CIAN};
        text-align: center; margin-bottom: 2rem;
    }}
    .option-card {{
        background: {COLOR_BLUE_SEA}; padding: 40px; border-radius: 20px;
        border: 2px solid #1900AF; text-align: center; height: 280px;
        display: flex; flex-direction: column; justify-content: center;
    }}
    .section-header {{ color: {COLOR_CIAN}; font-weight: bold; text-transform: uppercase; border-bottom: 2px solid {COLOR_CIAN}; padding-bottom: 5px; margin: 25px 0 15px 0; }}
    .report-card {{ background: {COLOR_BLUE_SEA}; padding: 30px; border-radius: 20px; border: 1px solid #1900AF; }}
    .text-box {{ background: #000; padding: 12px; border-radius: 8px; border: 1px solid #1900AF; white-space: pre-wrap; color: #cbd5e1; }}
    div.stButton > button {{ background: {COLOR_CIAN} !important; color: {COLOR_BLACK} !important; font-weight: bold !important; border-radius: 50px !important; }}
    
    /* Clases para semáforo */
    .status-ok {{ color: {COLOR_SUCCESS}; font-weight: bold; border-left: 4px solid {COLOR_SUCCESS}; padding-left: 10px; }}
    .status-fail {{ color: {COLOR_DANGER}; font-weight: bold; border-left: 4px solid {COLOR_DANGER}; padding-left: 10px; }}
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
            st.markdown(f'<div class="option-card"><h2>📋 SUPERVISOR</h2><p>Registro de inspección técnica</p></div>', unsafe_allow_html=True)
            if st.button("ACCEDER"): navega('SUPERVISOR'); st.rerun()
        with c2:
            st.markdown(f'<div class="option-card"><h2>📊 REPORTES</h2><p>Control e historial de puntos</p></div>', unsafe_allow_html=True)
            if st.button("CONSULTAR"): navega('REPORTES'); st.rerun()

# --- PANTALLA 2: SUPERVISOR ---
elif st.session_state.page == 'SUPERVISOR':
    if st.button("← VOLVER AL MENÚ"): navega('HOME'); st.rerun()
    
    with st.form("form_full_v3"):
        st.subheader("📝 Registro de Inspección Integral")
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

        st.markdown('<div class="section-header">🏗️ Estructura, Energía y Seguridad</div>', unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        energia = e1.radio("Energía", ["OK", "Falla"])
        cableado = e2.radio("Cableado", ["OK", "Falla"])
        ilumina = e3.radio("Iluminación", ["OK", "Falla"])
        camaras = e4.radio("Cámaras", ["OK", "Falla"])
        
        st.write("**Estado de Puertas:**")
        p1, p2, p3, p4 = st.columns(4)
        p_izq = p1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = p2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = p3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = p4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Notas Estructura y Puertas")

        st.markdown('<div class="section-header">✨ Branding y Limpieza</div>', unsafe_allow_html=True)
        l1, l2, l3, l4 = st.columns(4)
        muebles = l1.radio("Muebles", ["OK", "Falla"])
        branding = l2.radio("Branding", ["OK", "Dañado"])
        l_int = l3.radio("Limp. Int", ["Limpio", "Sucio"])
        l_ext = l4.radio("Limp. Ext", ["Limpio", "Sucio"])

        st.markdown('<div class="section-header">Finalización</div>', unsafe_allow_html=True)
        obs_gen = st.text_area("COMENTARIOS GENERALES DEL SUPERVISOR *")
        fotos_u = st.file_uploader("Subir Evidencia (Opcional)", accept_multiple_files=True)
        
        if st.form_submit_button("✅ ENVIAR REPORTE AL SISTEMA"):
            if not tec: st.error("⚠️ El nombre del técnico es obligatorio.")
            else:
                with st.spinner("Sincronizando..."):
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
                        "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                        "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina,
                        "p_360": p_360, "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der,
                        "branding": branding, "l_int": l_int, "l_ext": l_ext, "camaras": camaras,
                        "obs_pan": obs_it, "obs_gen": obs_gen, "fotos": ";".join(links)
                    }
                    requests.post(URL_BRIDGE, json=payload, timeout=30)
                    st.success("✅ ¡Datos guardados correctamente!")

# --- PANTALLA 3: REPORTES ---
elif st.session_state.page == 'REPORTES':
    if st.button("← VOLVER AL MENÚ"): navega('HOME'); st.rerun()
    
    st.subheader("📊 Historial y Control de Estados")
    try:
        r = requests.get(URL_BRIDGE, timeout=35)
        df = pd.DataFrame(r.json()[1:], columns=r.json()[0])
        df = df[df['Ubicación'].isin(KIOSCOS_OFICIALES)]
        
        c1, c2 = st.columns(2)
        k_sel = c1.selectbox("Kiosco", df['Ubicación'].unique())
        f_sel = c2.selectbox("Fecha", df[df['Ubicación'] == k_sel]['Fecha'].unique())
        rep = df[(df['Ubicación'] == k_sel) & (df['Fecha'] == f_sel)].iloc[0]
        
        # Función interna para el color
        def get_status_class(val):
            val_str = str(val).upper()
            if val_str in ["OK", "PERFECTO", "LIMPIO"]: return "status-ok"
            if val_str in ["FALLA", "DAÑADO", "SUCIO"]: return "status-fail"
            return ""

        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.write(f"### 📍 {k_sel} - {f_sel}")
        st.write(f"👷 **Técnico:** {rep.get('Técnico', 'N/A')}")
        
        # --- SECCIÓN IT ---
        st.markdown('<div class="section-header">🖥️ SISTEMAS IT & PANTALLAS</div>', unsafe_allow_html=True)
        it_cols = st.columns(5)
        it_items = [
            ("Totem Izq", rep.get('Totem Izquierdo')),
            ("Totem Der", rep.get('Totem Derecho')),
            ("TV Izq", rep.get('TV Izquierdo')),
            ("TV Der", rep.get('TV Derecha')),
            ("P-360", rep.get('Pantallas 360'))
        ]
        for col, (label, val) in zip(it_cols, it_items):
            col.markdown(f"{label}:<br><span class='{get_status_class(val)}'>{val}</span>", unsafe_allow_html=True)
        st.markdown(f"**Notas IT:** <div class='text-box'>{rep.get('Obs Pantallas', 'N/A')}</div>", unsafe_allow_html=True)

        # --- SECCIÓN INFRAESTRUCTURA ---
        st.markdown('<div class="section-header">🏗️ INFRAESTRUCTURA, ENERGÍA & SEGURIDAD</div>', unsafe_allow_html=True)
        e_cols = st.columns(4)
        e_items = [
            ("Energía", rep.get('Energía')),
            ("Cableado", rep.get('Cableado')),
            ("Luz", rep.get('Iluminación')),
            ("Cámaras", rep.get('Cámaras Seguridad'))
        ]
        for col, (label, val) in zip(e_cols, e_items):
            col.markdown(f"{label}:<br><span class='{get_status_class(val)}'>{val}</span>", unsafe_allow_html=True)
        
        st.write("**Puertas y Muebles:**")
        p_cols = st.columns(5)
        p_items = [
            ("Piloto I.", rep.get('Piloto Izquierdo')),
            ("Copiloto D.", rep.get('Copiloto Derecho')),
            ("Delantera", rep.get('Delantera')),
            ("Posterior", rep.get('Posterior')),
            ("Muebles", rep.get('Muebles'))
        ]
        for col, (label, val) in zip(p_cols, p_items):
            col.markdown(f"{label}:<br><span class='{get_status_class(val)}'>{val}</span>", unsafe_allow_html=True)
        st.markdown(f"**Notas Estructura:** <div class='text-box'>{rep.get('Obs Puertas', 'N/A')}</div>", unsafe_allow_html=True)

        # --- SECCIÓN ESTÉTICA ---
        st.markdown('<div class="section-header">✨ ESTÉTICA Y LIMPIEZA</div>', unsafe_allow_html=True)
        l_cols = st.columns(3)
        l_items = [
            ("Branding", rep.get('Branding')),
            ("Limp. Int", rep.get('Limp Interna')),
            ("Limp. Ext", rep.get('Limp Externa'))
        ]
        for col, (label, val) in zip(l_cols, l_items):
            col.markdown(f"{label}:<br><span class='{get_status_class(val)}'>{val}</span>", unsafe_allow_html=True)

        st.markdown('<div class="section-header">📝 COMENTARIOS GENERALES</div>', unsafe_allow_html=True)
        st.markdown(f"<div class='text-box'>{rep.get('Obs Generales', 'N/A')}</div>", unsafe_allow_html=True)
        
        if rep.get('Fotos'):
            st.image(str(rep['Fotos']).split(";"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
