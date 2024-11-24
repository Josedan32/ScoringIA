### API de Scoring Crediticio

Esta es una API diseñada para predecir el puntaje crediticio de un usuario basado en múltiples factores financieros. La predicción se realiza utilizando un modelo de Machine Learning previamente entrenado.

## Estructura del Proyecto
src/
- data/: Contiene los datos de entrada para entrenar y testear el modelo de scoring.
- models/predict_data.py: Define la estructura del modelo de datos de entrada para las predicciones.
- utils/handleError.py: Manejo centralizado de errores para la API.
- utils/procesData.py: Preprocesamiento de los datos de entrada antes de la predicción.
- app.py: Código principal de la API.
- docker-compose.yml: Configuración para ejecutar la API en un contenedor Docker.
- Dockerfile: Archivo Docker para la construcción de la imagen del proyecto.
- scoring.py: Script que entrena y guarda el modelo de scoring.
- start.sh: Script para entrenar el modelo y lanzar la API.
- README.md: Documentación del proyecto.

## Ejecución

1. Construir y ejecutar el contenedor
docker-compose up --build
2. La API estará disponible en http://localhost:8000

## Endpoints
1. /predict (POST)
Realizar una predicción del puntaje crediticio.
- Formato JSON:
{
    "edad": 22,
    "estado_civil": "Soltero",
    "tipo_vivienda": "Arrendada",
    "estrato": 2,
    "historial_credito": 450,
    "nivel_ingresos_est": 1200000,
    "ingresos_totales": 1300000,
    "gastos_totales": 1000000,
    "activos": 2000000,
    "pasivos": 3000000,
    "limite_credito": 1500000,
    "monto_credito_solicitado": 2000000,
    "destino_credito": "Consumo",
    "declara_renta": false,
    "pep": false,
    "score_riesgo": 520
}

- Response
{
  "puntaje_crediticio_predicho": 153
}

2. /openapi.json
Documentación en formato OpenAPI.

## Componentes Clave

### scoring.py
Entrena un modelo de machine learning usando GradientBoostingRegressor para predecir el puntaje crediticio. Los datos se escalan y las variables categóricas se codifican usando LabelEncoder.
### app.py
Implementa la API con FastAPI y utiliza el modelo entrenado para responder las solicitudes.
#### utils/handleError.py
Centraliza el manejo de errores en la API para mantener consistencia en las respuestas.
### start.sh
Ejecuta el script de entrenamiento y lanza la API.

## Tecnologías Utilizadas
- Lenguaje: Python
- Framework Web: FastAPI
- Machine Learning: Scikit-learn
- Contenedores: Docker