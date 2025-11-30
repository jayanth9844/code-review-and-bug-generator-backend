from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Union
from app.core.dependencies import get_api_key,get_current_user
from app.services.model_service import predict_student_score, predict_batch_student_scores

router = APIRouter()


class Studentfeatures(BaseModel):
    comprehension: float
    attention:float
    focus:float
    retention:float
    engagement_time: int

class BatchRequest(BaseModel):
    students: List[Studentfeatures] = Field(..., max_items=200, min_items=1)
    
    @validator('students')
    def validate_batch_size(cls, v):
        if len(v) > 200:
            raise ValueError('Maximum 200 students allowed per batch')
        return v

@router.post("/predict")
def predict_score(
    request: Union[Studentfeatures, BatchRequest],
    user=Depends(get_current_user),
    _=Depends(get_api_key)
):
    # Handle single prediction (backward compatibility)
    if isinstance(request, Studentfeatures):
        prediction = predict_student_score(request.model_dump())
        return {"predicted_score": f'{prediction:.2f}'}
    
    # Handle batch prediction
    if isinstance(request, BatchRequest):
        if len(request.students) > 200:
            raise HTTPException(status_code=400, detail="Maximum 200 students allowed per batch")
        
        student_data = [student.model_dump() for student in request.students]
        predictions = predict_batch_student_scores(student_data)
        
        return {
            "batch_size": len(predictions),
            "predictions": [{"predicted_score": f'{pred:.2f}'} for pred in predictions]
        }