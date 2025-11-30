"""
Routes for code metrics endpoint.
Calculates code quality metrics and issue distribution using Gemini API.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from app.services import get_code_metrics as get_code_metrics_service
from app.api.routes_code_input import get_stored_code

router = APIRouter()


class MetricsRequest(BaseModel):
    """Request model for code metrics."""
    code: Optional[str] = Field(
        default=None,
        description="Code snippet to analyze. If not provided, uses stored code from /code-input"
    )
    api_key: Optional[str] = Field(
        default=None,
        description="Gemini API key. If not provided, uses API_KEY from environment variables.",
        examples=[None]
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
    error_message: Optional[str] = None


@router.post(
    "/code-metrics",
    response_model=MetricsResponse,
    summary="Calculate Code Metrics",
    description="Calculate code quality metrics and issue distribution for code.",
)
def code_metrics_endpoint(request: MetricsRequest):
    """
    Get code quality metrics and issue distribution.
    
    - **code**: Optional code snippet. If not provided, analyzes code from /code-input endpoint
    - **api_key**: Optional Gemini API key. If not provided, uses API_KEY from environment variables
    """
    try:
        # Get code to analyze
        code_to_analyze = request.code if request.code else get_stored_code()
        
        if not code_to_analyze:
            return MetricsResponse(
                status="error",
                summary_metrics=SummaryMetrics(
                    code_quality_score=0,
                    security_rating=0,
                    bug_density=0,
                    critical_issue_count=0
                ),
                issue_distribution=IssueDistribution(
                    security_vulnerabilities=0,
                    code_smells=0,
                    best_practices=0,
                    performance_issues=0
                ),
                error_message="No code provided. Please provide code in request or load code using /code-input endpoint"
            )
        
        # Get metrics
        result = get_code_metrics_service(code_to_analyze, api_key=request.api_key)
        
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
    except ValueError as e:
        # API key validation or other ValueError
        error_msg = str(e)
        print(f"API Key/Validation Error: {error_msg}")
        return MetricsResponse(
            status="error",
            summary_metrics=SummaryMetrics(
                code_quality_score=0,
                security_rating=0,
                bug_density=0,
                critical_issue_count=0
            ),
            issue_distribution=IssueDistribution(
                security_vulnerabilities=0,
                code_smells=0,
                best_practices=0,
                performance_issues=0
            ),
            error_message=error_msg
        )
    except Exception as e:
        import traceback
        error_msg = f"Error getting code metrics: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return MetricsResponse(
            status="error",
            summary_metrics=SummaryMetrics(
                code_quality_score=0,
                security_rating=0,
                bug_density=0,
                critical_issue_count=0
            ),
            issue_distribution=IssueDistribution(
                security_vulnerabilities=0,
                code_smells=0,
                best_practices=0,
                performance_issues=0
            ),
            error_message=error_msg
        )
