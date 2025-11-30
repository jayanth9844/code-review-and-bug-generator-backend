"""
Configuration module for RAG system.
Handles API key loading and Gemini API setup.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai


def load_api_key() -> str:
    """
    Load the API key from environment variables.
    
    Returns:
        str: The API key for Gemini API.
        
    Raises:
        RuntimeError: If API_KEY is not found in environment variables.
    """
    load_dotenv()
    
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY missing. Add API_KEY to your .env file.")
    
    # Strip accidental surrounding quotes
    if api_key.startswith('"') and api_key.endswith('"'):
        api_key = api_key[1:-1]
    if api_key.startswith("'") and api_key.endswith("'"):
        api_key = api_key[1:-1]
    
    return api_key


def configure_gemini(api_key: str) -> None:
    """
    Configure the Gemini API with the provided API key.
    
    Args:
        api_key (str): The API key for Gemini API.
    """
    genai.configure(api_key=api_key)


# Initialize API key on module load
try:
    API_KEY = load_api_key()
    configure_gemini(API_KEY)
except RuntimeError as e:
    print(f"Warning: {e}")
    API_KEY = None
