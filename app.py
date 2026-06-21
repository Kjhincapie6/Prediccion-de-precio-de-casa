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

if not API_KEY or not DEPLOYMENT_ID or not HOST:
    st.error("❌ Faltan credenciales de DataRobot")
    st.stop()

headers = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json"
}

# ==================================
# FUNCIÓN PREDICCIÓN
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
# UI PRINCIPAL
# ==================================
st.set_page_config(
    page_title="Simulador Inmobiliario",
    page_icon="🏡",
    layout="wide"
)

st.title("🏡 Simulador de Valor del Mercado Inmobiliario por Zona")

# ==================================
# EXPLICACIÓN DEL MODELO
# ==================================
st.markdown("""
## 📊 ¿Qué predice realmente este modelo?

Este modelo está basado en datasets tipo **California Housing Dataset**.

👉 NO predice el valor de una casa individual.  
👉 Predice el **valor promedio del mercado inmobiliario en una zona geográfica (bloque censal)**.

---

📌 Cada fila del dataset representa una ZONA, no una vivienda.

### Variables del modelo:
- ingreso_mediano → ingreso promedio del sector  
- total_habitaciones → total de habitaciones en la zona  
- total_hogares → número de hogares en el área  
- población → habitantes del bloque  
- edad_mediana_vivienda → antigüedad promedio de viviendas  

⚠️ Los valores varían según la ubicación (zonas costeras vs interiores).
""")

# ==================================
# INPUTS
# ==================================
st.sidebar.header("🏠 Variables del modelo")

ingreso_mediano = st.sidebar.slider("Ingreso medio de la zona", 0.5, 15.0, 5.0, 0.1)

proximidad_oceano = st.sidebar.selectbox(
    "Proximidad al océano",
    ["NEAR BAY", "INLAND", "NEAR OCEAN", "<1H OCEAN", "ISLAND"]
)

latitud = st.sidebar.slider("Latitud", 32.0, 42.0, 34.0, 0.01)
longitud = st.sidebar.slider("Longitud", -124.0, -114.0, -118.0, 0.01)

total_habitaciones = st.sidebar.number_input("Total habitaciones (zona)", 100, 10000, 2000)
total_dormitorios = st.sidebar.number_input("Total dormitorios (zona)", 50, 5000, 500)
poblacion = st.sidebar.number_input("Población (zona)", 100, 50000, 1500)
hogares = st.sidebar.number_input("Hogares (zona)", 50, 5000, 500)
edad_mediana_vivienda = st.sidebar.number_input("Edad mediana vivienda", 1, 100, 30)

# ==================================
# DATAFRAME
# ==================================
datos = pd.DataFrame([{
    "ingreso_mediano": ingreso_mediano,
    "proximidad_oceano": proximidad_oceano,
    "latitud": latitud,
    "longitud": longitud,
    "total_habitaciones": total_habitaciones,
    "total_dormitorios": total_dormitorios,
    "poblacion": poblacion,
    "hogares": hogares,
    "edad_mediana_vivienda": edad_mediana_vivienda
}])

# ==================================
# PREDICCIÓN
# ==================================
if st.button("🔍 Estimar valor de mercado"):

    resultado = hacer_prediccion(datos)

    if "error" in resultado:
        st.error(f"Error DataRobot: {resultado['error']}")
    else:

        pred = resultado["data"][0]["prediction"]

        st.success("✅ Predicción generada correctamente")

        st.subheader("🏡 Resultado del modelo")
        st.metric("Valor estimado de la zona", f"${pred:,.2f} USD")

        # Interpretación
        st.subheader("📊 Interpretación del mercado")

        if pred < 150000:
            st.info("🔵 Zona de valor accesible")
        elif pred < 300000:
            st.warning("🟡 Zona de valor medio")
        else:
            st.error("🔴 Zona de alto valor inmobiliario")

        # Mapa
        st.subheader("📍 Ubicación del análisis")
        st.map(pd.DataFrame({"lat": [latitud], "lon": [longitud]}))

        # Interpretación profesional
        st.info("""
📌 Interpretación profesional:
Este valor representa el precio promedio del mercado inmobiliario en la zona analizada.
No corresponde a una vivienda individual.
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
    <a href="https://www.linkedin.com/in/kely-jhojana-hincapi%C3%A9-zapata-502587130/"
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

📌 Proyecto: Simulador inmobiliario basado en Machine Learning con DataRobot + Streamlit
""")
