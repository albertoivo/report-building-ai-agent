from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class AnswerResponse(BaseModel):
    """Schema for agent responses to user questions."""
    
    question: str
    answer: str
    sources: List[str]
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    timestamp: datetime = Field(default_factory=datetime.now)
