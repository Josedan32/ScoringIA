from pydantic import BaseModel, Field, condecimal, conint
from typing import Literal

# Definicion del modelo de datos de entrada para l predicción del scoring
class CreditScoringInput(BaseModel):
    edad: conint(ge=18, le=100) # Edad entre 18 y 100 
    estado_civil: Literal['Soltero', 'Casado', 'Unión Libre', 'Divorciado', 'Viudo'] #Se limita a estos valores
    tipo_vivienda: Literal['Arrendada', 'Propia', 'Familiar'] #Se limita a estos valores
    estrato: conint(ge=1, le=6) 
    historial_credito: conint(ge=0, le=1000)
    nivel_ingresos_est: condecimal(ge=0) #Los ingesos deben ser un valor positivo
    ingresos_totales: condecimal(ge=0)
    gastos_totales: condecimal(ge=0)
    activos: condecimal(ge=0) 
    pasivos: condecimal(ge=0) 
    limite_credito: condecimal(ge=0) 
    monto_credito_solicitado: condecimal(ge=0) 
    destino_credito: Literal['Consumo', 'Vivienda', 'Automóvil', 'Negocio', 'Educación', 'Inversión']
    declara_renta: bool
    pep: bool
    score_riesgo: conint(ge=300, le=950)