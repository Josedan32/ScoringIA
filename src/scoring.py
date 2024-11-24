import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

#Datos de entrenamiento y testeo
df = pd.read_csv("./data/data_scoring.csv");

# Convertir variables categóricas a numéricas usando Label Encoding
# Mantener los LabelEncoders para su reutilización en nuevas predicciones
label_encoders = {}
categorical_columns = ['estado_civil', 'tipo_vivienda', 'destino_credito']

for column in categorical_columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column].astype(str))
    label_encoders[column] = le

# Separar características (X) y variable objetivo (y)
X = df.drop('puntaje_aprobado', axis=1)
y = df['puntaje_aprobado']

# Dividir datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizar características numéricas
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Modelo: Gradient Boosting Regressor para predecir el puntaje de crédito
model = GradientBoostingRegressor()
model.fit(X_train, y_train)

# Predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

# Evaluar el desempeño del modelo
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared (R2): {r2}")

# Guardar el modelo, escalador y codificadores
joblib.dump(model, 'scoring.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')