import streamlit as st
import pandas as pd
import requests
import os
import matplotlib.pyplot as plt

# ==================================
# CONFIGURACIÓN DATAROBOT
# ==================================
API_KEY = os.getenv("DATAROBOT_API_KEY")
DEPLOYMENT_ID = os.getenv("DATAROBOT_DEPLOYMENT_ID")
HOST = os.getenv("DATAROBOT_HOST")

if not API_KEY or not DEPLOYMENT_ID or not HOST:
    st.error("Faltan variables de entorno de DataRobot")
    st.stop()

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ==================================
# FUNCIÓN PREDICCIÓN
# ==================================
def hacer_prediccion(df):

    url = f"{HOST}/api/v2/deployments/{DEPLOYMENT_ID}/predictions"

    try:
        response = requests.post(
            url,
            headers=headers,
            json=df.to_dict(orient="records"),
            timeout=30
        )
    except Exception as e:
        return {"error": str(e)}

    if response.status_code != 200:
        return {"error": response.text}

    try:
        return response.json()
    except:
        return {"error": "Respuesta inválida de DataRobot"}


# ==================================
# CONFIG STREAMLIT
# ==================================
st.set_page_config(
    page_title="Predicción Precio Viviendas",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Predictor de Precio de Viviendas")

st.markdown("""
Modelo de Machine Learning entrenado en DataRobot para estimar el valor medio de viviendas
utilizando variables socioeconómicas y geográficas.
""")

# ==================================
# INPUTS
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
# PREDICCIÓN
# ==================================
if st.button("🔍 Predecir precio de vivienda"):

    resultado = hacer_prediccion(datos)

    if "error" in resultado:
        st.error(resultado["error"])
    else:

        pred = resultado["data"][0]["prediction"]

        st.success("Predicción generada correctamente")

        st.metric("🏠 Valor estimado", f"${pred:,.2f} USD")

        # ==================================
        # MAPA
        # ==================================
        st.subheader("📍 Ubicación de la vivienda")

        st.map(pd.DataFrame({"lat": [latitud], "lon": [longitud]}))

        # ==================================
        # GRÁFICO MEJORADO
        # ==================================
        st.subheader("📊 Comparación de variables")

        fig, ax = plt.subplots()
        ax.bar(
            ["Ingreso medio", "Precio estimado"],
            [ingreso_mediano * 10000, pred]
        )
        ax.set_ylabel("Escala comparable")
        st.pyplot(fig)

# ==================================
# BOTONES CONTACTO
# ==================================
st.markdown("---")

st.subheader("📲 Contacto")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <a href="https://wa.me/573015704518?text=Hola%20Kely,%20vi%20tu%20proyecto%20de%20predicción%20de%20viviendas"
    target="_blank">
    <button style="background-color:#25D366;color:white;padding:10px 20px;border-radius:8px;border:none;">
    💬 WhatsApp Business
    </button>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <a href="www.linkedin.com/in/kely-jhojana-hincapi%C3%A9-zapata-502587130"
    target="_blank">
    <button style="background-color:#0077B5;color:white;padding:10px 20px;border-radius:8px;border:none;">
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

**Especialista en Analítica de Datos | Profesional en Administración Financiera | Tecnóloga en Gestión de Redes de Datos**

---

📌 Proyecto: Sistema de predicción de precios de viviendas basado en Machine Learning  
Integrado con DataRobot y desplegado en Streamlit Cloud para análisis interactivo en tiempo real.
""")
