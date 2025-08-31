"""Intent classification service using LLM with sophisticated language understanding."""

import re
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from ..schemas import UserIntent
from ..prompts import intent_classification_prompt
from ..prompts.llm_simulator import SimpleLLMSimulator


class IntentClassificationResult(BaseModel):
    """Structured output from intent classification."""
    
    intent: str = Field(..., description="The classified intent type")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    reasoning: str = Field(..., description="Detailed reasoning for classification")
    keywords_found: list[str] = Field(default_factory=list, description="Keywords that influenced decision")
    context_influence: Optional[str] = Field(None, description="How conversation context affected classification")


class IntentClassifier:
    """Advanced intent classification using LLM with structured output parsing."""
    
    def __init__(self, llm=None):
        self.llm = llm or SimpleLLMSimulator()
        self.intent_mapping = {
            "CALCULATION": "calculation",
            "SUMMARIZATION": "summarization", 
            "QA": "qa"
        }
    
    def classify_intent(self, user_input: str, conversation_history: str = "") -> UserIntent:
        """
        Classify user intent with sophisticated language understanding.
        
        Args:
            user_input: The user's input text
            conversation_history: Previous conversation context
            
        Returns:
            UserIntent with classification results
        """
        # Format the enhanced prompt
        prompt_text = intent_classification_prompt.format(
            user_input=user_input,
            conversation_history=conversation_history or "No previous conversation."
        )
        
        # Get LLM response
        llm_response = self.llm.generate(prompt_text)
        
        # Parse structured output
        result = self._parse_classification_response(llm_response)
        
        # Convert to UserIntent schema
        return UserIntent(
            intent_type=result.intent,
            confidence=result.confidence,
            reasoning=result.reasoning,
            keywords_found=result.keywords_found,
            context_influence=result.context_influence
        )
    
    def _parse_classification_response(self, response: str) -> IntentClassificationResult:
        """Parse LLM response into structured format."""
        
        # Extract intent
        intent_match = re.search(r'Intent:\s*([A-Z]+)', response, re.IGNORECASE)
        raw_intent = intent_match.group(1).upper() if intent_match else "QA"
        intent = self.intent_mapping.get(raw_intent, "qa")
        
        # Extract confidence
        confidence_match = re.search(r'Confidence:\s*([0-9.]+)', response)
        confidence = float(confidence_match.group(1)) if confidence_match else 0.5
        confidence = max(0.0, min(1.0, confidence))  # Clamp to valid range
        
        # Extract reasoning
        reasoning_match = re.search(r'Reasoning:\s*(.+?)(?=\n[A-Z][a-z_]*:|$)', response, re.DOTALL)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else "Default classification based on input analysis."
        
        # Extract keywords found
        keywords_match = re.search(r'Keywords_Found:\s*\[([^\]]*)\]', response)
        keywords_text = keywords_match.group(1) if keywords_match else ""
        keywords_found = [k.strip().strip('"\'') for k in keywords_text.split(',') if k.strip()]
        
        # Extract context influence
        context_match = re.search(r'Context_Influence:\s*(.+?)(?=\n[A-Z][a-z_]*:|$)', response, re.DOTALL)
        context_influence = context_match.group(1).strip() if context_match else None
        
        return IntentClassificationResult(
            intent=intent,
            confidence=confidence,
            reasoning=reasoning,
            keywords_found=keywords_found,
            context_influence=context_influence
        )
    
    def classify_with_fallback(self, user_input: str, conversation_history: str = "") -> UserIntent:
        """
        Classify intent with keyword-based fallback for reliability.
        
        Args:
            user_input: The user's input text
            conversation_history: Previous conversation context
            
        Returns:
            UserIntent with classification results
        """
        try:
            # Try LLM-based classification first
            result = self.classify_intent(user_input, conversation_history)
            
            # If confidence is very low, use keyword fallback
            if result.confidence < 0.3:
                fallback_result = self._keyword_based_fallback(user_input)
                if fallback_result.confidence > result.confidence:
                    return fallback_result
            
            return result
            
        except Exception as e:
            # Fallback to keyword-based classification on error
            return self._keyword_based_fallback(user_input)
    
    def _keyword_based_fallback(self, user_input: str) -> UserIntent:
        """Simple keyword-based fallback classification."""
        user_input_lower = user_input.lower()
        
        # Calculation keywords and patterns
        calc_keywords = ['calculate', 'compute', '+', '-', '*', '/', '=', 'solve', 'math', '%', 'times', 'plus', 'minus', 'divided', 'multiply']
        calc_patterns = [r'\d+\s*[+\-*/]\s*\d+', r'\bsolve\b', r'\btimes\b', r'\bplus\b', r'\bminus\b']
        
        calc_score = sum(1 for kw in calc_keywords if kw in user_input_lower)
        calc_score += sum(1 for pattern in calc_patterns if re.search(pattern, user_input_lower))
        
        # Summarization keywords  
        summ_keywords = ['summarize', 'summary', 'recap', 'overview', 'main points', 'key points', 'gist', 'brief']
        summ_patterns = [r'\bmain\s+points?\b', r'\bkey\s+points?\b', r'\bsummar[iy]', r'\brecap\b']
        
        summ_score = sum(1 for kw in summ_keywords if kw in user_input_lower)
        summ_score += sum(1 for pattern in summ_patterns if re.search(pattern, user_input_lower))
        
        # QA keywords
        qa_keywords = ['what', 'how', 'why', 'when', 'where', 'who', 'explain', 'tell me', 'define', 'describe']
        qa_score = sum(1 for kw in qa_keywords if kw in user_input_lower)
        
        # Determine intent based on scores with better logic
        if calc_score > 0 and calc_score >= max(summ_score, qa_score):
            return UserIntent(
                intent_type="calculation",
                confidence=min(0.8, 0.5 + calc_score * 0.1),
                reasoning="Keyword-based fallback classification detected calculation intent.",
                keywords_found=[kw for kw in calc_keywords if kw in user_input_lower]
            )
        elif summ_score > 0 and summ_score > qa_score:
            return UserIntent(
                intent_type="summarization", 
                confidence=min(0.8, 0.5 + summ_score * 0.1),
                reasoning="Keyword-based fallback classification detected summarization intent.",
                keywords_found=[kw for kw in summ_keywords if kw in user_input_lower]
            )
        else:
            return UserIntent(
                intent_type="qa",
                confidence=0.6,
                reasoning="Default QA classification via keyword-based fallback.",
                keywords_found=[kw for kw in qa_keywords if kw in user_input_lower]
            )
