import streamlit as st
import pandas as pd
import requests
import os

# ==================================
# CONFIG DATAROBOT
# ==================================
API_KEY = os.getenv("DATAROBOT_API_KEY")
DEPLOYMENT_ID = os.getenv("DATAROBOT_DEPLOYMENT_ID")
HOST = os.getenv("DATAROBOT_HOST")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

if not API_KEY or not DEPLOYMENT_ID or not HOST:
    st.error("Faltan credenciales de DataRobot")
    st.stop()

# ==================================
# PREDICCIÓN
# ==================================
def hacer_prediccion(df):
    url = f"{HOST}/api/v2/deployments/{DEPLOYMENT_ID}/predictions"

    response = requests.post(
        url,
        headers=headers,
        json=df.to_dict(orient="records")
    )

    if response.status_code != 200:
        return {"error": response.text}

    return response.json()

# ==================================
# UI
# ==================================
st.set_page_config(page_title="Simulador Inmobiliario", page_icon="🏡", layout="wide")

st.title("🏡 Simulador Inteligente de Valor de Vivienda")

st.markdown("""
### 📊 ¿Cómo funciona este modelo?

Este sistema NO predice una casa individual.
Predice el **valor promedio del mercado inmobiliario en una zona**, basado en características socioeconómicas.

👉 Lo interpretamos como una **vivienda representativa del sector**
""")

# ==================================
# INPUTS (SIMULACIÓN DE VIVIENDA)
# ==================================
st.sidebar.header("🏠 Perfil de vivienda simulada")

ingreso_mediano = st.sidebar.slider("Nivel de ingreso del sector", 0.5, 15.0, 5.0, 0.1)

proximidad_oceano = st.sidebar.selectbox(
    "Ubicación",
    ["NEAR BAY", "INLAND", "NEAR OCEAN", "<1H OCEAN", "ISLAND"]
)

latitud = st.sidebar.slider("Latitud", 32.0, 42.0, 34.0, 0.01)
longitud = st.sidebar.slider("Longitud", -124.0, -114.0, -118.0, 0.01)

# 🔥 reinterpretación humana (NO técnica)
tipo_vivienda = st.sidebar.selectbox(
    "Tipo de entorno",
    ["Zona urbana", "Zona suburbana", "Zona costera", "Zona rural"]
)

# variables técnicas del modelo (ocultas conceptualmente)
total_habitaciones = st.sidebar.number_input("Habitaciones del sector", 100, 10000, 2000)
total_hogares = st.sidebar.number_input("Hogares en el sector", 50, 5000, 500)
poblacion = st.sidebar.number_input("Población del sector", 100, 50000, 1500)
edad_mediana_vivienda = st.sidebar.number_input("Antigüedad promedio (años)", 1, 100, 30)

# ==================================
# DATAFRAME
# ==================================
datos = pd.DataFrame([{
    "ingreso_mediano": ingreso_mediano,
    "proximidad_oceano": proximidad_oceano,
    "latitud": latitud,
    "longitud": longitud,
    "total_habitaciones": total_habitaciones,
    "total_hogares": total_hogares,
    "poblacion": poblacion,
    "edad_mediana_vivienda": edad_mediana_vivienda
}])

# ==================================
# PREDICCIÓN
# ==================================
if st.button("🔍 Estimar valor de mercado"):

    resultado = hacer_prediccion(datos)

    if "error" in resultado:
        st.error(resultado["error"])
    else:
        pred = resultado["data"][0]["prediction"]

        st.success("✅ Análisis completado")

        # ==================================
        # RESULTADO PRINCIPAL
        # ==================================
        st.metric("🏡 Valor estimado del sector", f"${pred:,.2f} USD")

        # ==================================
        # INTERPRETACIÓN DE NEGOCIO
        # ==================================
        st.subheader("📊 Interpretación del mercado")

        if pred < 150000:
            st.warning("🔵 Zona de precio accesible")
        elif pred < 300000:
            st.info("🟡 Zona de precio medio")
        else:
            st.error("🔴 Zona de alto valor inmobiliario")

        # ==================================
        # MAPA
        # ==================================
        st.subheader("📍 Ubicación del análisis")
        st.map(pd.DataFrame({"lat": [latitud], "lon": [longitud]}))

        # ==================================
        # PERFIL SIMULADO
        # ==================================
        st.subheader("🏠 Perfil de vivienda simulada")

        st.write(f"""
        - Tipo de entorno: {tipo_vivienda}  
        - Ubicación: {proximidad_oceano}  
        - Nivel de ingreso: {ingreso_mediano}  
        - Edad promedio de viviendas: {edad_mediana_vivienda} años  
        """)

# ==================================
# CONTACTO
# ==================================
st.markdown("---")
st.subheader("📲 Contacto profesional")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <a href="https://wa.me/573015704518?text=Hola%20Kely,%20vi%20tu%20simulador%20inmobiliario"
    target="_blank">
    <button style="background:#25D366;color:white;padding:10px 18px;border-radius:8px;border:none;">
    💬 WhatsApp Business
    </button>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <a href="https://www.linkedin.com/in/kely-jhojana-hincapi%C3%A9-zapata-502587130"
    target="_blank">
    <button style="background:#0077B5;color:white;padding:10px 18px;border-radius:8px;border:none;">
    🔗 LinkedIn
    </button>
    </a>
    """, unsafe_allow_html=True)

# ==================================
# FOOTER
# ==================================
st.markdown("---")
st.markdown("""
### 👩‍💻 Kely Jhojana Hincapié Zapata  
Especialista en Analítica de Datos | Administración Financiera | Gestión de Redes de Datos  

📌 Proyecto: Simulador inmobiliario basado en Machine Learning (DataRobot + Streamlit)
""")
