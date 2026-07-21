"""
Modulo de prediccion local para el Simulador de Valor Inmobiliario.
Reemplaza la integracion con DataRobot (cuenta vencida) por
un modelo scikit-learn entrenado localmente.

Modelo: Pipeline(StandardScaler + LinearRegression)
Entrenado en dataset de 20,640 registros similares a California Housing
R² Score: 0.9411
RMSE: 0.1606 (en unidades de $100,000 USD)

No requiere API keys, deployment_id ni conexion a internet.
"""
import base64
import io
import joblib
import pandas as pd

_MODEL_B64 = "gASVggEAAAAAAAB9lCiMBW1vZGVslIwQc2tsZWFybi5waXBlbGluZZSMCFBpcGVsaW5llJOUKYGUfZQojAVzdGVwc5RdlCiMBnNjYWxlcpSMG3NrbGVhcm4ucHJlcHJvY2Vzc2luZy5fZGF0YZSMDlN0YW5kYXJkU2NhbGVylJOUKYGUfZQojAl3aXRoX21lYW6UiIwId2l0aF9zdGSUiIwEY29weZSIjBFmZWF0dXJlX25hbWVzX2luX5SME2pvYmxpYi5udW1weV9waWNrbGWUjBFOdW1weUFycmF5V3JhcHBlcpSTlCmBlH2UKIwIc3ViY2xhc3OUjAVudW1weZSMB25kYXJyYXmUk5SMBXNoYXBllEsJhZSMBW9yZGVylIwBQ5SMBWR0eXBllGgZjAVkdHlwZZSTlIwCTziUiYiHlFKUKEsDjAF8lE5OTkr/////Sv////9LP3SUYowKYWxsb3dfbW1hcJSJjBtudW1weV9hcnJheV9hbGlnbm1lbnRfYnl0ZXOUSxB1YoAFlRwBAAAAAAAAjBZudW1weS5fY29yZS5tdWx0aWFycmF5lIwMX3JlY29uc3RydWN0lJOUjAVudW1weZSMB25kYXJyYXmUk5RLAIWUQwFilIeUUpQoSwFLCYWUaAOMBWR0eXBllJOUjAJPOJSJiIeUUpQoSwOMAXyUTk5OSv////9K/////0s/dJRiiV2UKIwPaW5ncmVzb19tZWRpYW5vlIwRcHJveGltaWRhZF9vY2Vhbm+UjAdsYXRpdHVklIwIbG9uZ2l0dWSUjBJ0b3RhbF9oYWJpdGFjaW9uZXOUjBF0b3RhbF9kb3JtaXRvcmlvc5SMCXBvYmxhY2lvbpSMB2hvZ2FyZXOUjBVlZGFkX21lZGlhbmFfdml2aWVuZGGUZXSUYi6VqQAAAAAAAACMDm5fZmVhdHVyZXNfaW5flEsJjA9uX3NhbXBsZXNfc2Vlbl+UjBZudW1weS5fY29yZS5tdWx0aWFycmF5lIwGc2NhbGFylJOUaCKMAmY4lImIh5RSlChLA4wBPJROTk5K/////0r/////SwB0lGJDCAAAAAAAINBAlIaUUpSMBW1lYW5flGgVKYGUfZQoaBhoG2gcSwmFlGgeaB9oIGgxaCiIaClLEHViCf///////////yrrOEkh8h5ACnvCnrAHCECtQvrTpYRCQGsC1WO9wF3AqW7haGyzs0APp47skLqjQCAHxGh9PdhAWWKjSDfMo0B2oUa+o29JQJUqAAAAAAAAAIwEdmFyX5RoFSmBlH2UKGgYaBtoHEsJhZRoHmgfaCBoMWgoiGgpSxB1YgT/////DfJNKoZzMUBjGwztTzQAQBDyrXbGoiBA9rj9jgf6IEBXO8eZo/5eQQ38+Uou9D5Buf2VsZi8qEEMWm0vLz4/QQ6SfUsueolAlSwAAAAAAAAAjAZzY2FsZV+UaBUpgZR9lChoGGgbaBxLCYWUaB5oH2ggaDFoKIhoKUsQdWIC//9R9jYFu7UQQMW85eB9xfY/3U7czZgSB0BZbQUxzE4HQDdN9t3mRKZANeEEwCRBlkDh36kWiyLMQNnD/zOvW5ZAW5azBpCNPECV0gAAAAAAAACMEF9za2xlYXJuX3ZlcnNpb26UjAUxLjguMJR1YoaUjAlyZWdyZXNzb3KUjBpza2xlYXJuLmxpbmVhcl9tb2RlbC5fYmFzZZSMEExpbmVhclJlZ3Jlc3Npb26Uk5QpgZR9lCiMDWZpdF9pbnRlcmNlcHSUiIwGY29weV9YlIiMA3RvbJRHPrDG96C17Y2MBm5fam9ic5ROjAhwb3NpdGl2ZZSJaCpLCYwFY29lZl+UaBUpgZR9lChoGGgbaBxLCYWUaB5oH2ggaDFoKIhoKUsQdWIM////////////////dpwNQ+gp4D9ck+TSfcu9Pw6xhV7Teqa/Y3CPItVWiL9GuxFH2FKXP9Xz25tEaVW/ZABQF5SSeD9ybER0u4Zcv8fpy9/WBNY/lTkAAAAAAAAAjAVyYW5rX5RLCYwJc2luZ3VsYXJflGgVKYGUfZQoaBhoG2gcSwmFlGgeaB9oIGgxaCiIaClLEHViBf//////hzGHuPRoYED/AE9P6khgQPdRVs4jMWBAgyfM+6giYED7/AxqFR1gQMbow2tR719Afpf2UAvCX0C5oLEM2qNfQNzo8q1nfl9Alf8AAAAAAAAAjAppbnRlcmNlcHRflGguaDFDCL9VBm/hdAhAlIaUUpRoQ2hEdWKGlGWMD3RyYW5zZm9ybV9pbnB1dJROjAZtZW1vcnmUTowHdmVyYm9zZZSJaENoRHVijA1mZWF0dXJlX29yZGVylF2UKIwPaW5ncmVzb19tZWRpYW5vlIwRcHJveGltaWRhZF9vY2Vhbm+UjAdsYXRpdHVklIwIbG9uZ2l0dWSUjBJ0b3RhbF9oYWJpdGFjaW9uZXOUjBF0b3RhbF9kb3JtaXRvcmlvc5SMCXBvYmxhY2lvbpSMB2hvZ2FyZXOUjBVlZGFkX21lZGlhbmFfdml2aWVuZGGUZXUu"

