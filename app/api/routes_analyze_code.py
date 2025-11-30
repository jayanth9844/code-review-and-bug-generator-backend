"""
Routes for code analysis endpoint.
Analyzes code snippets for potential issues using Gemini API.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services import analyze_code as analyze_code_service
from app.api.routes_code_input import get_stored_code

router = APIRouter()


class AnalyzeCodeRequest(BaseModel):
    """Request model for code analysis."""
    code: Optional[str] = Field(
        default=None,
        description="Code snippet to analyze. If not provided, uses stored code from /code-input"
    )
    api_key: Optional[str] = Field(
        default=None,
        description="Gemini API key. If not provided, uses API_KEY from environment variables.",
        examples=[None]
    )


class IssueDetail(BaseModel):
    """Model for individual code issue."""
    title: str
    type: str
    severity: str
    lineNumber: Optional[int] = None
    description: str
    suggestedFix: str


class AnalyzeCodeResponse(BaseModel):
    """Response model for code analysis."""
    status: str
    issues: List[IssueDetail] = []
    total_issues: int
    error_message: Optional[str] = None


@router.post(
    "/analyze-code",
    response_model=AnalyzeCodeResponse,
    summary="Analyze Code for Issues",
    description="Analyze code snippets for potential bugs, security risks, and best practices.",
)
def analyze_code_endpoint(request: AnalyzeCodeRequest):
    """
    Analyze code for potential issues.
    
    - **code**: Optional code snippet. If not provided, analyzes code from /code-input endpoint
    - **api_key**: Optional Gemini API key. If not provided, uses API_KEY from environment variables
    """
    try:
        # Get code to analyze
        code_to_analyze = request.code if request.code else get_stored_code()
        
        if not code_to_analyze:
            return AnalyzeCodeResponse(
                status="error",
                issues=[],
                total_issues=0,
                error_message="No code provided. Please provide code in request or load code using /code-input endpoint"  
            )
        
        # Analyze code
        result = analyze_code_service(code_to_analyze, api_key=request.api_key)
        
        if not isinstance(result, dict):
            return AnalyzeCodeResponse(
                status="error",
                issues=[],
                total_issues=0,
                error_message="Unexpected response format from AI service"
            )
        
        issues = result.get("issues", [])
        
        # Convert to response format
        formatted_issues = []
        for issue in issues:
            try:
                formatted_issues.append(IssueDetail(
                    title=issue.get("title", ""),
                    type=issue.get("type", ""),
                    severity=issue.get("severity", ""),
                    lineNumber=issue.get("lineNumber"),
                    description=issue.get("description", ""),
                    suggestedFix=issue.get("suggestedFix", "")
                ))
            except Exception:
                # Skip malformed issues
                pass
        
        return AnalyzeCodeResponse(
            status="success",
            issues=formatted_issues,
            total_issues=len(formatted_issues)
        )
    except ValueError as e:
        # API key validation or other ValueError
        error_msg = str(e)
        print(f"API Key/Validation Error: {error_msg}")
        return AnalyzeCodeResponse(
            status="error",
            issues=[],
            total_issues=0,
            error_message=error_msg
        )
    except Exception as e:
        import traceback
        error_msg = f"Error analyzing code: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return AnalyzeCodeResponse(
            status="error",
            issues=[],
            total_issues=0,
            error_message=error_msg
        )
