"""
Routes for code metrics endpoint.
Calculates code quality metrics and issue distribution using RAG and Gemini API.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.core.dependencies import get_current_user, get_api_key
from app.RAG import get_code_metrics, initialize_vector_store_and_embeddings

router = APIRouter()

# Global vector store cache
_vector_store_cache = None
_embedding_model_cache = None


def get_vector_store_and_embeddings():
    """Get or initialize vector store and embedding model."""
    global _vector_store_cache, _embedding_model_cache
    
    if _vector_store_cache is None or _embedding_model_cache is None:
        _embedding_model_cache, _vector_store_cache = initialize_vector_store_and_embeddings()
    
    return _embedding_model_cache, _vector_store_cache


class MetricsRequest(BaseModel):
    """Request model for code metrics."""
    query: Optional[str] = Field(
        default="Provide overall code quality, security metrics, bug density, and issue distribution.",
        description="Natural language query describing the metrics needed"
    )


class SummaryMetrics(BaseModel):
    """Model for code quality metrics."""
    code_quality_score: int
    security_rating: int
    bug_density: int
    critical_issue_count: int


class IssueDistribution(BaseModel):
    """Model for issue distribution."""
    security_vulnerabilities: int
    code_smells: int
    best_practices: int
    performance_issues: int


class MetricsResponse(BaseModel):
    """Response model for code metrics."""
    status: str
    summary_metrics: SummaryMetrics
    issue_distribution: IssueDistribution


@router.post(
    "/code-metrics",
    response_model=MetricsResponse,
    summary="Calculate Code Metrics",
    description="Calculate code quality metrics and issue distribution for loaded code.",
)
def code_metrics_endpoint(
    request: MetricsRequest,
    user=Depends(get_current_user),
    _=Depends(get_api_key)
):
    """
    Get code quality metrics and issue distribution.
    
    - **query**: Natural language description of metrics needed (optional, uses default if not provided)
    
    Default Query: "Provide overall code quality, security metrics, bug density, and issue distribution."
    """
    try:
        embedding_model, vector_store = get_vector_store_and_embeddings()
        
        # Get metrics
        result = get_code_metrics(request.query, embedding_model, vector_store)
        
        summary_metrics = result.get("summary_metrics", {})
        issue_distribution = result.get("issue_distribution", {})
        
        return MetricsResponse(
            status="success",
            summary_metrics=SummaryMetrics(
                code_quality_score=summary_metrics.get("code_quality_score", 0),
                security_rating=summary_metrics.get("security_rating", 0),
                bug_density=summary_metrics.get("bug_density", 0),
                critical_issue_count=summary_metrics.get("critical_issue_count", 0)
            ),
            issue_distribution=IssueDistribution(
                security_vulnerabilities=issue_distribution.get("security_vulnerabilities", 0),
                code_smells=issue_distribution.get("code_smells", 0),
                best_practices=issue_distribution.get("best_practices", 0),
                performance_issues=issue_distribution.get("performance_issues", 0)
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating metrics: {str(e)}")
