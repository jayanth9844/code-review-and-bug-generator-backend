"""
Code Analysis module using RAG and Gemini API.
Analyzes code snippets for potential issues.
"""

import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .config import API_KEY


def analyze_code(query: str, embedding_model, vector_store) -> dict:
    """
    Analyzes code using the Gemini API via LangChain, retrieving relevant snippets 
    from a vector store based on a query.

    Args:
        query (str): The natural language query describing the code analysis needed.
        embedding_model: The SentenceTransformerEmbeddings model to embed the query.
        vector_store: The Chroma vector store instance to retrieve relevant code snippets.

    Returns:
        dict: A dictionary containing the analysis results with 'issues' key.
        
    Raises:
        ValueError: If API_KEY is not configured.
    """
    if not API_KEY:
        raise ValueError("API_KEY is not configured. Please check your .env file.")

    # 1. Create an embedding for the query
    query_embedding = embedding_model.embed_query(query)

    # 2. Retrieve top N relevant code snippets from the vector store
    # We'll retrieve top 5 for a good balance of context and conciseness.
    relevant_docs = vector_store.similarity_search_by_vector(query_embedding, k=5)

    # 3. Concatenate the page_content of the retrieved documents
    # This combined code will be what Gemini analyzes.
    combined_code_for_analysis = "\n\n".join([doc.page_content for doc in relevant_docs])

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=API_KEY)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that analyzes code for potential issues and returns the analysis in a structured JSON format."),
        ("human", "Analyze the following code snippet for potential issues. \nProvide the analysis in a structured JSON format, including 'title', 'type', 'severity' (e.g., 'Low', 'Medium', 'High', 'Critical'), 'lineNumber', 'description', and 'suggestedFix' for each issue found.\n\nCode:\n```python\n{code_snippet}\n```\n\nExample JSON format for issues:\n{{\"issues\": [{{\"title\": \"Issue Title\", \"type\": \"Bug\", \"severity\": \"High\", \"lineNumber\": 10, \"description\": \"Detailed description of the issue.\", \"suggestedFix\": \"Recommended fix for the issue.\"}}]}}")
    ])

    output_parser = StrOutputParser()

    chain = prompt_template | llm | output_parser

    # Pass the combined code from RAG to the Gemini API
    response = chain.invoke({"code_snippet": combined_code_for_analysis})

    # Remove markdown code block if present in the response
    if response.startswith('```json') and response.endswith('```'):
        response = response.replace('```json\n', '', 1)
        response = response.replace('\n```', '', 1)

    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON string received from model: {response}")
        return {"issues": []}
