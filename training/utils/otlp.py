"""
OTLP Exporter Setup module.

Module này cấu hình OpenTelemetry OTLP exporter để:
- Gửi traces đến Agent Lightning
- Capture agent execution spans
- Enable distributed tracing
"""

import logging
from typing import Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME


logger = logging.getLogger(__name__)


def setup_otlp_exporter(
    endpoint: str = "http://localhost:4318/v1/traces",
    service_name: str = "agno-agent"
) -> Optional[TracerProvider]:
    """
    Setup OTLP exporter for Agent Lightning.
    
    Args:
        endpoint: OTLP endpoint URL
        service_name: Service name for traces
        
    Returns:
        TracerProvider instance or None if setup fails
    """
    try:
        # Create resource with service name
        resource = Resource(attributes={
            SERVICE_NAME: service_name
        })
        
        # Create tracer provider
        provider = TracerProvider(resource=resource)
        
        # Create OTLP exporter
        otlp_exporter = OTLPSpanExporter(
            endpoint=endpoint,
            timeout=30  # 30 seconds timeout
        )
        
        # Add span processor
        provider.add_span_processor(
            BatchSpanProcessor(otlp_exporter)
        )
        
        # Set as global tracer provider
        trace.set_tracer_provider(provider)
        
        logger.info(f"✅ OTLP exporter configured: {endpoint}")
        return provider
        
    except Exception as e:
        logger.warning(f"⚠️ OTLP exporter setup failed: {e}")
        logger.warning("Continuing without OTLP exporter...")
        return None

