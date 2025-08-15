"""Integrated agent that combines all components."""

from datetime import datetime
from .schemas import AnswerResponse
from .prompts import intent_classification_prompt, SimpleLLMSimulator
from .tools import calculate
from .logging import SimpleLogger


class IntegratedAgent:
    """Simple integrated agent combining all components."""
    
    def __init__(self):
        self.llm = SimpleLLMSimulator()
        self.logger = SimpleLogger()
        self.memory = []
    
    def process_input(self, user_input: str) -> AnswerResponse:
        """Process user input through the complete pipeline."""
        # Start session
        self.logger.start_session(user_input)
        
        try:
            # Step 1: Classify intent
            conversation_history = str(self.memory[-3:])  # Last 3 interactions
            classification_prompt = intent_classification_prompt.format(
                user_input=user_input,
                conversation_history=conversation_history
            )
            
            intent = self.llm.classify_intent(classification_prompt)
            self.logger.log_tool_call("classify_intent", {"user_input": user_input}, str(intent.intent_type))
            
            # Step 2: Generate response based on intent
            response_text = ""
            sources = []
            confidence = intent.confidence
            
            if intent.intent_type == "qa":
                response_text = self._handle_qa(user_input)
                sources = ["knowledge_base"]
                
            elif intent.intent_type == "summarization":
                response_text = self._handle_summarization(user_input)
                sources = ["document_processor"]
                
            elif intent.intent_type == "calculation":
                response_text = self._handle_calculation(user_input)
                sources = ["calculator_tool"]
                
            else:
                response_text = "I'm not sure how to help with that."
                sources = ["default"]
                confidence = 0.3
            
            # Step 3: Create response
            response = AnswerResponse(
                question=user_input,
                answer=response_text,
                sources=sources,
                confidence=confidence,
                timestamp=datetime.now()
            )
            
            # Step 4: Update memory
            self.memory.append({
                "user_input": user_input,
                "intent": intent.intent_type,
                "response": response_text,
                "timestamp": datetime.now().isoformat()
            })
            
            # End session
            self.logger.end_session(response_text)
            
            return response
            
        except Exception as e:
            # Error handling
            error_response = AnswerResponse(
                question=user_input,
                answer=f"Error processing request: {str(e)}",
                sources=["error_handler"],
                confidence=0.0,
                timestamp=datetime.now()
            )
            self.logger.end_session(f"Error: {str(e)}")
            return error_response
    
    def _handle_qa(self, user_input: str) -> str:
        """Handle question-answering requests."""
        # Simulate Q&A processing
        if "capital of france" in user_input.lower():
            return "Paris"
        elif "what did i just ask" in user_input.lower():
            if self.memory:
                last_question = self.memory[-1].get("user_input", "")
                return f"You asked: {last_question}"
            else:
                return "I don't have any previous questions in memory."
        else:
            return f"This is a Q&A response to: {user_input}"
    
    def _handle_summarization(self, user_input: str) -> str:
        """Handle summarization requests."""
        # Log tool usage
        self.logger.log_tool_call("summarization_tool", {"text": user_input}, "summary_generated")
        return f"Summary: {user_input[:50]}... [This is a summarized version]"
    
    def _handle_calculation(self, user_input: str) -> str:
        """Handle calculation requests."""
        # Use the calculator tool
        result = calculate(user_input)
        self.logger.log_tool_call("calculator_tool", {"expression": user_input}, result)
        return result
    
    def get_memory(self) -> list:
        """Get conversation memory."""
        return self.memory
