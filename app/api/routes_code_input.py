"""
Routes for code input endpoint.
Handles receiving code snippets for analysis.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()

# Global storage for code snippets
_code_storage: List[str] = []


class CodeInputRequest(BaseModel):
    """Request model for loading code snippets."""
    code_snippets: List[str] = Field(
        ..., 
        description="List of code snippets to load",
        min_items=1,
    )


class CodeInputResponse(BaseModel):
    """Response model for code input endpoint."""
    status: str
    message: str
    snippets_loaded: int


@router.post(
    "/code-input",
    response_model=CodeInputResponse,
    summary="Load Code Snippets",
    description="Load code snippets for analysis.",
)
def code_input_endpoint(request: CodeInputRequest):
    """
    Load and store code snippets for analysis.
    
    - **code_snippets**: List of Python code snippets (required)
    """
    global _code_storage
    
    try:
        # Store the code snippets
        _code_storage.extend(request.code_snippets)
        
        return CodeInputResponse(
            status="success",
            message=f"Loaded {len(request.code_snippets)} code snippet(s) into memory",
            snippets_loaded=len(request.code_snippets)
        )
    except Exception as e:
        return CodeInputResponse(
            status="error",
            message=f"Error loading code: {str(e)}",
            snippets_loaded=0
        )


def get_stored_code() -> str:
    """Get all stored code snippets joined together."""
    global _code_storage
    return "\n\n---SNIPPET SEPARATOR---\n\n".join(_code_storage) if _code_storage else ""


def clear_stored_code():
    """Clear stored code snippets."""
    global _code_storage
    _code_storage = []
