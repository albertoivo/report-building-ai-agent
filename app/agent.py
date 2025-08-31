"""Integrated agent that combines all components."""

from datetime import datetime
from .schemas import AnswerResponse
from .workflow import create_workflow, AgentState
from .prompts import intent_classification_prompt, SimpleLLMSimulator
from .tools import calculate
from .logging import SimpleLogger


class IntegratedAgent:
    """Simple integrated agent combining all components."""
    
    def __init__(self):
        self.llm = SimpleLLMSimulator()
        self.logger = SimpleLogger()
        self.memory = []
        self.workflow = create_workflow()  # Create compiled LangGraph workflow
    
    def process_input(self, user_input: str) -> AnswerResponse:
        """Process user input through the LangGraph workflow."""
        # Start session
        session_id = self.logger.start_session(user_input)
        
        try:
            # Create initial state with existing memory
            initial_state = AgentState(
                user_input=user_input,
                intent=None,
                response=None,
                memory=self.memory.copy(),  # Pass existing memory to workflow
                current_step="start"
            )
            
            # Run the LangGraph workflow
            final_state = self.workflow.invoke(initial_state)
            
            # Extract response from final state
            if final_state["response"]:
                response = final_state["response"]
            else:
                # Fallback response if workflow didn't generate one
                response = AnswerResponse(
                    question=user_input,
                    answer="I'm sorry, I couldn't process your request.",
                    sources=["error_handler"],
                    confidence=0.0,
                    timestamp=datetime.now()
                )
            
            # Update memory with the interaction
            self.memory = final_state["memory"]  # Replace with updated memory from workflow
            
            # Log the session
            self.logger.end_session(response.answer)
            
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
