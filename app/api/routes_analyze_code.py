"""
Routes for code analysis endpoint.
Analyzes code snippets for potential issues using RAG and Gemini API.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.core.dependencies import get_current_user, get_api_key
from app.RAG import analyze_code, initialize_vector_store_and_embeddings

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


class AnalyzeCodeRequest(BaseModel):
    """Request model for code analysis."""
    query: Optional[str] = Field(
        default="Analyze the code for potential bugs, security risks, performance issues, and best-practice violations.",
        description="Natural language query describing the code analysis needed"
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


@router.post(
    "/analyze-code",
    response_model=AnalyzeCodeResponse,
    summary="Analyze Code for Issues",
    description="Analyze loaded code snippets for potential bugs, security risks, and best practices.",
)
def analyze_code_endpoint(
    request: AnalyzeCodeRequest,
    user=Depends(get_current_user),
    _=Depends(get_api_key)
):
    """
    Analyze code for potential issues.
    
    - **query**: Natural language description of analysis (optional, uses default if not provided)
    
    Default Query: "Analyze the code for potential bugs, security risks, performance issues, and best-practice violations."
    """
    try:
        embedding_model, vector_store = get_vector_store_and_embeddings()
        
        # Analyze code
        result = analyze_code(request.query, embedding_model, vector_store)
        
        issues = result.get("issues", [])
        
        return AnalyzeCodeResponse(
            status="success",
            issues=issues,
            total_issues=len(issues)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing code: {str(e)}")
