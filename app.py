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
# FUNCIÓN DE PREDICCIÓN (ROBUSTA)
# ==================================
def hacer_prediccion(df):

    url = f"{HOST}/api/v2/deployments/{DEPLOYMENT_ID}/predictions"

    df = df.copy()

    # =========================
    # FIX CRÍTICO DE EDAD (CSV + manual)
    # =========================
    if "edad_dias" not in df.columns:

        if "edad_anhios" in df.columns:
            df["edad_dias"] = df["edad_anhios"] * 365

        elif "edad_anios" in df.columns:
            df["edad_dias"] = df["edad_anios"] * 365

        elif "edad_anios" not in df.columns:
            return {"error": "No se encontró columna de edad válida"}

    # =========================
    # RENOMBRAR VARIABLES (DataRobot)
    # =========================
    df = df.rename(columns={
        "edad_dias": "age",
        "genero": "gender",
        "estatura_cm": "height",
        "peso_kg": "weight",
        "presion_sistolica": "ap_hi",
        "presion_diastolica": "ap_lo",
        "colesterol": "cholesterol",
        "glucosa": "gluc",
        "fuma": "smoke",
        "consume_alcohol": "alco",
        "actividad_fisica": "active",
        "enfermedad_cardiovascular": "cardio"
    })

    datos = df.to_dict(orient="records")

    response = requests.post(url, headers=headers, json=datos)

    if response.status_code != 200:
        return {"error": response.text}

    return response.json()


# ==================================
# STREAMLIT CONFIG
# ==================================
st.set_page_config(
    page_title="Predicción de Riesgo Cardiovascular",
    page_icon="🩺",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align: center; color: #2E86C1;'>🩺 Predictor de Riesgo Cardiovascular</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Ingrese los datos del paciente o cargue un archivo CSV.</p>",
    unsafe_allow_html=True
)

# ==================================
# INPUT MANUAL
# ==================================
st.sidebar.header("Datos del paciente")

genero = st.sidebar.selectbox("Género", ["Masculino", "Femenino"])
edad_anios = st.sidebar.slider("Edad (años)", 18, 100, 40)
estatura_cm = st.sidebar.slider("Estatura (cm)", 120, 220, 170)
peso_kg = st.sidebar.slider("Peso (kg)", 30, 200, 70)
presion_sistolica = st.sidebar.slider("Presión Sistólica", 80, 220, 120)
presion_diastolica = st.sidebar.slider("Presión Diastólica", 50, 150, 80)
glucosa = st.sidebar.slider("Glucosa", 50, 300, 100)

fuma = st.sidebar.selectbox("¿Fuma?", ["No", "Sí"])
consume_alcohol = st.sidebar.selectbox("¿Alcohol?", ["No", "Sí"])
actividad_fisica = st.sidebar.selectbox("Actividad Física", ["Baja", "Media", "Alta"])
enfermedad_cardiovascular = st.sidebar.selectbox("Cardiovascular", ["No", "Sí"])
colesterol = st.sidebar.selectbox("Colesterol", [1, 2, 3])

# ==================================
# CODIFICACIÓN
# ==================================
genero = 1 if genero == "Masculino" else 0
fuma = 1 if fuma == "Sí" else 0
consume_alcohol = 1 if consume_alcohol == "Sí" else 0
enfermedad_cardiovascular = 1 if enfermedad_cardiovascular == "Sí" else 0

actividad_map = {"Baja": 0, "Media": 1, "Alta": 2}
actividad_fisica = actividad_map[actividad_fisica]

# ==================================
# DATAFRAME
# ==================================
datos_manual = pd.DataFrame([{
    "edad_dias": edad_anios * 365,
    "genero": genero,
    "estatura_cm": estatura_cm,
    "peso_kg": peso_kg,
    "presion_sistolica": presion_sistolica,
    "presion_diastolica": presion_diastolica,
    "colesterol": colesterol,
    "glucosa": glucosa,
    "fuma": fuma,
    "consume_alcohol": consume_alcohol,
    "actividad_fisica": actividad_fisica,
    "enfermedad_cardiovascular": enfermedad_cardiovascular
}])

# ==================================
# RESULTADO UI
# ==================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Datos ingresados")
    st.dataframe(datos_manual, use_container_width=True)

with col2:

    debug = st.checkbox("Debug técnico")

    if st.button("🔍 Predecir"):

        resultado = hacer_prediccion(datos_manual)

        if "error" in resultado:
            st.error(resultado["error"])
        else:

            if debug:
                st.json(resultado)

            fila = resultado["data"][0]
            pred = fila["prediction"]

            st.metric("Predicción de riesgo", str(pred))

            if pred == 1:
                st.error("🔴 Alto riesgo cardiovascular")
            else:
                st.success("🟢 Bajo riesgo cardiovascular")


# ==================================
# PREDICCIÓN CSV
# ==================================
st.markdown("### 📂 Predicción en lote")

archivo_csv = st.file_uploader("Subir CSV", type=["csv"])

if archivo_csv:

    datos_csv = pd.read_csv(archivo_csv)

    st.dataframe(datos_csv.head())

    if st.button("Predecir CSV"):

        if "id_paciente" not in datos_csv.columns:
            datos_csv["id_paciente"] = range(1, len(datos_csv) + 1)

        resultado = hacer_prediccion(datos_csv)

        if "error" in resultado:
            st.error(resultado["error"])
        else:

            predicciones = [x["prediction"] for x in resultado["data"]]

            datos_csv["prediccion"] = predicciones

            st.success("Predicciones generadas")
            st.dataframe(datos_csv)

            st.download_button(
                "Descargar CSV",
                datos_csv.to_csv(index=False).encode("utf-8"),
                "predicciones.csv",
                "text/csv"
            )


# ==================================
# FOOTER + CONTACTO (CORREGIDO LINKEDIN)
# ==================================
st.markdown("---")

st.markdown("""
### 👩‍💻 Desarrollado por Kely Jhojana Hincapié Zapata

Especialista en Analítica de Datos | Administración Financiera | Tecnóloga en Redes de Datos

📌 Proyecto: Modelo predictivo de riesgo cardiovascular con DataRobot + Streamlit

---

""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <a href="https://wa.me/573015704518?text=Hola%20Kely,%20quiero%20más%20información"
    target="_blank">
    <button style="background:#25D366;color:white;padding:10px;border-radius:8px;">
    WhatsApp Business
    </button>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <a href="https://www.linkedin.com/in/kely-jhojana-hincapie-zapata-502587130/"
    target="_blank">
    <button style="background:#0077B5;color:white;padding:10px;border-radius:8px;">
    LinkedIn
    </button>
    </a>
    """, unsafe_allow_html=True)
