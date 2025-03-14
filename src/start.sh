#!/bin/bash

echo "|_|-|_|-|Entrenando Modelo XGBOOST para scoring|-|_|-|_|"
python main.py

echo "|_|-|_|-|Iniciando la API para el scoring|-|_|-|_|"
uvicorn app:app --host 0.0.0.0 --port 8000