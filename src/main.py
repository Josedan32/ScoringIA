import pandas as pd
from models.model import train_model
if __name__ == "__main__":
    model, feature_importance_df  = train_model("./data/data_wrc.csv")
    
    caso_3 = pd.DataFrame({
        "edad": [52],
        "estado_civil": ["Casado"],
        "tipo_de_vivienda": ["Propia"],
        "estrato": [4],
        "nivel_academico": ["Universitario"],
        "profesion": ["Médico"],
        "tipo_contrato": ["Independiente"],
        "antiguedad_trabajo": [25],
        "actividad_economica": ["Salud"],
        "cargo": ["Médico Especialista"],
        "ingresos": [25000000],
        "gastos": [9000000],
        "activos": [700000000],
        "pasivos": [150000000],
        "origen_fondos": ["Consultas Privadas, Salario"],
        "declara_renta": ["Sí"],
        "referencias_familiares": [2],
        "es_pep": ["No"],
        "responsabilidad_fiscal_exterior": ["No"],
        "tipo_credito": ["Hipotecario"],
        "monto_solicitado": [500000000],
        "destino_credito": ["Compra de Vivienda"],
        # "scoring_puntaje": [340]
    })
    caso_5 = pd.DataFrame({
        "edad": [60],
        "estado_civil": ["Casado"],
        "tipo_de_vivienda": ["Propia"],
        "estrato": [5],
        "nivel_academico": ["Posgrado"],
        "profesion": ["Director de Finanzas"],
        "tipo_contrato": ["Independiente"],
        "antiguedad_trabajo": [35],
        "actividad_economica": ["Finanzas"],
        "cargo": ["Director Financiero"],
        "ingresos": [35000000],
        "gastos": [15000000],
        "activos": [2000000000],
        "pasivos": [80000000000],
        "origen_fondos": ["Salario, Inversiones"],
        "declara_renta": ["Sí"],
        "referencias_familiares": [5],
        "es_pep": ["No"],
        "responsabilidad_fiscal_exterior": ["No"],
        "tipo_credito": ["Hipotecario"],
        "monto_solicitado": [700000000],
        "destino_credito": ["Compra de Vivienda"],
        # "scoring_puntaje": [345]
    })

    casos = [caso_3, caso_5]

    for i, caso, in enumerate(casos,1):
        scoring_predicho = model.predict(caso)
        print(f"Caso {i} - Scoring Predicho: {scoring_predicho[0]}")