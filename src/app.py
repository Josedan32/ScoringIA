from fastapi import FastAPI, HTTPException, Request
import joblib
import pandas as pd
from models.predict_data import SolicitudScoring
from utils.handleError import handle_error
from utils.procesData import proces_data
from utils.tracing import TracingContext, add_span_attributes, time_span_operation
from config.telemetry import telemetry_config
from decimal import Decimal
import time

#configurar telemetria 
tracer = telemetry_config.tracer

app = FastAPI(
    title= "API de Scoring Crediticio",
    description= "Predice el puntaje crediticio basado en factores financieros",
    version= "1.0.2"
)

#Instrumentar FastApi
telemetry_config.instrument_fastapi(app)

@time_span_operation("model_loading")
def load_model():
    with TracingContext("load_model"):
        try:
            return joblib.load("XgboostScoring.pkl")
        except FileNotFoundError as e:
            raise handle_error(
                status=500,
                title="Error al cargar el modelo",
                detail=str(e),
                error = e
            )

def preprocess_input(input_data: SolicitudScoring) -> pd.DataFrame:

    with TracingContext("preprocess_input", {
        "destino_credito": str(input_data.destino_credito),
        "nivel_academico": str(input_data.nivel_academico),
        "estrato": str(input_data.estrato)
    }):
        
        data_dict = input_data.dict()
        data_dict = { 
            key: float(value) if isinstance(value, Decimal) else value for key, value in data_dict.items()
        }
        
        # Convertir cada valor en una lista para el DataFrame
        formatted_data = { key: [value] for key, value in data_dict.items() }
        
        return pd.DataFrame(formatted_data)

model = load_model()
preprocesor = joblib.load("preprocessor.pkl")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    add_span_attributes({
        "app.request.duration_ms": process_time * 1000,
        "app.request.path": str(request.url.path),
        "app.request.method": request.method
    })
    
    response.headers["X-Process-Time"] = str(process_time)
    return response
    

@app.post("/predict", tags=["Prediccion"])
def predict(input_data: SolicitudScoring):

    add_span_attributes({
        "scoring.request_id": str(id(input_data)),
        "scoring.destino_credito": input_data.destino_credito
    })

    try:
        
        if input_data.destino_credito.lower() == "viajes":
            input_data.destino_credito = "Viajes y turismo"
            

        with TracingContext("Preprocesamiento de datos"):
            df = preprocess_input(input_data)

            with TracingContext("proces_data"):
                df = proces_data(df)

        with TracingContext("Transformacion Modelo") as span:
            df_transformed = preprocesor.transform(df)
            span.set_attribute("forma_transformada", f"{df_transformed.shape[0]}x{df_transformed.shape[1]}")

        with TracingContext("Prediccion del modelo") as span:
            start_time = time.time()
            prediction = model.predict(df_transformed)
            prediction_time = time.time() - start_time

            span.set_attribute("resultado", int(prediction[0]))
            span.set_attribute("tiempo_ms", prediction_time * 1000)
            
            add_span_attributes({"scoring.result": int(prediction[0])})
            
        return {"scoring": int(prediction[0])}

    except HTTPException as e:
        add_span_attributes({
            "error": True,
            "error.type": "HTTPException",
            "error.message": str(e.detail)
        })
        raise e
    except Exception as e:
        add_span_attributes({
            "error": True,
            "error.type": type(e).__name__,
            "error.message": str(e)
        })
        raise handle_error(
            status=500, 
            title="Error en la predicción", 
            detail=str(e), 
            instance="/predict", 
            error=e
        )
