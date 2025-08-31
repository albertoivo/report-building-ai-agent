"""LangChain-based prompt templates for the agent."""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts.prompt import PromptTemplate as LangChainPromptTemplate


class PromptTemplate:
    """Simple prompt template class for backward compatibility."""
    
    def __init__(self, input_variables: list, template: str):
        self.input_variables = input_variables
        self.template = template
    
    def format(self, **kwargs) -> str:
        """Format the template with provided variables."""
        return self.template.format(**kwargs)


# Intent Classification Prompt
intent_classification_prompt = PromptTemplate(
    input_variables=["user_input", "conversation_history"],
    template="""
You are an intelligent assistant. Classify the user's intent based on the input below:

User Input: {user_input}
Conversation History: {conversation_history}

Possible intents: "qa", "summarization", "calculation".

Please provide the intent type, confidence score (0-1), and reasoning for your classification.

Response format:
Intent: [intent_type]
Confidence: [score]
Reasoning: [explanation]
"""
)


# System Prompts for different intents
QA_SYSTEM_PROMPT = """You are a helpful question-answering assistant. 
Answer user questions clearly and concisely based on the conversation history.
Provide accurate information and cite sources when possible.
Use the conversation context to provide more relevant and personalized responses."""

SUMMARIZATION_SYSTEM_PROMPT = """You are a text summarization assistant.
Create concise and informative summaries of the provided text or conversation.
Focus on key points and main ideas from the entire conversation context.
Consider the conversation history to provide better context for summaries."""

CALCULATION_SYSTEM_PROMPT = """You are a mathematical calculation assistant.
Solve mathematical problems step by step using the calculator tool when needed.
Show your work and provide clear explanations.
Reference previous calculations from the conversation history if relevant."""

DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant.
Provide clear and helpful responses to user queries.
Use the conversation history to maintain context and provide better assistance."""


def get_chat_prompt_template(intent_type: str) -> ChatPromptTemplate:
    """
    Dynamic chat prompt selection based on intent type.
    Uses LangChain's ChatPromptTemplate with MessagesPlaceholder for conversation history.
    
    Args:
        intent_type: The classified intent ("qa", "summarization", "calculation")
    
    Returns:
        ChatPromptTemplate with appropriate system prompt and message structure
    """
    if intent_type == "qa":
        system_prompt = QA_SYSTEM_PROMPT
    elif intent_type == "summarization":
        system_prompt = SUMMARIZATION_SYSTEM_PROMPT
    elif intent_type == "calculation":
        system_prompt = CALCULATION_SYSTEM_PROMPT
    else:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    
    # Create ChatPromptTemplate with system message, conversation history, and current input
    template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="conversation_history", optional=True),
        ("human", "{user_input}")
    ])
    
    return template
