"""
Routes for code input endpoint.
Handles loading and indexing code snippets into the vector store.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List
from app.core.dependencies import get_current_user, get_api_key
from app.RAG import load_and_index_code, initialize_vector_store_and_embeddings

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


class CodeInputRequest(BaseModel):
    """Request model for loading code snippets."""
    code_snippets: List[str] = Field(
        ..., 
        description="List of code snippets to load and index",
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
    summary="Load and Index Code Snippets",
    description="Load code snippets and index them in the vector store for RAG processing.",
)
def code_input_endpoint(
    request: CodeInputRequest,
    user=Depends(get_current_user),
    _=Depends(get_api_key)
):
    """
    Load code snippets and add them to the vector store.
    
    - **code_snippets**: List of Python code snippets (required)
    """
    try:
        embedding_model, vector_store = get_vector_store_and_embeddings()
        
        # Load and index the code snippets
        message = load_and_index_code(request.code_snippets, embedding_model, vector_store)
        
        return CodeInputResponse(
            status="success",
            message=message,
            snippets_loaded=len(request.code_snippets)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading code: {str(e)}")
