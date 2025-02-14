import pandas as pd
import numpy as np

def proces_data(df):
    """
    Prepara los datos para el modelo, aplicando feature engineering y transformaciones.
    """
    # Crear nuevas características
    df["ratio_endeudamiento"] = df["pasivos"] / (df["activos"] + 1e-6)  # Evitar división por cero
    df["ratio_gastos_ingresos"] = df["gastos"] / (df["ingresos"] + 1e-6)
    df["ratio_ahorro"] = (df["ingresos"] - df["gastos"]) / (df["ingresos"] + 1e-6)

    # Contar el número de orígenes de fondos
    df["num_origen_fondos"] = df["origen_fondos"].str.split(", ").apply(len)
    
    # Convertir es_pep a binario
    df["es_pep"] = df["es_pep"].map({"Sí": 1, "No": 0})
    
    # Aplicar transformaciones no lineales
    df["log_ingresos"] = np.log(df["ingresos"] + 1)
    df["edad_cuadrado"] = df["edad"] ** 2

    return df