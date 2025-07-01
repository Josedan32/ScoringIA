from pydantic import BaseModel, Field, condecimal, conint
from typing import Literal, List, Optional

# Definición del modelo de datos de entrada para la predicción del scoring
class SolicitudScoring(BaseModel):
    edad: Optional[conint(ge=19, le=100)] = None  # Edad entre 18 y 100
    estado_civil: Optional[Literal['Soltero', 'Divorciado', 'Viudo', 'Casado', 'Unión Libre']] = None  # Se limita a estos valores
    tipo_de_vivienda: Optional[Literal['Arrendada', 'Familiar', 'Propia']] = None  # Se limita a estos valores
    estrato: Optional[conint(ge=1, le=6)] = None  # Estrato socioeconómico
    nivel_academico: Optional[Literal['Educación básica', 'Bachiller', 'Pregrado', 'Posgrado']] = None   # Nivel académico
    profesion : Optional[Literal["2145"]] = None  # Tipo de ocupación (texto libre)
    tipo_contrato: Optional[Literal['Contrato temporal', 'Contrato por obra o labor', "Contrato de aprendizaje", "Contrato de trabajo a término fijo","Contrato de trabajo a término indefinido"]] = None  # Tipo de contrato
    antiguedad_trabajo: Optional[conint(ge=0)] = None  # Antigüedad laboral en años
    cargo: Optional[Literal["Técnico","Asistencial","Profesional", "Asesor", "Directivo"]] = None  # Cargo (texto libre)
    ingresos: condecimal(ge=0)  # Ingresos totales
    gastos: condecimal(ge=0)   # Gastos totales
    activos: condecimal(ge=0)   # Activos totales
    pasivos: condecimal(ge=0)  # Pasivos totales
    origen_fondos: Optional[Literal["Salario"]] = None
    declara_renta: Optional[Literal['Sí', 'No']] = None # Declara renta (Sí/No)
    es_pep: Optional[Literal['No']] = None # Es persona políticamente expuesta (Sí/No)
    responsabilidad_fiscal_exterior: Optional[Literal['No']] = None # Responsabilidad fiscal en el exterior (Sí/No)
    tipo_credito: Optional[Literal['Crédito de consumo']] = None # Tipo de crédito
    monto_solicitado: condecimal(ge=0) # Monto solicitado
    destino_credito: Literal['Viajes y turismo', 'viajes', 'Viajes'] # Destino del crédito