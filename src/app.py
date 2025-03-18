from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from models.predict_data import SolicitudScoring
from utils.handleError import handle_error
from utils.procesData import proces_data
from decimal import Decimal

app = FastAPI(
    title= "API de Scoring Crediticio",
    description= "Esta API predice el puntaje crediticio basado en múltiples factores financieros",
    version= "1.0.2"
)

def load_model():
    try:
        return joblib.load("XgboostScoring.pkl")
    except FileNotFoundError as e:
        print("Erro al cargar el modelo: ", e)
        raise handle_error(status=500, title="Error al cargar el modelo", detail=str(e))

def preprocess_input(input_data: SolicitudScoring) -> pd.DataFrame:

    data_dict = input_data.dict()
    data_dict = {key: float(value) if isinstance(value, Decimal) else value for key, value in data_dict.items()}
    
    # Convertir cada valor en una lista para el DataFrame
    formatted_data = {key: [value] for key, value in data_dict.items()}
    
    return pd.DataFrame(formatted_data)

model = load_model()
preprocesor = joblib.load("preprocessor.pkl")

@app.post("/predict", tags=["Prediccion"])
def predict(input_data: SolicitudScoring):
    try:
        df = preprocess_input(input_data)
        df = proces_data(df)
        df_transformed = preprocesor.transform(df)

        prediction = model.predict(df_transformed)
        return {"scoring": int(prediction[0])}

    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error en la predicción:", e)
        raise handle_error(status=500, title="Error en la predicción", detail=str(e), instance="/predict")
