#!/bin/bash

# Ejecutar los archivos de entrenamiento
echo "Entrenando Modelo Scoring"
python scoring.py

# Iniciar la aplicación FastAPI
echo "Iniciando la API..."
uvicorn app:app --host 0.0.0.0 --port 8000
