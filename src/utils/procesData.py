import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def proces_data(df):
    """
    Prepara los datos para el modelo, aplicando feature engineering y transformaciones.
    """
    
    scaler = StandardScaler()


    # Crear nuevas características
    df["DTI"] = df["pasivos"] / df["ingresos"] # Relacion deuda / ingresos mensuales
    df["capacidad_de_pago"] = df["ingresos"] - df["gastos"] # Capacidad de pago
    df["ratio_endeudamiento"] = df["pasivos"] / df["activos"]   # Evitar división por cero
    df["ratio_gastos_ingresos"] = df["gastos"] / df["ingresos"]
    df["deuda_neta"] = df["pasivos"] - df["activos"]
    df["ratio_ahorro"] = (df["ingresos"] - df["gastos"]) / df["ingresos"]
    df["ratio_deuda_activos_netos"] = df["pasivos"] / (df["activos"] - df["pasivos"])
    df["capacidad_pago_ajustada"] = df["capacidad_de_pago"] / df["ingresos"]
    df["endeudamiento_critico"] = np.where(df["ratio_endeudamiento"] > 0.5, 1, 0)
    
    # Convertir es_pep a binario
    df["es_pep"] = df["es_pep"].map({"Sí": 1, "No": 0})
    
    # Aplicar transformaciones no lineales
    df["edad_cuadrado"] = df["edad"] ** 2
    df["log_monto_solicitado"] = np.log(df["monto_solicitado"] + 1)
    # df["log_ingresos"] = np.log(df["ingresos"] + 1)
    # df["log_gastos"] = np.log(df["gastos"] + 1)
    # df["log_activos"] = np.log(df["activos"] + 1)
    # df["log_pasivos"] = np.log(df["pasivos"] + 1)
    df["log_ratio_gastos_ingresos"] = np.log(df["ratio_gastos_ingresos"] + 1)
    df["ratio_ahorro_escalado"] = scaler.fit_transform(df[["ratio_ahorro"]])
    df["deuda_neta_escalado"] = scaler.fit_transform(df[["deuda_neta"]])
    df["log_ratio_endeudamiento"] = np.log(df["ratio_endeudamiento"] + 1)
    df["log_DTI"] = np.log(df["DTI"] + 1)
    df["capacidad_de_pago_escalado"] = scaler.fit_transform(df[["capacidad_de_pago"]])
     
    if "referencias_familiares" in df:
        df.drop(["referencias_familiares"], axis=1, inplace=True)

    df.drop(["edad","monto_solicitado", "ingresos", "gastos", "activos", "pasivos", "ratio_gastos_ingresos", "ratio_ahorro", "deuda_neta", "ratio_endeudamiento", "DTI", "capacidad_de_pago", "origen_fondos"], axis=1, inplace=True)
    
    
    return df