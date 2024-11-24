from fastapi import FastAPI, HTTPException
import joblib
from models.predict_data import CreditScoringInput
from utils.handleError import handle_error
from utils.procesData import proces_data

app = FastAPI(
    title="API de Scoring Crediticio",
    description="Esta API predice el puntaje crediticio basado en múltiples factores financieros.",
    version="1.0.0"
)

# Cargar el modelo y otros elementos necesarios
try:
    model = joblib.load("scoring.pkl")
    scaler = joblib.load("scaler.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
except FileNotFoundError as e:
    print("Este es el error actual:" , e)
    raise handle_error(status=500,title="Error al cargar los modelos", detail=str(e))

# Definicion el endpoint para realizar la predicción
@app.post("/predict", tags=["Predicción"])
def predict(input_data: CreditScoringInput):
    try:
        # Procesamiento de los datos
        data_dict = input_data.dict()
        df = proces_data(data_dict, label_encoders, scaler)

        
        # Realizar la predicción
        prediction = model.predict(df)

        # Devolver el resultado de la predicción
        return {"puntaje_crediticio_predicho": int(prediction[0])}
    except HTTPException as e:
        raise e
    except Exception as e:
         raise handle_error(
            status=500,
            title="Error desconocido",
            detail=str(e),
            instance="/predict"
        )
    
    
