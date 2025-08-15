from pydantic import BaseModel, Field
from typing import Literal


class UserIntent(BaseModel):
    """Schema for capturing user intent classification."""
    
    intent_type: Literal["qa", "summarization", "calculation"]
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    reasoning: str
