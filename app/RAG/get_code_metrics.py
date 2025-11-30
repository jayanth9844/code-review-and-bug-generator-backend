"""
Code Metrics module using RAG and Gemini API.
Calculates code quality metrics and issue distribution.
"""

import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .config import API_KEY


def get_code_metrics(query: str, embedding_model, vector_store) -> dict:
    """
    Calculates summary metrics and issue distribution by directly querying the Gemini API,
    retrieving relevant snippets from a vector store based on a query.

    Args:
        query (str): The natural language query describing the code analysis needed.
        embedding_model: The SentenceTransformerEmbeddings model to embed the query.
        vector_store: The Chroma vector store instance to retrieve relevant code snippets.

    Returns:
        dict: A dictionary containing 'summary_metrics' and 'issue_distribution' from Gemini.
        
    Raises:
        ValueError: If API_KEY is not configured.
    """
    if not API_KEY:
        raise ValueError("API_KEY is not configured. Please check your .env file.")

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=API_KEY)

    # 1. Create an embedding for the query
    query_embedding = embedding_model.embed_query(query)

    # 2. Retrieve top N relevant code snippets from the vector store
    # We'll retrieve top 5 for a good balance of context and conciseness.
    relevant_docs = vector_store.similarity_search_by_vector(query_embedding, k=5)

    # 3. Concatenate the page_content of the retrieved documents
    # This combined code will be what Gemini analyzes.
    combined_code_for_metrics = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that analyzes code and provides summary metrics and issue distribution in a structured JSON format."),
        ("human", """Analyze the following code snippet and provide the analysis in a structured JSON format. I need two main sections: 'summary_metrics' and 'issue_distribution'.\n\nFor 'summary_metrics', include:\n- 'code_quality_score' (an integer from 0-100 where higher is better)\n- 'security_rating' (an integer from 0-100 where higher is better)\n- 'bug_density' (count of bugs/runtime errors)\n- 'critical_issue_count' (count of critical severity issues)\n\nFor 'issue_distribution', include:\n- 'security_vulnerabilities' (count of security/vulnerability issues)\n- 'code_smells' (count of code smell issues)\n- 'best_practices' (count of best practice violations, if any)\n- 'performance_issues' (count of performance-related issues, if any)\n\nEnsure the output is a single JSON object. Here's an example of the desired JSON format:\n```json\n{{\n  "summary_metrics": {{\n    "code_quality_score": 85,\n    "security_rating": 90,\n    "bug_density": 1,\n    "critical_issue_count": 0\n  }},\n  "issue_distribution": {{\n    "security_vulnerabilities": 0,\n    "code_smells": 2,\n    "best_practices": 1,\n    "performance_issues": 0\n  }}\n}}\n```\n\nCode:\n```python\n{code_snippet}\n```""")
    ])

    output_parser = StrOutputParser()

    chain = prompt_template | llm | output_parser

    response = chain.invoke({"code_snippet": combined_code_for_metrics})

    # Remove markdown code block if present in the response
    if response.startswith('```json') and response.endswith('```'):
        response = response.replace('```json\n', '', 1)
        response = response.replace('\n```', '', 1)

    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON string received from model: {response}")
        return {
            "summary_metrics": {},
            "issue_distribution": {}
        }
