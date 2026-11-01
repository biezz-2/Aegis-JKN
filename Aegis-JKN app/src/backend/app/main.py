"""Main FastAPI application entry point."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from .core.config import get_settings, Settings
from .middleware.logging_middleware import StructuredLoggingMiddleware, setup_logging
from .middleware.error_handler import global_exception_handler
from .middleware.auth_middleware import AuthMiddleware, MTLSMiddleware
from .core.security.audit import AuditMiddleware
from .api.graph.router import router as graph_router
from .api.simulation.router import router as simulation_router
from .api.report.router import router as report_router
from .api.metrics.router import router as metrics_router
from .api.jobs.router import router as jobs_router
from .api.vector.router import router as vector_router
from .api.auth.router import router as auth_router
from .api.mcp.router import router as mcp_router

def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    """
    settings = get_settings()

    # Setup structured logging
    setup_logging(
        log_level=settings.log_level,
        log_format=settings.log_format
    )

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        openapi_url="/docs/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # --- OpenTelemetry Setup (Only when explicitly enabled) ---
    import os
    if os.getenv("ENABLE_OTEL", "false").lower() == "true":
        try:
            from opentelemetry import trace
            from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

            provider = TracerProvider()
            otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")
            processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otel_endpoint, insecure=True))
            provider.add_span_processor(processor)
            trace.set_tracer_provider(provider)
            FastAPIInstrumentor.instrument_app(app)
            logging.info("OpenTelemetry tracing enabled.")
        except Exception as e:
            logging.warning(f"Failed to initialize OpenTelemetry: {e}")
    else:
        logging.info("OpenTelemetry disabled (default for local development).")
    # --- Middlewares ---

    # 1. GZip for payload compression
    app.add_middleware(GZipMiddleware)

    # 2. Structured Logging Middleware (must be near top to catch everything)
    app.add_middleware(StructuredLoggingMiddleware)

    # 3. CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    # 4. Audit Middleware (logs all requests for compliance)
    app.add_middleware(AuditMiddleware)

    # 5. Authentication Middleware (JWT validation)
    app.add_middleware(AuthMiddleware)

    # 6. mTLS Middleware (service-to-service auth)
    app.add_middleware(MTLSMiddleware)

    # --- Error Handling ---
    app.add_exception_handler(Exception, global_exception_handler)

    # --- API Routes ---
    app.include_router(auth_router, prefix=settings.api_prefix)
    app.include_router(graph_router, prefix=settings.api_prefix)
    app.include_router(simulation_router, prefix=settings.api_prefix)
    app.include_router(report_router, prefix=settings.api_prefix)
    app.include_router(metrics_router, prefix=settings.api_prefix)
    app.include_router(jobs_router, prefix=settings.api_prefix)
    app.include_router(vector_router, prefix=settings.api_prefix)
    app.include_router(mcp_router, prefix=settings.api_prefix)
    @app.on_event("startup")
    async def startup_event():
        from .services.ml_service import ml_service
        from .services.vector_db_service import vector_db_service
        from .services.qdrant_service import qdrant_service
        ml_service.load_model()
        # Vector DB is optional for local runs (no Docker/Qdrant): only connect when configured
        if settings.qdrant_url:
            for name, init in (
                ("vector_db_service", vector_db_service.initialize),
                ("qdrant_service", lambda: qdrant_service.initialize(settings)),
            ):
                try:
                    await init()
                except Exception as e:
                    logging.getLogger(__name__).info(
                        "%s unavailable (%s). Semantic features disabled.", name, e
                    )
        else:
            logging.info("Vector DB / Qdrant not configured (degraded mode for local run).")

    @app.get("/", tags=["Root"])

    async def root():
        """Health check for the root endpoint."""
        return {"status": "online", "message": "Aegis-JKN Backend is running"}

    return app

app = create_app()
