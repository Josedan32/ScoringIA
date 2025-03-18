import joblib
import numpy as np
import pandas as pd
from utils.procesData import proces_data
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from utils.preprocessing import get_preprocesor
from data.features_data import categorical_features, numeric_features, feature_weights

def train_model(data_path):

    data = pd.read_csv(data_path)
    data = proces_data(data)


    X = data.drop(columns=["scoring_puntaje","favorable","cuotas_pagar"])
    y = data["scoring_puntaje"]

   
    # Excluir variables con peso del escalado
    weighted_features = list(feature_weights.keys())
    scaled_numeric_features = [f for f in numeric_features if f not in weighted_features]


    #Obtener el preprocesador
    preprocessor = get_preprocesor(scaled_numeric_features, categorical_features)

    #Dividir en entrenamiento y pruebas
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Aplicar transformaciones
    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

     # Obtener nombres de columnas transformadas
    transformed_feature_names = preprocessor.get_feature_names_out()
    passthrough_features = weighted_features
    # Convertir a DataFrame después de la transformación
    feature_names = list(transformed_feature_names) + passthrough_features

    X_train = pd.DataFrame(X_train, columns=feature_names[:X_train.shape[1]])
    X_test = pd.DataFrame(X_test, columns=feature_names[:X_test.shape[1]])

     # Aplicar pesos manualmente a las variables que se dejaron fuera del escalado
    for col, weight in feature_weights.items():
        if col in X_train.columns:
            print(col, flush=True)
            X_train[col] *= weight
            X_test[col] *= weight


    model = XGBRegressor(
        n_estimators=200, 
        learning_rate=0.05, 
        max_depth=5, 
        subsample=0.8, 
        colsample_bytree=0.8,
        scale_pos_weight=1.2,
        reg_lambda=0.1,
        reg_alpha=0.1
    )
    model.fit(X_train, y_train)

    #Evaluacion del modelo
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"|-|-|-|-| MSE: {mse} |-|-|-|-|", flush=True)
    print(f"|-|-|-|-| R2: {r2} |-|-|-|-|", flush=True)
    print("\n\n")

    #Guardar el modelo
    joblib.dump(model, "XgboostScoring.pkl")
    joblib.dump(preprocessor, "preprocessor.pkl")

    # Obtener importancia de variables
    feature_importance = model.feature_importances_
    min_length = min(len(feature_importance), len(X_train.columns))
    
    feature_importance_df = pd.DataFrame({
        "feature": X_train.columns[:min_length],
        "importance": feature_importance[:min_length]
    }).sort_values(by="importance", ascending=False)

    print(feature_importance_df.head(), flush=True)

    print("remainder__log_DTI", feature_importance_df.loc[feature_importance_df["feature"] == "remainder__log_DTI", "importance"].values)
    print("remainder__capacidad_de_pago_escalado", feature_importance_df.loc[feature_importance_df["feature"] == "remainder__capacidad_de_pago_escalado", "importance"].values)
    print("remainder__log_ratio_endeudamiento", feature_importance_df.loc[feature_importance_df["feature"] == "remainder__log_ratio_endeudamiento", "importance"].values)

    print("---TESTS---")
        
    caso_1 = pd.DataFrame({
        "edad": [24],
        "estado_civil": ["Soltero"],
        "tipo_de_vivienda": ["Arrendada"],
        "estrato": [2],
        "nivel_academico": ["Pregrado"],
        "profesion": ["2145"],
        "tipo_contrato": ["Contrato temporal"],
        "antiguedad_trabajo": [1],
        "cargo": ["Técnico"],
        "ingresos": [2200000],
        "gastos": [2000000],
        "activos": [5000000],
        "pasivos": [10000000],
        "origen_fondos": ["Salario"],
        "declara_renta": ["No"],
        "referencias_familiares": [2],
        "es_pep": ["No"],
        "responsabilidad_fiscal_exterior": ["No"],
        "tipo_credito": ["Crédito de consumo"],
        "monto_solicitado": [4500000],
        "destino_credito": ["Viajes y turismo"],
        # "scoring_puntaje": [170]
    })
    caso_2 = pd.DataFrame({
        "edad": [35],
        "estado_civil": ["Casado"],
        "tipo_de_vivienda": ["Propia"],
        "estrato": [4],
        "nivel_academico": ["Pregrado"],
        "profesion": ["2145"],
        "tipo_contrato": ["Contrato de trabajo a término fijo"],
        "antiguedad_trabajo": [5],
        "cargo": ["Profesional"],
        "ingresos": [4200000],
        "gastos": [3000000],
        "activos": [20000000],
        "pasivos": [12000000],
        "origen_fondos": ["Salario"],
        "declara_renta": ["Sí"],
        "referencias_familiares": [2],
        "es_pep": ["No"],
        "responsabilidad_fiscal_exterior": ["No"],
        "tipo_credito": ["Crédito de consumo"],
        "monto_solicitado": [10000000],
        "destino_credito": ["Viajes y turismo"],
        # "scoring_puntaje": [250]
    })
    caso_3 = pd.DataFrame({
        "edad": [40],
        "estado_civil": ["Casado"],
        "tipo_de_vivienda": ["Propia"],
        "estrato": [5],
        "nivel_academico": ["Posgrado"],
        "profesion": ["2145"],
        "tipo_contrato": ["Contrato de trabajo a término indefinido"],
        "antiguedad_trabajo": [12],
        "cargo": ["Directivo"],
        "ingresos": [8500000],
        "gastos": [4000000],
        "activos": [50000000],
        "pasivos": [8000000],
        "origen_fondos": ["Salario"],
        "declara_renta": ["Sí"],
        "referencias_familiares": [2],
        "es_pep": ["No"],
        "responsabilidad_fiscal_exterior": ["No"],
        "tipo_credito": ["Crédito de consumo"],
        "monto_solicitado": [15000000],
        "destino_credito": ["Viajes y turismo"],
        # "scoring_puntaje": [320]
    })
    caso_4 = pd.DataFrame({
        "edad": [42],
        "estado_civil": ["Casado"],
        "tipo_de_vivienda": ["Propia"],
        "estrato": [6],
        "nivel_academico": ["Posgrado"],
        "profesion": ["2145"],
        "tipo_contrato": ["Contrato de trabajo a término indefinido"],
        "antiguedad_trabajo": [7],
        "cargo": ["Directivo"],
        "ingresos": [100000000],
        "gastos": [5000000000],
        "activos": [10000000],
        "pasivos": [5000000000000],
        "origen_fondos": ["Salario"],
        "declara_renta": ["Sí"],
        "referencias_familiares": [2],
        "es_pep": ["No"],
        "responsabilidad_fiscal_exterior": ["No"],
        "tipo_credito": ["Crédito de consumo"],
        "monto_solicitado": [20000000],
        "destino_credito": ["Viajes y turismo"],
        # "scoring_puntaje": [150]
    })
    caso_5 = pd.DataFrame({
        "edad": [40],
        "estado_civil": ["Casado"],
        "tipo_de_vivienda": ["Propia"],
        "estrato": [6],
        "nivel_academico": ["Posgrado"],
        "profesion": ["2145"],
        "tipo_contrato": ["Contrato de trabajo a término indefinido"],
        "antiguedad_trabajo": [10],
        "cargo": ["Directivo"],
        "ingresos": [8000000],
        "gastos": [9000000],
        "activos": [50000000],
        "pasivos": [10000000],
        "origen_fondos": ["Salario"],
        "declara_renta": ["Sí"],
        "referencias_familiares": [2],
        "es_pep": ["No"],
        "responsabilidad_fiscal_exterior": ["No"],
        "tipo_credito": ["Crédito de consumo"],
        "monto_solicitado": [15000000],
        "destino_credito": ["Viajes y turismo"],
        # "scoring_puntaje": [180]
    })
    
    casos = [caso_1,caso_2,caso_3,caso_4,caso_5]
    for i, caso, in enumerate(casos,1):
        caso_process = proces_data(caso)
        caso_procesado = preprocessor.transform(caso_process)
        caso_procesado = pd.DataFrame(caso_procesado, columns=feature_names[:caso_procesado.shape[1]])

        scoring_predicho = model.predict(caso_procesado)
        print(f"Caso {i} - Scoring Predicho: {scoring_predicho[0]}")

    