import streamlit as st
import requests
import base64
import pandas as pd

# --- CONFIGURACIÓN ---
URL_BRIDGE = "https://script.google.com/macros/s/AKfycbwZHc5UdHwbx52lgLWL5_LPDEuDjft7_yWbDuR1lDyOZk05h3G4bKfwHjJuHpziNjTS/exec"
IMGBB_API_KEY = "375f94b0781e8b8b0d2ffa0132d8edca"

# --- LISTA MAESTRA OFICIAL (Modifica esto para agregar kioscos nuevos) ---
KIOSCOS_OFICIALES = [
    "LA PUNTA", 
    "SALAVERRY REAL PLAZA", 
    "PERSHING - DOMINGO ORUE", 
    "ARENALES - DOMINGO CUETO", 
    "VIVANDA JAVIER PRADO", 
    "PASTIPAN JAVIER PRADO", 
    "UNIVERSIDAD RICARDO PALMA", 
    "SURCO WONG", 
]

st.set_page_config(page_title="Kioscos IA - Gestión Central", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .main-nav { background-color: #0f172a; padding: 20px; border-radius: 15px; border: 1px solid #00d4ff; margin-bottom: 30px; text-align: center; }
    .report-box { background-color: #0f172a; padding: 25px; border-radius: 15px; border-left: 5px solid #00d4ff; border: 1px solid #1e293b; margin-bottom: 20px; }
    .section-header { color: #00d4ff; font-weight: bold; border-bottom: 1px solid #1e293b; margin-top: 20px; margin-bottom: 10px; font-size: 1.1rem; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-nav"><h1>🚀 SISTEMA INTEGRAL KIOSCOS IA</h1></div>', unsafe_allow_html=True)
menu = st.sidebar.radio("MÓDULO SELECCIONADO", ["SUPERVISOR (Ingreso)", "REPORTES (Consulta)"])

# --- MÓDULO 1: SUPERVISOR ---
if menu == "SUPERVISOR (Ingreso)":
    st.header("📝 Registro de Inspección Oficial")
    with st.form("form_sup_final", clear_on_submit=True):
        c1, c2 = st.columns(2)
        tec = c1.text_input("Técnico Responsable *")
        ubi = c2.selectbox("Seleccione Kiosco Oficial *", KIOSCOS_OFICIALES)
        
        # Bloque 1: Estructura
        st.markdown('<div class="section-header">🏗️ Estructura y Puertas</div>', unsafe_allow_html=True)
        col_p = st.columns(4)
        p_izq = col_p[0].radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = col_p[1].radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = col_p[2].radio("Delantera", ["Perfecto", "Falla"])
        p_pos = col_p[3].radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Observaciones Puertas")

        # Bloque 2: IT y Pantallas
        st.markdown('<div class="section-header">🖥️ Sistemas IT y Pantallas</div>', unsafe_allow_html=True)
        col_it = st.columns(3)
        t_izq = col_it[0].radio("Totem Izq", ["OK", "Falla"])
        t_der = col_it[1].radio("Totem Der", ["OK", "Falla"])
        tv_izq = col_it[2].radio("TV Principal", ["OK", "Falla"])
        obs_pan = st.text_area("Observaciones IT")

        # Bloque 3: Otros Sistemas (Lockers, Cámaras, etc)
        st.markdown('<div class="section-header">⚙️ Otros Componentes</div>', unsafe_allow_html=True)
        o1, o2, o3 = st.columns(3)
        internet = o1.radio("Internet/Wifi", ["OK", "Falla"])
        camaras = o2.radio("Cámaras", ["OK", "Falla"])
        lockers = o3.radio("Lockers", ["OK", "Falla"])
        
        st.subheader("📸 Evidencia Final")
        obs_gen = st.text_area("Comentarios Generales del Supervisor *")
        fotos_u = st.file_uploader("Fotos de la inspección", accept_multiple_files=True)

        if st.form_submit_button("✅ ENVIAR REPORTE AL EXCEL"):
            if not tec or not fotos_u:
                st.error("⚠️ Datos obligatorios faltantes.")
            else:
                with st.spinner("Sincronizando con base de datos..."):
                    links = []
                    for img in fotos_u[:10]:
                        try:
                            res = requests.post("https://api.imgbb.com/1/upload", data={"key": IMGBB_API_KEY, "image": base64.b64encode(img.read()).decode('utf-8')})
                            if res.status_code == 200: links.append(res.json()['data']['url'])
                        except: pass
                    
                    payload = {
                        "action": "insertar", "tecnico": tec, "ubicacion": ubi,
                        "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                        "muebles": "N/A", "cableado": "N/A", "energia": "N/A", "iluminacion": "N/A", "obs_int": "N/A",
                        "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "obs_pan": obs_pan,
                        "internet": internet, "wifi": internet, "lockers": lockers, "camaras": camaras,
                        "obs_gen": obs_gen, "fotos": ";".join(links), "boton": "OK"
                    }
                    requests.post(URL_BRIDGE, json=payload, timeout=30)
                    st.success("¡Reporte Guardado!")

# --- MÓDULO 2: REPORTES ---
else:
    st.header("📊 Consulta Histórica de Reportes")
    try:
        r = requests.get(URL_BRIDGE, timeout=35)
        data = r.json()
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            
            # FILTRADO INTELIGENTE: Solo mostramos kioscos que estén en nuestra lista oficial
            df_limpio = df[df['Ubicación'].isin(KIOSCOS_OFICIALES)]
            
            c1, c2 = st.columns(2)
            sel_k = c1.selectbox("Filtrar por Kiosco Oficial:", df_limpio['Ubicación'].unique())
            df_k = df_limpio[df_limpio['Ubicación'] == sel_k]
            sel_f = c2.selectbox("Seleccionar Fecha:", df_k['Fecha'].unique())
            
            reporte = df_k[df_k['Fecha'] == sel_f].iloc[0]
            
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.subheader(f"📍 DETALLE COMPLETO: {sel_k}")
            st.write(f"**Técnico:** {reporte.get('Técnico', 'N/A')} | **Fecha:** {sel_f}")
            
            # FILA 1: ESTRUCTURA
            st.markdown('<div class="section-header">⚙️ ESTRUCTURA Y ACCESOS</div>', unsafe_allow_html=True)
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Piloto Izq", reporte.get('Piloto Izquierdo', 'N/A'))
            r2.metric("Copiloto Der", reporte.get('Copiloto Derecho', 'N/A'))
            r3.metric("Delantera", reporte.get('Delantera', 'N/A'))
            r4.metric("Posterior", reporte.get('Posterior', 'N/A'))
            st.write(f"**Notas Puertas:** {reporte.get('Obs Puertas', 'N/A')}")

            # FILA 2: TECNOLOGÍA
            st.markdown('<div class="section-header">🖥️ TECNOLOGÍA E IT</div>', unsafe_allow_html=True)
            it1, it2, it3 = st.columns(3)
            it1.metric("Totem Izq", reporte.get('Totem Izquierdo', 'N/A'))
            it2.metric("Totem Der", reporte.get('Totem Derecho', 'N/A'))
            it3.metric("TV Principal", reporte.get('TV Izquierdo', 'N/A'))
            st.write(f"**Notas IT:** {reporte.get('Obs Pantallas', 'N/A')}")

            # FILA 3: OTROS
            st.markdown('<div class="section-header">🔧 OTROS COMPONENTES</div>', unsafe_allow_html=True)
            o1, o2, o3 = st.columns(3)
            o1.metric("Internet", reporte.get('Internet', 'N/A'))
            o2.metric("Cámaras", reporte.get('Cámaras Seguridad', 'N/A'))
            o3.metric("Lockers", reporte.get('Lockers', 'N/A'))

            st.markdown('<div class="section-header">📝 COMENTARIOS FINALES</div>', unsafe_allow_html=True)
            st.info(reporte.get('Obs Generales', 'Sin observaciones.'))
            
            if reporte.get('Fotos'):
                st.markdown('<div class="section-header">📸 EVIDENCIA VISUAL</div>', unsafe_allow_html=True)
                st.image(str(reporte['Fotos']).split(";"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error al conectar con el Excel: {e}")
