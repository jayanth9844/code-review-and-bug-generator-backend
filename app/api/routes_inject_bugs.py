"""
Routes for bug injection endpoint.
Injects bugs into code snippets for testing using Gemini API.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services import inject_bugs as inject_bugs_service
from app.api.routes_code_input import get_stored_code

router = APIRouter()


class InjectBugsRequest(BaseModel):
    """Request model for bug injection."""
    code: Optional[str] = Field(
        default=None,
        description="Code snippet for bug injection. If not provided, uses stored code from /code-input"
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
    api_key: Optional[str] = Field(
        default=None,
        description="Gemini API key. If not provided, uses API_KEY from environment variables.",
        examples=[None]
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
def inject_bugs_endpoint(request: InjectBugsRequest):
    """
    Inject bugs into code snippets.
    
    - **code**: Optional code snippet. If not provided, uses code from /code-input endpoint
    - **bug_type**: Type of bug to inject (default: "Security Vulnerability")
    - **severity_level**: 1-5 where 5 is most severe (default: 5)
    - **num_bugs**: Number of bugs to inject (default: 2)
    - **api_key**: Optional Gemini API key. If not provided, uses API_KEY from environment variables
    """
    try:
        # Get code to analyze
        code_to_analyze = request.code if request.code else get_stored_code()
        
        if not code_to_analyze:
            return InjectBugsResponse(
                status="error",
                buggy_code="",
                bugs_injected=[],
                total_bugs_injected=0
            )
        
        # Inject bugs
        result = inject_bugs_service(
            code_snippet=code_to_analyze,
            bug_type=request.bug_type,
            severity_level=request.severity_level,
            num_bugs=request.num_bugs,
            api_key=request.api_key
        )
        
        buggy_code = result.get("buggy_code", "")
        bugs_injected = result.get("bugs_injected", [])
        
        # Convert to response format
        formatted_bugs = []
        for bug in bugs_injected:
            try:
                formatted_bugs.append(BugDetail(
                    type=bug.get("type", ""),
                    line_number=bug.get("line_number", 0),
                    description=bug.get("description", "")
                ))
            except Exception:
                # Skip malformed bugs
                pass
        
        return InjectBugsResponse(
            status="success",
            buggy_code=buggy_code,
            bugs_injected=formatted_bugs,
            total_bugs_injected=len(formatted_bugs)
        )
    except ValueError as e:
        # API key validation error
        print(f"API Key Error: {str(e)}")
        return InjectBugsResponse(
            status="error",
            buggy_code="",
            bugs_injected=[],
            total_bugs_injected=0
        )
    except Exception as e:
        import traceback
        print(f"Error injecting bugs: {str(e)}")
        traceback.print_exc()
        return InjectBugsResponse(
            status="error",
            buggy_code="",
            bugs_injected=[],
            total_bugs_injected=0
        )
