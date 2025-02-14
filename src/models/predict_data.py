from pydantic import BaseModel, Field, condecimal, conint
from typing import Literal, List, Optional

# Definición del modelo de datos de entrada para la predicción del scoring
class CreditScoringInput(BaseModel):
    edad: conint(ge=18, le=100)  # Edad entre 18 y 100
    estado_civil: Literal['Soltero', 'Casado', 'Unión Libre', 'Divorciado', 'Viudo']  # Se limita a estos valores
    tipo_de_vivienda: Literal['Arrendada', 'Propia', 'Familiar']  # Se limita a estos valores
    estrato: conint(ge=1, le=6)  # Estrato socioeconómico
    nivel_academico: Literal['Bachiller', 'Universitario', 'Posgrado']  # Nivel académico
    tipo_ocupacion: str  # Tipo de ocupación (texto libre)
    tipo_contrato: Literal['Indefinido', 'Término fijo', 'Temporal']  # Tipo de contrato
    antiguedad_trabajo: conint(ge=0)  # Antigüedad laboral en años
    actividad_economica: str  # Actividad económica (texto libre)
    cargo: str  # Cargo (texto libre)
    ingresos: condecimal(ge=0)  # Ingresos totales
    gastos: condecimal(ge=0)  # Gastos totales
    activos: condecimal(ge=0)  # Activos totales
    pasivos: condecimal(ge=0)  # Pasivos totales
    origen_fondos: str  # Origen de los fondos (texto libre)
    declara_renta: Literal['Sí', 'No']  # Declara renta (Sí/No)
    referencias_familiares: conint(ge=0)  # Número de referencias familiares
    es_pep: Literal['Sí', 'No']  # Es persona políticamente expuesta (Sí/No)
    responsabilidad_fiscal_exterior: Literal['Sí', 'No']  # Responsabilidad fiscal en el exterior (Sí/No)
    tipo_credito: Literal['Consumo', 'Hipotecario', 'Microcrédito', 'Educación', 'Vehículo', 'Libranza']  # Tipo de crédito
    monto_solicitado: condecimal(ge=0)  # Monto solicitado
    destino_credito: Literal['Libre Inversión', 'Compra de Vivienda', 'Capital de Trabajo', 'Educación', 'Salud']  # Destino del crédito