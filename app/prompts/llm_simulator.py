"""Simple LLM simulator for testing prompts."""

from ..schemas import UserIntent


class SimpleLLMSimulator:
    """Simple LLM simulator for testing purposes."""
    
    def chat(self, messages: list) -> str:
        """Simulate LLM chat response."""
        user_message = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        system_message = ""
        for msg in messages:
            if msg.get("role") == "system":
                system_message = msg.get("content", "")
                break
        
        # Simple response based on system prompt type
        if "question-answering" in system_message:
            return f"Q&A Response: {user_message}"
        elif "summarization" in system_message:
            return f"Summary: {user_message[:50]}..."
        elif "calculation" in system_message:
            return f"Calculation: Processing {user_message}"
        else:
            return f"General response to: {user_message}"
    
    def classify_intent(self, prompt_text: str) -> UserIntent:
        """Simulate intent classification."""
        user_input = ""
        
        # Extract user input from prompt
        if "User Input:" in prompt_text:
            lines = prompt_text.split("\n")
            for line in lines:
                if line.strip().startswith("User Input:"):
                    user_input = line.replace("User Input:", "").strip()
                    break
        
        # Simple keyword-based classification (same as workflow nodes)
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ["what", "how", "why", "who", "when", "where"]):
            intent_type = "qa"
            confidence = 0.8
            reasoning = "Detected question words indicating Q&A intent"
        elif any(word in user_input_lower for word in ["summarize", "summary", "brief", "overview"]):
            intent_type = "summarization"
            confidence = 0.9
            reasoning = "Detected summarization keywords"
        elif any(word in user_input_lower for word in ["calculate", "compute", "math", "+", "-", "*", "/"]):
            intent_type = "calculation"
            confidence = 0.85
            reasoning = "Detected calculation keywords or operators"
        else:
            intent_type = "qa"
            confidence = 0.6
            reasoning = "Default to Q&A for unclear intent"
        
        return UserIntent(
            intent_type=intent_type,
            confidence=confidence,
            reasoning=reasoning
        )
