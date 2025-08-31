from pydantic import BaseModel, Field
from typing import Literal, Optional


class UserIntent(BaseModel):
    """Schema for capturing user intent classification with enhanced structured output."""
    
    intent_type: Literal["qa", "summarization", "calculation"]
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    reasoning: str
    keywords_found: list[str] = Field(default_factory=list, description="Keywords that influenced the classification")
    context_influence: Optional[str] = Field(None, description="How conversation context affected classification")
