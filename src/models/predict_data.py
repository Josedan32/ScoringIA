from pydantic import BaseModel, Field, condecimal, conint
from typing import Literal, List, Optional

# Definición del modelo de datos de entrada para la predicción del scoring
class SolicitudScoring(BaseModel):
    edad: conint(ge=19, le=45)  # Edad entre 18 y 100
    estado_civil: Literal['Soltero', 'Divorciado', 'Viudo', 'Casado', 'Unión Libre']  # Se limita a estos valores
    tipo_de_vivienda: Literal['Arrendada', 'Familiar', 'Propia']  # Se limita a estos valores
    estrato: conint(ge=1, le=6)  # Estrato socioeconómico
    nivel_academico: Literal['Educación básica', 'Bachiller', 'Pregrado', 'Posgrado']  # Nivel académico
    profesion : Literal["2145"]  # Tipo de ocupación (texto libre)
    tipo_contrato: Literal['Contrato temporal', 'Contrato por obra o labor', "Contrato de aprendizaje", "Contrato de trabajo a término fijo","Contrato de trabajo a término indefinido"]  # Tipo de contrato
    antiguedad_trabajo: conint(ge=0)  # Antigüedad laboral en años
    cargo: Literal["Técnico","Asistencial","Profesional", "Asesor", "Directivo"]  # Cargo (texto libre)
    ingresos: condecimal(ge=0)  # Ingresos totales
    gastos: condecimal(ge=0)  # Gastos totales
    activos: condecimal(ge=0)  # Activos totales
    pasivos: condecimal(ge=0)  # Pasivos totales
    origen_fondos: Literal["Salario"] 
    declara_renta: Literal['Sí', 'No']  # Declara renta (Sí/No)
    es_pep: Literal['No']  # Es persona políticamente expuesta (Sí/No)
    responsabilidad_fiscal_exterior: Literal['No']  # Responsabilidad fiscal en el exterior (Sí/No)
    tipo_credito: Literal['Crédito de consumo']  # Tipo de crédito
    monto_solicitado: condecimal(ge=0)  # Monto solicitado
    destino_credito: Literal['Viajes y turismo']  # Destino del crédito