import streamlit as st
import requests
import base64
import pandas as pd

# --- IDENTIDAD KIOSCOS IA (BRANDBOOK) ---
COLOR_BLUE_SEA = "#000059"
COLOR_CIAN = "#66FBFC"
COLOR_BLACK = "#000000"

# SUSTITUYE POR TU URL DE GOOGLE APPS SCRIPT
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbzfsGoonaLWGVimiPS_v6ZPI_X3RiBQwNFZmJnpSoG0IWBwgLYsIOP_MFAyWHPQG2GZ/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

KIOSCOS_OFICIALES = [
    "LA PUNTA", "SALAVERRY REAL PLAZA", "PERSHING - DOMINGO ORUE", 
    "ARENALES - DOMINGO CUETO", "VIVANDA JAVIER PRADO", 
    "PASTIPAN JAVIER PRADO", "UNIVERSIDAD RICARDO PALMA", "SURCO WONG"
]

st.set_page_config(page_title="Kioscos IA - Gestión", layout="wide", page_icon="🚀")

# Estilo visual corporativo
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BLACK}; color: white; }}
    .main-header {{
        background: linear-gradient(135deg, {COLOR_BLUE_SEA} 0%, #1900AF 100%);
        padding: 2.5rem; border-radius: 0 0 30px 30px; border-bottom: 3px solid {COLOR_CIAN};
        text-align: center; margin-bottom: 2rem;
    }}
    .section-header {{
        color: {COLOR_CIAN}; font-weight: bold; text-transform: uppercase;
        border-bottom: 2px solid {COLOR_CIAN}; padding-bottom: 5px; margin: 25px 0 15px 0;
    }}
    .stForm, .report-box {{ 
        background-color: {COLOR_BLUE_SEA} !important; 
        padding: 25px !important; border-radius: 20px !important; 
        border: 1px solid #1900AF !important; 
    }}
    [data-testid="stMetricValue"] {{ color: {COLOR_CIAN} !important; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="main-header"><h1>KIOSCOS IΛ</h1><p style="color:{COLOR_CIAN};">EL FUTURO EN CADA ESQUINA</p></div>', unsafe_allow_html=True)

menu = st.sidebar.radio("MENÚ", ["📋 REGISTRO", "📊 CONSULTA"])

# --- MÓDULO DE REGISTRO ---
if menu == "📋 REGISTRO":
    with st.form("form_registro"):
        c1, c2 = st.columns(2)
        tec = c1.text_input("TÉCNICO RESPONSABLE (Obligatorio) *")
        ubi = c2.selectbox("UBICACIÓN", KIOSCOS_OFICIALES)
        
        st.markdown('<div class="section-header">Infraestructura y Accesos</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        p_izq = col1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = col2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = col3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = col4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Notas Estructura")

        st.markdown('<div class="section-header">Energía e Interiores</div>', unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        muebles = e1.radio("Muebles", ["OK", "Falla"])
        cableado = e2.radio("Cableado", ["OK", "Falla"])
        energia = e3.radio("Energía", ["OK", "Falla"])
        ilumina = e4.radio("Iluminación", ["OK", "Falla"])

        st.markdown('<div class="section-header">Sistemas IT</div>', unsafe_allow_html=True)
        it1, it2, it3, it4 = st.columns(4)
        t_izq = it1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it3.radio("TV Izq", ["OK", "Falla"])
        tv_der = it4.radio("TV Der", ["OK", "Falla"])

        st.markdown('<div class="section-header">Estética y Seguridad</div>', unsafe_allow_html=True)
        cl1, cl2, cl3, cl4 = st.columns(4)
        branding = cl1.radio("Branding", ["OK", "Dañado"])
        l_int = cl2.radio("Limp. Int", ["Limpio", "Sucio"])
        l_ext = cl3.radio("Limp. Ext", ["Limpio", "Sucio"])
        camaras = cl4.radio("Cámaras", ["OK", "Falla"])

        st.markdown('<div class="section-header">Finalización</div>', unsafe_allow_html=True)
        obs_gen = st.text_area("COMENTARIOS FINALES *")
        fotos_u = st.file_uploader("Fotos (Opcional)", accept_multiple_files=True)

        submit = st.form_submit_button("SINCRONIZAR REPORTE")

    if submit:
        if not tec:
            st.error("⚠️ El nombre es obligatorio.")
        else:
            with st.spinner("Enviando reporte..."):
                links = []
                if fotos_u:
                    for img in fotos_u[:10]:
                        try:
                            res = requests.post("https://api.imgbb.com/1/upload", data={"key": IMGBB_API_KEY, "image": base64.b64encode(img.read()).decode('utf-8')})
                            if res.status_code == 200: links.append(res.json()['data']['url'])
                        except: pass
                
                payload = {
                    "action": "insertar", "tecnico": tec, "ubicacion": ubi,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina,
                    "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der,
                    "branding": branding, "l_int": l_int, "l_ext": l_ext, "camaras": camaras,
                    "obs_gen": obs_gen, "fotos": ";".join(links)
                }
                
                try:
                    # Lógica de conexión simplificada (la que funcionaba)
                    r = requests.post(URL_BRIDGE, json=payload, timeout=30)
                    st.success("✅ ¡Reporte enviado con éxito!")
                    st.balloons()
                except:
                    st.error("❌ Error de conexión. Verifique los permisos del Script.")

# --- MÓDULO DE CONSULTA ---
else:
    st.subheader("📊 Historial de Inspecciones")
    try:
        r = requests.get(URL_BRIDGE, timeout=30)
        data = r.json()
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df[df['Ubicación'].isin(KIOSCOS_OFICIALES)]
            
            sel_k = st.selectbox("Seleccione Kiosco", df['Ubicación'].unique())
            sel_f = st.selectbox("Seleccione Fecha", df[df['Ubicación'] == sel_k]['Fecha'].unique())
            rep = df[(df['Ubicación'] == sel_k) & (df['Fecha'] == sel_f)].iloc[0]
            
            st.markdown(f'<div class="report-box">', unsafe_allow_html=True)
            st.write(f"### 📍 {sel_k} - {sel_f}")
            st.write(f"👷 **Técnico:** {rep.get('Técnico')}")
            
            c_it1, c_it2, c_it3, c_it4 = st.columns(4)
            c_it1.metric("Totem Izq", rep.get('Totem Izquierdo'))
            c_it2.metric("Totem Der", rep.get('Totem Derecho'))
            c_it3.metric("TV Izq", rep.get('TV Izquierdo'))
            c_it4.metric("TV Der", rep.get('TV Derecha'))
            
            st.markdown('<div class="section-header">Detalles Generales</div>', unsafe_allow_html=True)
            st.write(f"**Branding:** {rep.get('Branding')} | **Limpieza:** {rep.get('Limp Interna')} | **Cámaras:** {rep.get('Cámaras Seguridad')}")
            st.write(f"**Observaciones:** {rep.get('Obs Generales')}")
            
            if rep.get('Fotos'):
                st.image(str(rep['Fotos']).split(";"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.info("Sincronizando datos... Si el error persiste, revisa los permisos 'Anyone' en tu Script.")
