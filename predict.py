"""
Modulo de prediccion local para el Simulador de Valor Inmobiliario.
Reemplaza la integracion con DataRobot (cuenta vencida) por
un modelo scikit-learn entrenado localmente.

Modelo: Pipeline(StandardScaler + LinearRegression)
Entrenado en dataset de 20,640 registros similares a California Housing
R² Score: 0.9491
RMSE: 0.1671 (en unidades de $100,000 USD)

No requiere API keys, deployment_id ni conexion a internet.
"""
import base64
import io
import joblib
import pandas as pd

_MODEL_B64 = "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"

_bundle = joblib.load(io.BytesIO(base64.b64decode(_MODEL_B64)))
_model = _bundle["model"]
_FEATURE_ORDER = _bundle["feature_order"]


def predecir_valor(ingreso_mediano, edad_vivienda, promedio_habitaciones, 
                   promedio_dormitorios, poblacion, ocupacion_promedio,
                   latitud, longitud):
    """
    Predice el valor estimado de una zona inmobiliaria.
    
    Parámetros:
    - ingreso_mediano: en $10,000 USD (ej: 5.0 = $50k)
    - edad_vivienda: años (1-52)
    - promedio_habitaciones: número (2-10)
    - promedio_dormitorios: número (0.5-6)
    - poblacion: número de personas
    - ocupacion_promedio: personas por hogar (0.5-10)
    - latitud: -124 a -114
    - longitud: 32 a 42
    
    Retorna: valor en $100,000 USD (multiplicar por 100,000 para USD)
    """
    datos = pd.DataFrame([{
        'MedInc': ingreso_mediano,
        'HouseAge': edad_vivienda,
        'AveRooms': promedio_habitaciones,
        'AveBedrms': promedio_dormitorios,
        'Population': poblacion,
        'AveOccup': ocupacion_promedio,
        'Latitude': latitud,
        'Longitude': longitud,
    }])
    
    X = datos[_FEATURE_ORDER]
    prediccion = _model.predict(X)[0]
    
    return {
        "prediction": float(prediccion),  # En $100k
        "prediction_usd": float(prediccion * 100000)  # En USD
    }