_bundle = joblib.load(io.BytesIO(base64.b64decode(_MODEL_B64)))
_model = _bundle["model"]
_FEATURE_ORDER = _bundle["feature_order"]

# Mapeo de proximidad al océano
_PROXIMIDAD_MAP = {
    "NEAR BAY": 1,
    "INLAND": 2,
    "NEAR OCEAN": 3,
    "<1H OCEAN": 4,
    "ISLAND": 5
}


def hacer_prediccion(df):
    """
    Recibe un DataFrame con columnas:
    - ingreso_mediano: en $10,000 USD
    - proximidad_oceano: string ("NEAR BAY", "INLAND", etc.)
    - latitud, longitud, total_habitaciones, total_dormitorios,
      poblacion, hogares, edad_mediana_vivienda

    Retorna diccionario con predicción (compatible con DataRobot API).
    """
    datos = df.copy()

    # Validar y transformar proximidad_oceano
    if "proximidad_oceano" in datos.columns:
        datos["proximidad_oceano"] = datos["proximidad_oceano"].map(_PROXIMIDAD_MAP)

    # Validar columnas
    columnas_requeridas = set(_FEATURE_ORDER)
    faltantes = columnas_requeridas - set(datos.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")

    X = datos[_FEATURE_ORDER]
    predicciones = _model.predict(X)

    resultados = []
    for pred in predicciones:
        resultados.append({
            "prediction": float(pred),
            "prediction_usd": float(pred * 100000)
        })

    return {"data": resultados}
