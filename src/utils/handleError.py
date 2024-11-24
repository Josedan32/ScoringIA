from fastapi import HTTPException


""" 
Crea una excepción HTTP con un formato de respuesta estándar.
Args:
    status (int): El código de estado HTTP de la respuesta.
    title (str): Un título corto describiendo el error.
    detail (str): Una descripción detallada del error.
    instance (str, optional): Un identificador único o ruta para la instancia del error.
Returns:
    HTTPException: Una excepción HTTP configurada con los detalles proporcionados
"""
def handle_error(status: int, title: str, detail: str, instance: str = "/"):
    return HTTPException(
        status_code= status,
        detail={
            "title":title,
            "detail":detail,
            "instance":instance
        }
    )