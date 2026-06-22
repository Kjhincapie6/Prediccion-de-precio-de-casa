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

Este sistema está basado en datasets tipo **California Housing Dataset**.

👉 NO predice viviendas individuales.  
👉 Predice el **valor promedio del mercado inmobiliario por zona geográfica (bloque censal)**.
📌 Cada registro representa una ZONA del mercado, no una casa.
⚠️ Los valores dependen fuertemente de la ubicación.
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

        st.subheader("📊 Interpretación del mercado")

        if pred < 150000:
            st.info("🔵 Zona de valor accesible")
        elif pred < 300000:
            st.warning("🟡 Zona de valor medio")
        else:
            st.error("🔴 Zona de alto valor inmobiliario")

        st.subheader("📍 Ubicación del análisis")
        st.map(pd.DataFrame({"lat": [latitud], "lon": [longitud]}))

        st.info("""
📌 Interpretación profesional:
El valor mostrado corresponde al precio promedio del mercado inmobiliario en la zona analizada.
No representa una vivienda individual.
""")

# ==================================
# CONTACTO
# ==================================
st.markdown("---")
st.subheader("📲 Contacto profesional")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <a href="https://wa.me/573015704518?text=Hola%20Kely,%20estuve%20revisando%20tu%20proyecto%20de%20simulador%20inmobiliario%20con%20Machine%20Learning.%20Estoy%20interesado%20en%20implementar%20un%20modelo%20similar%20en%20mi%20empresa%20para%20an%C3%A1lisis%20de%20valor%20de%20mercado%20por%20zonas.%20Quisiera%20conocer%20m%C3%A1s%20sobre%20tu%20enfoque%20t%C3%A9cnico%20y%20la%20posibilidad%20de%20adaptaci%C3%B3n%20a%20un%20entorno%20empresarial."
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

Especialista en Analítica de Datos | Administración Financiera | Tecnóloga en Gestión de Redes de Datos  

📌 Proyecto: Simulador inmobiliario basado en Machine Learning con DataRobot + Streamlit
""")
