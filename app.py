import streamlit as st
import pandas as pd
import requests
import os

# ==================================
# CONFIGURACIÓN DATAROBOT
# ==================================
API_KEY = os.getenv("DATAROBOT_API_KEY")
DEPLOYMENT_ID = os.getenv("DATAROBOT_DEPLOYMENT_ID")
HOST = os.getenv("DATAROBOT_HOST")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ==================================
# FUNCIÓN PREDICCIÓN
# ==================================
def hacer_prediccion(df):

    url = f"{HOST}/api/v2/deployments/{DEPLOYMENT_ID}/predictions"

    payload = df.to_dict(orient="records")

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return {"error": response.text}

    return response.json()


# ==================================
# CONFIG STREAMLIT
# ==================================
st.set_page_config(
    page_title="Predicción Precio de Viviendas",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Predictor de Precio de Viviendas")

st.markdown("""
Este modelo de Machine Learning estima el **valor medio de una vivienda**
utilizando variables socioeconómicas y geográficas entrenadas en DataRobot.
""")

# ==================================
# INPUTS DEL USUARIO
# ==================================
st.sidebar.header("🔧 Variables del modelo")

ingreso_mediano = st.sidebar.slider("Ingreso medio de la zona", 0.5, 15.0, 5.0)
proximidad_oceano = st.sidebar.selectbox(
    "Proximidad al océano",
    ["NEAR BAY", "INLAND", "NEAR OCEAN", "<1H OCEAN", "ISLAND"]
)

latitud = st.sidebar.slider("Latitud", 32.0, 42.0, 34.0)
longitud = st.sidebar.slider("Longitud", -124.0, -114.0, -118.0)

total_habitaciones = st.sidebar.number_input("Total habitaciones", 1, 10000, 2000)
total_hogares = st.sidebar.number_input("Total hogares", 1, 5000, 500)
poblacion = st.sidebar.number_input("Población", 1, 50000, 1500)
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
    "total_hogares": total_hogares,
    "poblacion": poblacion,
    "edad_mediana_vivienda": edad_mediana_vivienda
}])

# ==================================
# BOTÓN PREDICCIÓN
# ==================================
if st.button("🔍 Predecir precio de vivienda"):

    resultado = hacer_prediccion(datos)

    if "error" in resultado:
        st.error(resultado["error"])
    else:

        pred = resultado["data"][0]["prediction"]

        st.success("Predicción generada correctamente")

        st.metric("🏠 Precio estimado de la vivienda", f"${pred:,.2f} USD")

# ==================================
# FOOTER PROFESIONAL
# ==================================
st.markdown("---")

st.markdown("""
### 👩‍💻 Kely Jhojana Hincapié Zapata

**Especialista en Analítica de Datos | Profesional en Administración Financiera | Tecnóloga en Gestión de Redes de Datos**

---

📌 Proyecto: Modelo predictivo de precios de vivienda basado en Machine Learning  
Este sistema estima el valor medio de una vivienda utilizando variables geográficas y socioeconómicas,
integrado con DataRobot y desplegado en Streamlit para consumo en tiempo real.

---

📱 WhatsApp Business: https://wa.me/573015704518  
🔗 LinkedIn: www.linkedin.com/in/kely-jhojana-hincapié-zapata-502587130
""")
