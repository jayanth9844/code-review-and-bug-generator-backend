"""
RAG (Retrieval-Augmented Generation) Module for Code Analysis and Bug Injection.
"""

from .vector_store import initialize_vector_store_and_embeddings, load_and_index_code
from .analyze_code import analyze_code
from .get_code_metrics import get_code_metrics
from .inject_bugs import inject_bugs

__all__ = [
    "initialize_vector_store_and_embeddings",
    "load_and_index_code",
    "analyze_code",
    "get_code_metrics",
    "inject_bugs",
]
