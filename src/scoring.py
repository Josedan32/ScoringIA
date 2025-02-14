import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from models.tranformer import PrepararDatosTransformer
# Cargar los datos
data = pd.read_csv("./data/data_example_wrc.csv")

# Preprocesamiento
# Separar características (X) y variable objetivo (y)
X = data.drop(columns=["scoring_puntaje"])
y = data["scoring_puntaje"]

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# columnas categóricas y numéricas
categorical_features = [
    "estado_civil", "tipo_de_vivienda", "nivel_academico", "tipo_ocupacion", "tipo_contrato", "actividad_economica", "cargo", 
    "declara_renta", "responsabilidad_fiscal_exterior", 
    "tipo_credito", "destino_credito"
]
numeric_features = [
    "edad", "estrato", "antiguedad_trabajo", "ingresos","gastos", "activos", "pasivos", "referencias_familiares", "monto_solicitado","ratio_gastos_ingresos", "ratio_ahorro", "num_origen_fondos", 
"es_pep", "log_ingresos", "edad_cuadrado"
]

# Preprocesamiento: OneHotEncoder para categóricas y StandardScaler para numéricas
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

# Crear el pipeline con preprocesamiento y modelo
model = Pipeline(steps=[
    ("preparar_datos",PrepararDatosTransformer()),
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])

# Entrenar el modelo
model.fit(X_train, y_train)

# Predecir en el conjunto de prueba
y_pred = model.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"MSE: {mse}")
print(f"R2: {r2}")

joblib.dump(model, 'scoring.pkl')