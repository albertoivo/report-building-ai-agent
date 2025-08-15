"""Simple prompt templates for the agent."""

from typing import Dict, Any


class PromptTemplate:
    """Simple prompt template class."""
    
    def __init__(self, input_variables: list, template: str):
        self.input_variables = input_variables
        self.template = template
    
    def format(self, **kwargs) -> str:
        """Format the template with provided variables."""
        return self.template.format(**kwargs)


class ChatPromptTemplate:
    """Simple chat prompt template class."""
    
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
    
    def format_messages(self, **kwargs) -> list:
        """Format messages for chat."""
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": kwargs.get("user_input", "")}
        ]


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
Answer user questions clearly and concisely. 
Provide accurate information and cite sources when possible."""

SUMMARIZATION_SYSTEM_PROMPT = """You are a text summarization assistant.
Create concise and informative summaries of the provided text.
Focus on key points and main ideas."""

CALCULATION_SYSTEM_PROMPT = """You are a mathematical calculation assistant.
Solve mathematical problems step by step.
Show your work and provide clear explanations."""

DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant.
Provide clear and helpful responses to user queries."""


def get_chat_prompt_template(intent_type: str) -> ChatPromptTemplate:
    """
    Dynamic chat prompt selection based on intent type.
    
    Args:
        intent_type: The classified intent ("qa", "summarization", "calculation")
    
    Returns:
        ChatPromptTemplate with appropriate system prompt
    """
    if intent_type == "qa":
        return ChatPromptTemplate(QA_SYSTEM_PROMPT)
    elif intent_type == "summarization":
        return ChatPromptTemplate(SUMMARIZATION_SYSTEM_PROMPT)
    elif intent_type == "calculation":
        return ChatPromptTemplate(CALCULATION_SYSTEM_PROMPT)
    else:
        return ChatPromptTemplate(DEFAULT_SYSTEM_PROMPT)
