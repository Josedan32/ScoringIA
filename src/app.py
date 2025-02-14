from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from models.predict_data import CreditScoringInput
from utils.handleError import handle_error  
from decimal import Decimal

app = FastAPI(
    title="API de Scoring Crediticio",
    description="Esta API predice el puntaje crediticio basado en múltiples factores financieros.",
    version="1.0.2"
)

# Cargar el modelo y otros elementos necesarios
try:
    model = joblib.load("scoring.pkl")
except FileNotFoundError as e:
    print("Este es el error actual:" , e)
    raise handle_error(status=500,title="Error al cargar el modelo", detail=str(e))

# Definicion el endpoint para realizar la predicción
@app.post("/predict", tags=["Predicción"])
def predict(input_data: CreditScoringInput):
    try:
        data_dict = input_data.dict()

        # Convertir los valores Decimal a float
        for key, value in data_dict.items():
            if isinstance(value, Decimal):
                data_dict[key] = float(value)

        # Cada valor se convierte en una lista de un solo elemento
        data_dict = {key: [value] for key, value in data_dict.items()}

        # Crear un DataFrame de pandas
        df = pd.DataFrame(data_dict)

        # Realizar la predicción
        prediction = model.predict(df)

        # Devolver el resultado de la predicción
        return {"scoring": int(prediction[0])}

    except HTTPException as e:
        raise e
    except Exception as e:
         print("This is the error: ", e)
         raise handle_error(
            status=500,
            title="Error desconocido",
            detail=str(e),
            instance="/predict"
        )
    