from fastapi import FastAPI
# from prometheus_fastapi_instrumentator import Instrumentator
from app.api import routes_auth
from app.api import routes_code_input, routes_analyze_code, routes_code_metrics, routes_inject_bugs
from app.middleware.logging_middleware import LoggingMiddleware
from app.core.exceptions import register_exception_handlers

app = FastAPI(
    title="Code Reviewer and Bug Generator API",
    description="API for code analysis, metrics, and bug injection using RAG"
)

# Link middleware
app.add_middleware(LoggingMiddleware)

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

# Root endpoint
@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Code Review and Bug Generator API", "docs": "/docs"}

# Link endpoints
app.include_router(routes_auth.router, tags=["Auth"])

# RAG Endpoints
app.include_router(routes_code_input.router, prefix="/rag", tags=["RAG - Code Input"])
app.include_router(routes_analyze_code.router, prefix="/rag", tags=["RAG - Analysis"])
app.include_router(routes_code_metrics.router, prefix="/rag", tags=["RAG - Metrics"])
app.include_router(routes_inject_bugs.router, prefix="/rag", tags=["RAG - Bug Injection"])

# Add exception handler
register_exception_handlers(app)