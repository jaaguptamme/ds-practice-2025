import os

from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_INSTANCE_ID, Resource

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from opentelemetry import trace, metrics # Re-export

def get_tracer_and_meter(service_name: str):
    # Service name is required for most backends
    resource = Resource.create(attributes={
        SERVICE_NAME: service_name,
        SERVICE_INSTANCE_ID: os.getenv('HOSTNAME', ''),
    })
    
    tracerProvider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint="observability:4317", insecure=True)
    )
    tracerProvider.add_span_processor(processor)

    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint="observability:4317", insecure=True)
    )
    meterProvider = MeterProvider(resource=resource, metric_readers=[reader])

    return tracerProvider.get_tracer(service_name), meterProvider.get_meter(service_name)
