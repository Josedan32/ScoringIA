from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import os


# Clase que encapsula toda la configuración de telemetría del backend
class TelemetryConfig:
    def __init__(self):
        self.service_name = "scoring-API"
        self.service_version = "1.0.2"
        self.dataset_name = "scoring-api"
        self.honeycomb_api_key = os.getenv("HONEYCOMB_API_KEY", "ij6dtNLWz9xAgsZBpDdjxA")
        self.honeycomb_endpoint = "https://api.honeycomb.io/v1/traces"
        self.tracer = None
        
    def setup_tracing(self):
        """Configura el proveedor de trazas de OpenTelemetry"""
        resource = Resource(attributes={
            ResourceAttributes.SERVICE_NAME: self.service_name,
            "service.version": self.service_version,
            "honeycomb.dataset": self.dataset_name,
        })

        # Crea el proveedor de trazas y le asocia el recurso
        trace_provider = TracerProvider(resource=resource)
        
        # Configura el exportador OTLP para enviar las trazas a Honeycomb vía HTTP
        otlp_exporter = OTLPSpanExporter(
            endpoint=self.honeycomb_endpoint,
            headers={
                "x-honeycomb-team": self.honeycomb_api_key,
                "x-honeycomb-dataset": self.dataset_name
            }
        )

        # Usa un procesador por lotes para mejorar el rendimiento de exportación
        span_processor = BatchSpanProcessor(otlp_exporter)
        trace_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(trace_provider)
        
        self.tracer = trace.get_tracer(__name__)
        return self.tracer
    
    def instrument_fastapi(self, app):
        """Instrumenta la aplicación FastAPI"""
        FastAPIInstrumentor.instrument_app(app)

# Instancia global de configuración
telemetry_config = TelemetryConfig()
telemetry_config.setup_tracing()