"""
Code Analysis Services - Direct Gemini API implementation without RAG.
Functions for analyzing code, calculating metrics, and injecting bugs.
Exact logic from code_review.ipynb notebook.
"""

import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load API key from environment
load_dotenv()
DEFAULT_API_KEY = os.getenv("API_KEY")

def get_api_key(user_api_key: str = None) -> str:
    """
    Get API key from user input or fall back to environment variable.
    
    Args:
        user_api_key (str, optional): API key provided by user
        
    Returns:
        str: API key to use
        
    Raises:
        ValueError: If neither user_api_key nor DEFAULT_API_KEY is available
    """
    # Handle empty strings and Swagger UI placeholder values as None
    if user_api_key:
        cleaned = user_api_key.strip() if isinstance(user_api_key, str) else str(user_api_key)
        # Ignore Swagger UI placeholder values
        if cleaned.lower() not in ["string", "none", "null", ""]:
            return cleaned
    
    # Fall back to environment variable
    if DEFAULT_API_KEY and DEFAULT_API_KEY.strip():
        return DEFAULT_API_KEY.strip()
    
    # No valid API key found
    raise ValueError("API_KEY is required. Provide it in the request or set API_KEY environment variable.")


def analyze_code(code_snippet: str, api_key: str = None):
  """
  Analyzes a given code snippet using the Gemini API via LangChain and returns structured analysis results.

  Args:
    code_snippet (str): The code to be analyzed.
    api_key (str, optional): Gemini API key. If not provided, uses API_KEY from environment.

  Returns:
    dict: A dictionary containing the analysis results with 'issues' key.
  """
  key = get_api_key(api_key)
  genai.configure(api_key=key)
  llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=key)

  prompt_template = ChatPromptTemplate.from_messages([
      ("system", "You are a helpful assistant that analyzes code for potential issues and returns the analysis in a structured JSON format."),
      ("human", "Analyze the following code snippet for potential issues. \nProvide the analysis in a structured JSON format, including 'title', 'type', 'severity' (e.g., 'Low', 'Medium', 'High', 'Critical'), 'lineNumber', 'description', and 'suggestedFix' for each issue found.\n\nCode:\n```python\n{code_snippet}\n```\n\nExample JSON format for issues:\n{{\"issues\": [{{\"title\": \"Issue Title\", \"type\": \"Bug\", \"severity\": \"High\", \"lineNumber\": 10, \"description\": \"Detailed description of the issue.\", \"suggestedFix\": \"Recommended fix for the issue.\"}}]}}")
  ])

  output_parser = StrOutputParser()

  chain = prompt_template | llm | output_parser

  response = chain.invoke({"code_snippet": code_snippet})

  # Remove markdown code block if present in the response
  if response.startswith('```json') and response.endswith('```'):
    response = response.replace('```json\n', '', 1)
    response = response.replace('\n```', '', 1)

  try:
    parsed_response = json.loads(response)
    return parsed_response
  except json.JSONDecodeError:
    print(f"Error: Invalid JSON string received from model: {response}")
    return {
        "issues": []
    }


def get_code_metrics(code_snippet: str, api_key: str = None) -> dict:
  """
  Calculates summary metrics and issue distribution by directly querying the Gemini API.

  Args:
    code_snippet (str): The code to be analyzed for metrics.
    api_key (str, optional): Gemini API key. If not provided, uses API_KEY from environment.

  Returns:
    dict: A dictionary containing 'summary_metrics' and 'issue_distribution' from Gemini.
  """
  key = get_api_key(api_key)
  genai.configure(api_key=key)
  llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=key)

  prompt_template = ChatPromptTemplate.from_messages([
      ("system", "You are a helpful assistant that analyzes code and provides summary metrics and issue distribution in a structured JSON format."),
      ("human", """Analyze the following code snippet and provide the analysis in a structured JSON format. I need two main sections: 'summary_metrics' and 'issue_distribution'.\n\nFor 'summary_metrics', include:\n- 'code_quality_score' (an integer from 0-100 where higher is better)\n- 'security_rating' (an integer from 0-100 where higher is better)\n- 'bug_density' (count of bugs/runtime errors)\n- 'critical_issue_count' (count of critical severity issues)\n\nFor 'issue_distribution', include:\n- 'security_vulnerabilities' (count of security/vulnerability issues)\n- 'code_smells' (count of code smell issues)\n- 'best_practices' (count of best practice violations, if any)\n- 'performance_issues' (count of performance-related issues, if any)\n
Ensure the output is a single JSON object. Here's an example of the desired JSON format:\n```json\n{{\n  "summary_metrics": {{\n    "code_quality_score": 85,\n    "security_rating": 90,\n    "bug_density": 1,\n    "critical_issue_count": 0\n  }},\n  "issue_distribution": {{\n    "security_vulnerabilities": 0,\n    "code_smells": 2,\n    "best_practices": 1,\n    "performance_issues": 0\n  }}\n}}\n```\n
Code:\n```python\n{code_snippet}\n```""")
  ])

  output_parser = StrOutputParser()

  chain = prompt_template | llm | output_parser

  response = chain.invoke({"code_snippet": code_snippet})

  # Remove markdown code block if present in the response
  if response.startswith('```json') and response.endswith('```'):
    response = response.replace('```json\n', '', 1)
    response = response.replace('\n```', '', 1)

  try:
    parsed_response = json.loads(response)
    return parsed_response
  except json.JSONDecodeError:
    print(f"Error: Invalid JSON string received from model: {response}")
    return {
        "summary_metrics": {},
        "issue_distribution": {}
    }


def inject_bugs(code_snippet: str, bug_type: str, severity_level: int, num_bugs: int, api_key: str = None) -> dict:
  """
  Injects specified types and number of bugs into a given code snippet using the Gemini API.

  Args:
    code_snippet (str): The original code snippet where bugs will be injected.
    bug_type (str): The type of bug to inject (e.g., 'SQL Injection', 'Division by Zero').
    severity_level (int): The severity level of the bugs (e.g., 1 for low, 5 for critical).
    num_bugs (int): The number of bugs to inject.
    api_key (str, optional): Gemini API key. If not provided, uses API_KEY from environment.

  Returns:
    dict: A dictionary containing the modified code with injected bugs and details
          about the injected bugs (e.g., their locations, types, and severities).
  """
  key = get_api_key(api_key)
  genai.configure(api_key=key)
  llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=key)

  prompt_template = ChatPromptTemplate.from_messages([
      ("system", "You are a helpful assistant that injects bugs into code based on given parameters and returns the modified code and bug details in JSON format."),
      ("human", """Inject {num_bugs} bugs of type '{bug_type}' with severity level {severity_level} into the following Python code snippet.\nProvide the output in a structured JSON format with two keys: 'buggy_code' (containing the full modified code) and 'bugs_injected' (an array of objects, where each object describes an injected bug with 'type', 'line_number', and 'description').\n\nCode:\n```python\n{code_snippet}\n```\n\nExample JSON format:\n{{\n  "buggy_code": "def example_function():\n    # Some example code without further template variables\n    return 0",\n  "bugs_injected": [\n    {{\n      "type": "{bug_type}", "line_number": 2, "description": "Description of the injected bug."\n    }}\n  ]\n}}\n""")
  ])

  output_parser = StrOutputParser()

  chain = prompt_template | llm | output_parser

  response = chain.invoke({
      "code_snippet": code_snippet,
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
  except json.JSONDecodeError:
    print(f"Error: Invalid JSON string received from model: {response}")
    return {
        "buggy_code": code_snippet, # Return original code on error
        "bugs_injected": []
    }
