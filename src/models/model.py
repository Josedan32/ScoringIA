import joblib
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from models.tranformer import PrepararDatosTransformer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from utils.preprocessing import get_preprocesor

def train_model(data_path):

    data = pd.read_csv(data_path)


    X = data.drop(columns=["scoring_puntaje","referencias_familiares"])
    y = data["scoring_puntaje"]

    #Dividir en entrenamiento y pruebas
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    

    #Columnas categoricas y numercias
    categorical_features = [ "estado_civil", "tipo_de_vivienda","nivel_academico","profesion", "tipo_contrato", "actividad_economica", "cargo","declara_renta", "responsabilidad_fiscal_exterior", "tipo_credito", "destino_credito" ]
    numeric_features = [
        "edad",
        "edad_cuadrado",
        "estrato",
        "antiguedad_trabajo",
        "log_monto_solicitado", #"monto_solicitado",
        "log_ingresos", #"ingresos",
        "log_gastos", #"gastos",
        "log_activos", #"activos",
        "log_pasivos", #"pasivos",
        "log_ratio_gastos_ingresos",#"ratio_gastos_ingresos",
        "ratio_ahorro_escalado", #"ratio_ahorro",
        "deuda_neta_escalado", #"deuda_neta",
        "es_pep",
        "log_ratio_endeudamiento", #"ratio_endeudamiento",
        "log_DTI", #"DTI",
        "capacidad_de_pago_escalado", #"capacidad_de_pago",
        #"num_origen_fondos",
        "ratio_deuda_activos_netos",
        "capacidad_pago_ajustada",
        "endeudamiento_critico"
    ]

    #Obtener el preprocesador
    preprocesor = get_preprocesor(numeric_features, categorical_features)

    #Definicion de pipeline
    model = Pipeline(steps=[
        ("preparar_datos", PrepararDatosTransformer()),
        ("preprocessor", preprocesor),
        ("regressor", XGBRegressor(
            random_state=42,
            max_depth=6,  
            colsample_bytree=0.8,  
            min_child_weight=1,
            reg_lambda=0.5,  # Reduce la regularización para que XGBoost tome más en cuenta ciertas variables
            reg_alpha=0.5

        ))
    ])

    # Aplicar preprocesamiento a los datos de entrenamiento antes de calcular los pesos
    # X_train_transformed = model.named_steps["preprocessor"].fit_transform(X_train)

    # # Obtener los nombres de las columnas transformadas
    # cat_names = model.named_steps["preprocessor"].named_transformers_["cat"].get_feature_names_out(categorical_features)
    # feature_names = np.concatenate([numeric_features, cat_names])

    # # Convertir la salida transformada en un DataFrame con nombres de columnas correctos
    # X_train_transformed_df = pd.DataFrame(X_train_transformed, columns=feature_names)

    # # Ahora sí, calcular los pesos con las variables transformadas
    # weights = 1 + 2 * X_train_transformed_df["log_DTI"] + 2 * X_train_transformed_df["capacidad_de_pago_escalado"]


    #Entrenar modelo
    model.fit(X_train, y_train)

    #Evaluacion del modelo
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"|-|-|-|-| MSE: {mse} |-|-|-|-|")
    print(f"|-|-|-|-| R2: {r2} |-|-|-|-|")

    #Guardar el modelo
    joblib.dump(model, "XgboostScoring.pkl")

    #Obtener la importancia de las variables
    cat_names = model.named_steps["preprocessor"].named_transformers_["cat"].get_feature_names_out(categorical_features)
    feature_names = np.concatenate([numeric_features, cat_names])
    importances = model.named_steps["regressor"].feature_importances_

    feature_importance_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
    feature_importance_df = feature_importance_df.sort_values(by="Importance", ascending=False)

    print(feature_importance_df.head(10))

    return model, feature_importance_df
    