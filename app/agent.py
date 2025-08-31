"""Integrated agent that combines all components."""

from datetime import datetime
from .schemas import AnswerResponse
from .workflow import create_workflow, AgentState
from .prompts import OpenAIChatLLM
from .logging import SimpleLogger


class IntegratedAgent:
    """Simple integrated agent combining all components."""

    def __init__(self):
        # Use OpenAI GPT - requires OPENAI_API_KEY environment variable
        self.llm = OpenAIChatLLM()
        self.workflow = create_workflow()
        self.logger = SimpleLogger()
        self.memory = []
        self.conversation_messages = []  # Store messages across interactions

    def process_input(self, user_input: str) -> AnswerResponse:
        """Process user input through the LangGraph workflow."""
        # Start session
        self.logger.start_session(user_input)

        try:
            # Create initial state with existing memory and messages
            initial_state = AgentState(
                user_input=user_input,
                intent=None,
                response=None,
                memory=self.memory.copy(),
                current_step="start",
                messages=self.conversation_messages.copy(),  # Use existing messages
                logger=self.logger
            )

            # Run the LangGraph workflow
            final_state = self.workflow.invoke(initial_state)

            # Extract response and update memory
            if final_state["response"]:
                response = final_state["response"]
            else:
                response = AnswerResponse(
                    question=user_input,
                    answer="I'm sorry, I couldn't process your request.",
                    sources=["error_handler"],
                    confidence=0.0,
                    timestamp=datetime.now(),
                )

            # Update memory and store messages for next conversation
            self.memory = final_state["memory"]
            self.conversation_messages = final_state.get("messages", [])

            # Log the session
            self.logger.end_session(response.answer)

            return response

        except Exception as e:
            error_response = AnswerResponse(
                question=user_input,
                answer=f"Error processing request: {str(e)}",
                sources=["error_handler"],
                confidence=0.0,
                timestamp=datetime.now(),
            )

            self.logger.end_session(error_response.answer)
            return error_response

    def get_memory(self) -> list:
        """Get current conversation memory."""
        return self.memory
