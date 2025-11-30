"""
Routes for bug injection endpoint.
Injects bugs into code snippets for testing using RAG and Gemini API.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.core.dependencies import get_current_user, get_api_key
from app.RAG import inject_bugs, initialize_vector_store_and_embeddings

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


class InjectBugsRequest(BaseModel):
    """Request model for bug injection."""
    query: Optional[str] = Field(
        default="Inject bugs into the code and return details.",
        description="Natural language query describing the bug injection context"
    )
    bug_type: str = Field(
        default="Security Vulnerability",
        description="Type of bug to inject (e.g., 'SQL Injection', 'Division by Zero')",
    )
    severity_level: int = Field(
        default=5,
        description="Severity level of bugs (1=Low, 2=Medium, 3=High, 4=Critical, 5=Extreme)",
        ge=1,
        le=5,
    )
    num_bugs: int = Field(
        default=2,
        description="Number of bugs to inject",
        ge=1,
        le=10,
    )


class BugDetail(BaseModel):
    """Model for individual injected bug."""
    type: str
    line_number: int
    description: str


class InjectBugsResponse(BaseModel):
    """Response model for bug injection."""
    status: str
    buggy_code: str
    bugs_injected: List[BugDetail] = []
    total_bugs_injected: int


@router.post(
    "/inject-bugs",
    response_model=InjectBugsResponse,
    summary="Inject Bugs into Code",
    description="Inject specified bugs into code for testing and training purposes.",
)
def inject_bugs_endpoint(
    request: InjectBugsRequest,
    user=Depends(get_current_user),
    _=Depends(get_api_key)
):
    """
    Inject bugs into loaded code snippets.
    
    - **query**: Context for bug injection (optional, uses default if not provided)
    - **bug_type**: Type of bug to inject (default: "Security Vulnerability")
    - **severity_level**: 1-5 where 5 is most severe (default: 5)
    - **num_bugs**: Number of bugs to inject (default: 2)
    
    Default Query: "Inject bugs into the code and return details."
    """
    try:
        embedding_model, vector_store = get_vector_store_and_embeddings()
        
        # Inject bugs
        result = inject_bugs(
            query=request.query,
            embedding_model=embedding_model,
            vector_store=vector_store,
            bug_type=request.bug_type,
            severity_level=request.severity_level,
            num_bugs=request.num_bugs
        )
        
        buggy_code = result.get("buggy_code", "")
        bugs_injected = result.get("bugs_injected", [])
        
        return InjectBugsResponse(
            status="success",
            buggy_code=buggy_code,
            bugs_injected=bugs_injected,
            total_bugs_injected=len(bugs_injected)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error injecting bugs: {str(e)}")
