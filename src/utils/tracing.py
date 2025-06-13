from opentelemetry import trace
from functools import wraps
import time
from typing import Dict, Any, Optional

def get_tracer():
    """Obtiene el trazador actual"""
    return trace.get_tracer(__name__)

def trace_function(span_name: Optional[str] = None):
    """Decorador para instrumentar funciones automáticamente"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            name = span_name or f"{func.__module__}.{func.__name__}"
            
            with tracer.start_as_current_span(name) as span:
                try:
                    result = func(*args, **kwargs)
                    span.set_attribute("success", True)
                    return result
                except Exception as e:
                    span.set_attribute("error", True)
                    span.set_attribute("error.type", type(e).__name__)
                    span.set_attribute("error.message", str(e))
                    raise
        return wrapper
    return decorator

def add_span_attributes(attributes: Dict[str, Any]):
    """Añade atributos al span actual"""
    current_span = trace.get_current_span()
    for key, value in attributes.items():
        current_span.set_attribute(key, value)

def time_span_operation(operation_name: str):
    """Mide el tiempo de una operación y lo añade como atributo"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            current_span = trace.get_current_span()
            current_span.set_attribute(f"{operation_name}.duration_ms", (end_time - start_time) * 1000)
            
            return result
        return wrapper
    return decorator

class TracingContext:
    """Context manager para crear spans personalizados"""
    def __init__(self, span_name: str, attributes: Optional[Dict[str, Any]] = None):
        self.span_name = span_name
        self.attributes = attributes or {}
        self.tracer = get_tracer()
        self.span = None
    
    def __enter__(self):
        self.span = self.tracer.start_as_current_span(self.span_name)
        active_span = self.span.__enter__()
        
        # Añadir atributos iniciales
        for key, value in self.attributes.items():
            active_span.set_attribute(key, value)
        
        return active_span
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.span.set_attribute("error", True)
            self.span.set_attribute("error.type", exc_type.__name__)
            self.span.set_attribute("error.message", str(exc_val))
        
        self.span.__exit__(exc_type, exc_val, exc_tb)