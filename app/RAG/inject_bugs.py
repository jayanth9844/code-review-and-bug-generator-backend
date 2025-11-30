"""
Bug Injection module using RAG and Gemini API.
Injects bugs into code snippets for testing and training purposes.
"""

import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .config import API_KEY


def inject_bugs(
    query: str,
    embedding_model,
    vector_store,
    bug_type: str,
    severity_level: int,
    num_bugs: int
) -> dict:
    """
    Injects specified types and number of bugs into a given code snippet, 
    retrieved via RAG, using the Gemini API.

    Args:
        query (str): The natural language query describing the code context for bug injection.
        embedding_model: The SentenceTransformerEmbeddings model to embed the query.
        vector_store: The Chroma vector store instance to retrieve relevant code snippets.
        bug_type (str): The type of bug to inject (e.g., 'SQL Injection', 'Division by Zero').
        severity_level (int): The severity level of the bugs (e.g., 1 for low, 5 for critical).
        num_bugs (int): The number of bugs to inject.

    Returns:
        dict: A dictionary containing the modified code with injected bugs and details
              about the injected bugs (e.g., their locations, types, and severities).
              
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
    # This combined code will be what Gemini injects bugs into.
    combined_code_for_injection = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that injects bugs into code based on given parameters and returns the modified code and bug details in JSON format."),
        ("human", """Inject {num_bugs} bugs of type '{bug_type}' with severity level {severity_level} into the following Python code snippet.
Provide the output in a structured JSON format with two keys: 'buggy_code' (containing the full modified code) and 'bugs_injected' (an array of objects, where each object describes an injected bug with 'type', 'line_number', and 'description').

Code:
```python
{code_snippet}
```

Example JSON format:
{{
  "buggy_code": "def example_function():\n    # Some example code without further template variables\n    return 0",
  "bugs_injected": [
    {{
      "type": "{bug_type}", "line_number": 2, "description": "Description of the injected bug."
    }}
  ]
}}
""")
    ])

    output_parser = StrOutputParser()

    chain = prompt_template | llm | output_parser

    response = chain.invoke({
        "code_snippet": combined_code_for_injection,
        "num_bugs": num_bugs,
        "bug_type": bug_type,
        "severity_level": severity_level
    })

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
            "buggy_code": combined_code_for_injection,
            "bugs_injected": []
        }
