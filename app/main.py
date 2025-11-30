from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_code_input, routes_analyze_code, routes_code_metrics, routes_inject_bugs

app = FastAPI(
    title="Code Analyzer and Bug Generator API",
    description="API for code analysis, metrics, and bug injection using Gemini",
    version="1.0.0"
)

# Add CORS middleware - ADD THIS BEFORE YOUR ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "code-analyzer"}

# Root endpoint
@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Code Analyzer and Bug Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "code_input": "/api/code-input",
            "analyze": "/api/analyze-code",
            "metrics": "/api/code-metrics",
            "inject_bugs": "/api/inject-bugs"
        },
        "note": "All endpoints accept an optional 'api_key' parameter. If not provided, API_KEY from environment will be used."
    }

# API Endpoints - No authentication required
app.include_router(routes_code_input.router, prefix="/api", tags=["Code Input"])
app.include_router(routes_analyze_code.router, prefix="/api", tags=["Code Analysis"])
app.include_router(routes_code_metrics.router, prefix="/api", tags=["Code Metrics"])
app.include_router(routes_inject_bugs.router, prefix="/api", tags=["Bug Injection"])