import streamlit as st
import pandas as pd
from predict_immobiliario import predecir_valor

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
- Edad mediana de las viviendas
- Promedio de habitaciones
- Promedio de dormitorios
- Población
- Ocupación promedio
- Latitud y Longitud
⚠️ Debido a que el modelo trabaja con zonas geográficas completas, es normal observar valores de cientos o miles de habitantes.
""")

# ==================================
# EXPLICACIÓN DE UBICACIÓN
# ==================================
st.markdown("""
## 🌍 Interpretación de la ubicación en el modelo
La **latitud y longitud** representan la ubicación geográfica del bloque censal y es un factor clave en la valoración del mercado inmobiliario.
📌 Estas variables influyen significativamente en la predicción del valor del mercado.
""")

# ==================================
# INPUTS
# ==================================
st.sidebar.header("🏠 Variables del modelo")

ingreso_mediano = st.sidebar.slider(
    "Ingreso medio de la zona ($10k USD)",
    0.5, 15.0, 5.0, 0.1
)

edad_vivienda = st.sidebar.slider(
    "Edad mediana de viviendas (años)",
    1, 52, 30, 1
)

promedio_habitaciones = st.sidebar.slider(
    "Promedio de habitaciones",
    2.0, 10.0, 5.0, 0.1
)

promedio_dormitorios = st.sidebar.slider(
    "Promedio de dormitorios",
    0.5, 6.0, 1.5, 0.1
)

poblacion = st.sidebar.number_input(
    "Población de la zona",
    100, 35000, 1500, 100
)

ocupacion_promedio = st.sidebar.slider(
    "Ocupación promedio (personas/hogar)",
    0.5, 10.0, 3.0, 0.1
)

latitud = st.sidebar.slider(
    "Latitud",
    32.0, 42.0, 34.0, 0.01
)

longitud = st.sidebar.slider(
    "Longitud",
    -124.0, -114.0, -118.0, 0.01
)

# ==================================
# PREDICCIÓN
# ==================================
if st.button("🔍 Estimar valor de mercado"):
    try:
        resultado = predecir_valor(
            ingreso_mediano=ingreso_mediano,
            edad_vivienda=edad_vivienda,
            promedio_habitaciones=promedio_habitaciones,
            promedio_dormitorios=promedio_dormitorios,
            poblacion=poblacion,
            ocupacion_promedio=ocupacion_promedio,
            latitud=latitud,
            longitud=longitud
        )

        st.success("✅ Predicción generada correctamente")

        st.subheader("🏡 Resultado del modelo")
        valor_usd = resultado["prediction_usd"]
        st.metric("Valor estimado de la zona", f"${valor_usd:,.0f} USD")

        st.subheader("📊 Interpretación del mercado")
        if valor_usd < 150000:
            st.info("🔵 Zona de valor accesible")
        elif valor_usd < 300000:
            st.warning("🟡 Zona de valor medio")
        else:
            st.error("🔴 Zona de alto valor inmobiliario")

        st.subheader("📍 Ubicación del análisis")
        st.map(pd.DataFrame({"lat": [latitud], "lon": [longitud]}))

    except Exception as e:
        st.error(f"❌ Error en la predicción: {str(e)}")

st.info("""
ℹ️ Importante
Las variables como habitaciones, dormitorios, población y ocupación corresponden
a características agregadas de una zona geográfica completa y no a una vivienda individual.
""")

# ==================================
# CONTACTO
# ==================================
st.markdown("---")
st.subheader("📲 Contacto profesional")
col1, col2 = st.columns(2)

with col1:
    mensaje_wa = "Hola%20Kely,%20vi%20tu%20Simulador%20Inmobiliario%20con%20IA%20y%20me%20interesa%20conocer%20m%C3%A1s%20sobre%20tu%20enfoque%20t%C3%A9cnico%20para%20empresas."

    st.markdown(f"""
    <a href="https://wa.me/573015704518?text={mensaje_wa}" target="_blank">
    <button style="background:#25D366;color:white;padding:10px 18px;border-radius:8px;border:none;cursor:pointer;font-weight:bold;">
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
st.markdown("""
### 👩‍💻 Kely Jhojana Hincapié Zapata
Especialista en Analítica de Datos | Administración Financiera | Tecnóloga en Gestión de Redes de Datos
📌 Proyecto: Simulador inmobiliario basado en Machine Learning (scikit-learn), desplegado en Streamlit Cloud
""")
