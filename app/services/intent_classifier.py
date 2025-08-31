import re
from ..schemas import UserIntent
from ..prompts import intent_classification_prompt
from ..prompts.llm_gpt import OpenAIChatLLM


class IntentClassifier:
    """OpenAI-powered intent classification."""
    
    def __init__(self, llm=None):
        self.llm = llm or OpenAIChatLLM()
        self.intent_mapping = {
            "CALCULATION": "calculation",
            "SUMMARIZATION": "summarization", 
            "QA": "qa"
        }
    
    def classify_intent(self, user_input: str, conversation_history: str = "") -> UserIntent:
        """Classify user intent using OpenAI."""
        prompt_text = intent_classification_prompt.format(
            user_input=user_input,
            conversation_history=conversation_history or "No previous conversation."
        )
        
        llm_response = self.llm.generate(prompt_text)
        return self._parse_response(llm_response)
    
    def _parse_response(self, response: str) -> UserIntent:
        """Parse OpenAI response into UserIntent."""
        # Extract intent
        intent_match = re.search(r'Intent:\s*([A-Z]+)', response, re.IGNORECASE)
        intent = self.intent_mapping.get(
            intent_match.group(1).upper() if intent_match else "QA", 
            "qa"
        )
        
        # Extract confidence
        confidence_match = re.search(r'Confidence:\s*([0-9.]+)', response)
        confidence = float(confidence_match.group(1)) if confidence_match else 0.6
        confidence = max(0.0, min(1.0, confidence))
        
        # Extract reasoning
        reasoning_match = re.search(r'Reasoning:\s*(.+?)(?=\n[A-Z]|$)', response, re.DOTALL)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else "OpenAI classification"
        
        # Extract keywords
        keywords_match = re.search(r'Keywords_Found:\s*\[([^\]]*)\]', response)
        keywords_text = keywords_match.group(1) if keywords_match else ""
        keywords_found = [k.strip().strip('"\'') for k in keywords_text.split(',') if k.strip()]
        
        return UserIntent(
            intent_type=intent,
            confidence=confidence,
            reasoning=reasoning,
            keywords_found=keywords_found
        )
