#Columnas categoricas y numercias
categorical_features = [ 
    "estado_civil",
    "tipo_de_vivienda",
    "nivel_academico",
    "profesion",
    "tipo_contrato",
    #"actividad_economica",
    "cargo",
    "declara_renta",
    "responsabilidad_fiscal_exterior",
    "tipo_credito",
    "destino_credito"
]

numeric_features = [
    #"edad",
    "edad_cuadrado",
    "estrato",
    "antiguedad_trabajo",
    "log_monto_solicitado", #"monto_solicitado",
    # "log_ingresos", #"ingresos",
    # "log_gastos", #"gastos",
    # "log_activos", #"activos",
    # "log_pasivos", #"pasivos",
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

feature_weights = {
    "log_DTI": 6,  
    "capacidad_de_pago_escalado": 6,
    "log_ratio_endeudamiento": 6
}