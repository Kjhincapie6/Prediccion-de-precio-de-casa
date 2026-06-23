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
# CONFIG STREAMLIT
# ==================================
st.set_page_config(
    page_title="Simulador Inmobiliario",
    page_icon="🏡",
    layout="wide"
)

st.title("🏡 Simulador de Valor del Mercado Inmobiliario por Zona")

# ==================================
# DESCRIPCIÓN PRINCIPAL
# ==================================
st.markdown("""
## 📊 ¿Qué predice este modelo?

Este sistema está basado en datasets tipo **California Housing Dataset** y utiliza técnicas de Machine Learning para estimar el comportamiento del mercado inmobiliario.

👉 **NO predice una vivienda individual.**

👉 Predice el **valor promedio del mercado inmobiliario de una zona geográfica (bloque censal)** utilizando variables socioeconómicas y características del entorno.

📌 Cada registro del conjunto de datos representa una **zona residencial**, no una casa específica.

### 🧠 Variables utilizadas

- Ingreso medio de la zona
- Latitud y longitud
- Total de habitaciones de la zona
- Total de dormitorios de la zona
- Población de la zona
- Número de hogares
- Edad mediana de las viviendas
- Proximidad al océano

⚠️ Debido a que el modelo trabaja con zonas geográficas completas, es normal observar valores de cientos o miles de habitaciones, hogares o habitantes.
""")

# ==================================
# EXPLICACIÓN DE ZONAS (MEJORADA)
# ==================================
st.markdown("""
## 🌍 Interpretación de la ubicación en el modelo

La variable **proximidad al océano** representa la ubicación geográfica del bloque censal y es un factor clave en la valoración del mercado inmobiliario.

Estas categorías no representan tipos de vivienda, sino condiciones del entorno geográfico:

- 🟦 **NEAR BAY** → zonas cercanas a bahías urbanas con alta demanda inmobiliaria  
- 🌊 **NEAR OCEAN** → zonas costeras con alta valorización  
- 🌆 **<1H OCEAN** → ubicaciones cercanas al mar (menos de 1 hora)  
- 🌄 **INLAND** → zonas interiores con menor presión de mercado  
- 🏝️ **ISLAND** → zonas insulares con comportamiento variable  

📌 Esta variable influye significativamente en la predicción del valor del mercado.
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
    "edad_mediana_vivienda
