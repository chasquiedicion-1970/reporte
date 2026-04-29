import streamlit as st
import requests
import base64
import pandas as pd

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwZHc5UdHwbx52lgLWL5_LPDEuDjft7_yWbDuR1lDyOZk05h3G4bKfwHjJuHpziNjTS/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

KIOSCOS_OFICIALES = [
    "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
    "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", 
    "PASTIPAN JAVIER PRADO", "UNIVERSIDAD RICARDO PALMA", "SURCO WONG"
]

st.set_page_config(page_title="Kioscos IA - Dashboard", layout="wide", page_icon="🚀")

# --- DISEÑO UI AVANZADO (CSS) ---
st.markdown("""
    <style>
    /* Fondo y Base */
    .stApp { background-color: #020617; color: #f8fafc; }
    
    /* Encabezado Principal */
    .main-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid #00d4ff;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 212, 255, 0.2);
    }
    
    /* Secciones / Tarjetas */
    .stForm, .report-box {
        background-color: #0f172a !important;
        padding: 30px !important;
        border-radius: 15px !important;
        border: 1px solid #1e293b !important;
        margin-bottom: 25px !important;
    }
    
    /* Encabezados de Sección */
    .section-header {
        color: #00d4ff;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-left: 4px solid #00d4ff;
        padding-left: 15px;
        margin-bottom: 20px;
        margin-top: 10px;
    }
    
    /* Caja de texto de Observaciones */
    .text-wrap {
        white-space: pre-wrap;
        background: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
        color: #e2e8f0;
        line-height: 1.6;
    }
    
    /* Botón de Envío */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #00d4ff 0%, #0080ff 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.6);
        transform: scale(1.02);
    }
    
    /* Estilo de métricas */
    [data-testid="stMetricValue"] { color: #00d4ff !important; font-size: 1.8rem !important; }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🛸 KIOSCOS IA · CONTROL PANEL</h1><p style="color:#94a3b8;">Gestión Técnica de Infraestructura Digital</p></div>', unsafe_allow_html=True)
menu = st.sidebar.radio("MODO DE OPERACIÓN", ["📋 SUPERVISOR (Ingreso)", "📊 REPORTES (Historial)"])

# --- MÓDULO 1: SUPERVISOR ---
if menu == "📋 SUPERVISOR (Ingreso)":
    st.subheader("📝 Nuevo Registro de Inspección")
    
    with st.form("form_visual"):
        c1, c2 = st.columns(2)
        tec = c1.text_input("👤 Técnico Responsable (Obligatorio) *", placeholder="Nombre completo")
        ubi = c2.selectbox("📍 Kiosco Seleccionado", KIOSCOS_OFICIALES)
        
        st.markdown('<div class="section-header">🏗️ Estructura y Puertas</div>', unsafe_allow_html=True)
        cp1, cp2, cp3, cp4 = st.columns(4)
        p_izq = cp1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = cp2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = cp3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = cp4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Notas sobre accesos", height=100)

        st.markdown('<div class="section-header">🖥️ Sistemas Digitales & IT</div>', unsafe_allow_html=True)
        it1, it2, it3, it4 = st.columns(4)
        t_izq = it1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it3.radio("TV Izquierda", ["OK", "Falla"])
        tv_der = it4.radio("TV Derecha", ["OK", "Falla"])
        obs_pan = st.text_area("Notas técnicas IT", height=100)

        st.markdown('<div class="section-header">⚡ Energía e Interiores</div>', unsafe_allow_html=True)
        ci1, ci2, ci3, ci4 = st.columns(4)
        muebles = ci1.radio("Muebles", ["OK", "Falla"])
        cableado = ci2.radio("Cableado", ["OK", "Falla"])
        energia = ci3.radio("Energía", ["OK", "Falla"])
        ilumina = ci4.radio("Iluminación", ["OK", "Falla"])
        
        st.markdown('<div class="section-header">✨ Branding y Limpieza</div>', unsafe_allow_html=True)
        cl1, cl2, cl3 = st.columns(3)
        branding = cl1.radio("Branding", ["OK", "Dañado"])
        l_int = cl2.radio("Limpieza Int.", ["Limpio", "Sucio"])
        l_ext = cl3.radio("Limpieza Ext.", ["Limpio", "Sucio"])

        st.markdown('<div class="section-header">📸 Evidencia y Conclusión</div>', unsafe_allow_html=True)
        obs_gen = st.text_area("Comentarios Finales de Supervisión *", height=150)
        fotos_u = st.file_uploader("Adjuntar fotos (Opcional)", accept_multiple_files=True)

        submit = st.form_submit_button("🚀 SINCRONIZAR REPORTE")

    if submit:
        if not tec:
            st.error("⚠️ Debes ingresar el nombre del técnico para validar el reporte.")
        else:
            with st.spinner("🚀 Subiendo datos a la nube..."):
                links = []
                if fotos_u:
                    for img in fotos_u[:10]:
                        try:
                            b64 = base64.b64encode(img.read()).decode('utf-8')
                            r = requests.post("https://api.imgbb.com/1/upload", data={"key": IMGBB_API_KEY, "image": b64})
                            if r.status_code == 200: links.append(r.json()['data']['url'])
                        except: pass
                
                payload = {
                    "action": "insertar", "tecnico": tec, "ubicacion": ubi,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina, "obs_int": "N/A",
                    "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der, "obs_pan": obs_pan,
                    "branding": branding, "l_int": l_int, "l_ext": l_ext, "obs_gen": obs_gen, "fotos": ";".join(links)
                }
                requests.post(URL_BRIDGE, json=payload, timeout=35)
                st.success("✅ ¡Reporte almacenado correctamente!")
                st.balloons()

# --- MÓDULO 2: REPORTES ---
else:
    st.subheader("📊 Historial de Inspecciones")
    try:
        r = requests.get(URL_BRIDGE, timeout=40)
        data = r.json()
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df[df['Ubicación'].isin(KIOSCOS_OFICIALES)]
            
            sc1, sc2 = st.columns(2)
            k_sel = sc1.selectbox("Filtrar Kiosco", df['Ubicación'].unique())
            f_sel = sc2.selectbox("Seleccionar Fecha", df[df['Ubicación']==k_sel]['Fecha'].unique())
            
            rep = df[(df['Ubicación']==k_sel) & (df['Fecha']==f_sel)].iloc[0]
            
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.markdown(f"<h2>📍 {k_sel}</h2>", unsafe_allow_html=True)
            st.write(f"👷 **Técnico:** {rep.get('Técnico')} | 📅 **Fecha:** {f_sel}")
            
            # Layout de Reporte
            st.markdown('<div class="section-header">⚙️ Estado Estructural</div>', unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Piloto Izq", rep.get('Piloto Izquierdo'))
            m2.metric("Copiloto Der", rep.get('Copiloto Derecho'))
            m3.metric("Delantera", rep.get('Delantera'))
            m4.metric("Posterior", rep.get('Posterior'))
            
            st.markdown('<div class="section-header">🖥️ Equipamiento IT</div>', unsafe_allow_html=True)
            i1, i2, i3, i4 = st.columns(4)
            i1.metric("Totem Izq", rep.get('Totem Izquierdo'))
            i2.metric("Totem Der", rep.get('Totem Derecho'))
            i3.metric("TV Izq", rep.get('TV Izquierdo'))
            i4.metric("TV Der", rep.get('TV Derecha'))

            st.markdown('<div class="section-header">📝 Notas Generales</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='text-wrap'>{rep.get('Obs Generales')}</div>", unsafe_allow_html=True)
            
            if rep.get('Fotos'):
                st.markdown('<div class="section-header">📸 Galería de Evidencia</div>', unsafe_allow_html=True)
                st.image(str(rep['Fotos']).split(";"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("❌ No se pudo conectar con la base de datos.")
