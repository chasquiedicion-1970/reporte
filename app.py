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

st.set_page_config(page_title="Kioscos IA - Gestión Central", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .main-nav { background-color: #0f172a; padding: 20px; border-radius: 15px; border: 1px solid #00d4ff; margin-bottom: 30px; text-align: center; }
    .report-box { background-color: #0f172a; padding: 25px; border-radius: 15px; border-left: 5px solid #00d4ff; border: 1px solid #1e293b; margin-bottom: 20px; }
    .section-header { color: #00d4ff; font-weight: bold; border-bottom: 1px solid #1e293b; margin-top: 20px; margin-bottom: 10px; font-size: 1.1rem; text-transform: uppercase; }
    .text-wrap { white-space: pre-wrap; font-family: sans-serif; background: #1e293b; padding: 12px; border-radius: 8px; border: 1px solid #334155; color: #cbd5e1; }
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
        
        st.markdown('<div class="section-header">🏗️ Estructura y Puertas</div>', unsafe_allow_html=True)
        cp1, cp2, cp3, cp4 = st.columns(4)
        p_izq = cp1.radio("Piloto Izq", ["Perfecto", "Falla"])
        c_der = cp2.radio("Copiloto Der", ["Perfecto", "Falla"])
        p_del = cp3.radio("Delantera", ["Perfecto", "Falla"])
        p_pos = cp4.radio("Posterior", ["Perfecto", "Falla"])
        obs_p = st.text_area("Observaciones Puertas")

        st.markdown('<div class="section-header">🏠 Interiores y Energía</div>', unsafe_allow_html=True)
        ci1, ci2, ci3, ci4 = st.columns(4)
        muebles = ci1.radio("Muebles", ["OK", "Falla"])
        cableado = ci2.radio("Cableado", ["OK", "Falla"])
        energia = ci3.radio("Energía", ["OK", "Falla"])
        ilumina = ci4.radio("Iluminación", ["OK", "Falla"])
        obs_int = st.text_area("Observaciones Interiores")

        st.markdown('<div class="section-header">🖥️ Sistemas IT y Pantallas</div>', unsafe_allow_html=True)
        it_c1, it_c2, it_c3, it_c4 = st.columns(4)
        t_izq = it_c1.radio("Totem Izq", ["OK", "Falla"])
        t_der = it_c2.radio("Totem Der", ["OK", "Falla"])
        tv_izq = it_c3.radio("TV Izquierda", ["OK", "Falla"])
        tv_der = it_c4.radio("TV Derecha", ["OK", "Falla"])
        leds_s = st.radio("LEDs Superiores", ["OK", "Falla"], horizontal=True)
        obs_pan = st.text_area("Observaciones IT")

        st.markdown('<div class="section-header">🌐 Conectividad y Seguridad</div>', unsafe_allow_html=True)
        co1, co2, co3, co4 = st.columns(4)
        internet = co1.radio("Internet", ["OK", "Falla"])
        wifi = co2.radio("Wifi Gratuito", ["OK", "Falla"])
        camaras = co3.radio("Cámaras", ["OK", "Falla"])
        boton = co4.radio("Botón Pánico", ["OK", "Falla"])

        st.markdown('<div class="section-header">✨ Branding y Limpieza</div>', unsafe_allow_html=True)
        cl1, cl2, cl3 = st.columns(3)
        branding = cl1.radio("Branding", ["OK", "Dañado"])
        l_int = cl2.radio("Limpieza Int.", ["OK", "Sucio"])
        l_ext = cl3.radio("Limpieza Ext.", ["OK", "Sucio"])
        obs_mod = st.text_area("Observaciones Módulo / Limpieza")

        st.subheader("📸 Evidencia Final")
        obs_gen = st.text_area("Comentarios Supervisor *")
        fotos_u = st.file_uploader("Fotos de Inspección", accept_multiple_files=True)

        submit = st.form_submit_button("✅ ENVIAR REPORTE COMPLETO")

    if submit:
        if not tec or not fotos_u:
            st.error("⚠️ El nombre y las fotos son obligatorios.")
        else:
            with st.spinner("Sincronizando con Excel..."):
                links = []
                for img in fotos_u[:10]:
                    try:
                        r_img = requests.post("https://api.imgbb.com/1/upload", data={"key": IMGBB_API_KEY, "image": base64.b64encode(img.read()).decode('utf-8')})
                        if r_img.status_code == 200:
                            links.append(r_img.json()['data']['url'])
                    except:
                        pass
                
                payload = {
                    "action": "insertar",
                    "tecnico": tec, "ubicacion": ubi,
                    "p_izq": p_izq, "c_der": c_der, "p_del": p_del, "p_pos": p_pos, "obs_p": obs_p,
                    "muebles": muebles, "cableado": cableado, "energia": energia, "iluminacion": ilumina, "obs_int": obs_int,
                    "leds_s": leds_s, "t_izq": t_izq, "t_der": t_der, "tv_izq": tv_izq, "tv_der": tv_der, "obs_pan": obs_pan,
                    "internet": internet, "wifi": wifi, "lockers": "OK", "camaras": camaras, "boton": boton,
                    "branding": branding, "l_int": l_int, "l_ext": l_ext, "obs_mod": obs_mod,
                    "obs_gen": obs_gen, "fotos": ";".join(links)
                }
                
                try:
                    r_final = requests.post(URL_BRIDGE, json=payload, timeout=35)
                    if r_final.status_code == 200:
                        st.success("¡Reporte Guardado con éxito!")
                        st.balloons()
                except:
                    st.error("Error de conexión con la base de datos.")

# --- MÓDULO 2: REPORTES ---
else:
    st.header("📊 Consulta de Reportes")
    try:
        r = requests.get(URL_BRIDGE, timeout=40)
        data = r.json()
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            df_limpio = df[df['Ubicación'].isin(KIOSCOS_OFICIALES)]
            
            c1, c2 = st.columns(2)
            sel_k = c1.selectbox("Kiosco:", df_limpio['Ubicación'].unique())
            df_k = df_limpio[df_limpio['Ubicación'] == sel_k]
            sel_f = c2.selectbox("Fecha:", df_k['Fecha'].unique())
            
            rep = df_k[df_k['Fecha'] == sel_f].iloc[0]
            
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.subheader(f"📍 REPORTE TÉCNICO: {sel_k}")
            st.write(f"**Técnico:** {rep.get('Técnico', 'N/A')} | **Fecha:** {sel_f}")
            
            st.markdown('<div class="section-header">⚙️ ESTRUCTURA Y ACCESOS</div>', unsafe_allow_html=True)
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Piloto Izq", rep.get('Piloto Izquierdo', 'N/A'))
            r2.metric("Copiloto Der", rep.get('Copiloto Derecho', 'N/A'))
            r3.metric("Delantera", rep.get('Delantera', 'N/A'))
            r4.metric("Posterior", rep.get('Posterior', 'N/A'))
            st.markdown(f"**Notas:**<div class='text-wrap'>{rep.get('Obs Puertas', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-header">🏠 INTERIORES</div>', unsafe_allow_html=True)
            i1, i2, i3, i4 = st.columns(4)
            i1.metric("Muebles", rep.get('Muebles', 'N/A'))
            i2.metric("Cableado", rep.get('Cableado', 'N/A'))
            i3.metric("Energía", rep.get('Energía', 'N/A'))
            i4.metric("Luz", rep.get('Iluminación', 'N/A'))
            st.markdown(f"**Notas:**<div class='text-wrap'>{rep.get('Obs Interiores', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-header">🖥️ SISTEMAS IT</div>', unsafe_allow_html=True)
            it1, it2, it3, it4 = st.columns(4)
            it1.metric("Totem Izq", rep.get('Totem Izquierdo', 'N/A'))
            it2.metric("Totem Der", rep.get('Totem Derecho', 'N/A'))
            it3.metric("TV Izq", rep.get('TV Izquierdo', 'N/A'))
            it4.metric("TV Der", rep.get('TV Derecha', 'N/A'))
            st.write(f"**LEDs:** {rep.get('Leds Superiores', 'N/A')}")
            st.markdown(f"**Notas:**<div class='text-wrap'>{rep.get('Obs Pantallas', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-header">🌐 CONECTIVIDAD</div>', unsafe_allow_html=True)
            o1, o2, o3, o4 = st.columns(4)
            o1.metric("Net", rep.get('Internet', 'N/A'))
            o2.metric("Wifi", rep.get('Wifi', 'N/A'))
            o3.metric("Cam", rep.get('Cámaras Seguridad', 'N/A'))
            o4.metric("Boton", rep.get('Boton Panico', 'N/A'))

            st.markdown('<div class="section-header">✨ ESTÉTICA</div>', unsafe_allow_html=True)
            st.write(f"**Branding:** {rep.get('Branding', 'N/A')} | **Limp Int:** {rep.get('Limp Interna', 'N/A')} | **Limp Ext:** {rep.get('Limp Externa', 'N/A')}")
            st.markdown(f"**Notas:**<div class='text-wrap'>{rep.get('Obs Modulo', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-header">📝 COMENTARIOS FINALES</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='text-wrap'>{rep.get('Obs Generales', 'N/A')}</div>", unsafe_allow_html=True)
            
            if rep.get('Fotos'):
                st.markdown('<div class="section-header">📸 EVIDENCIA</div>', unsafe_allow_html=True)
                st.image(str(rep['Fotos']).split(";"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")
