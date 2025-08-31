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


# Enhanced Intent Classification Prompt with sophisticated language understanding
intent_classification_prompt = PromptTemplate(
    input_variables=["user_input", "conversation_history"],
    template="""
You are an expert intent classification system with sophisticated language understanding capabilities. 
Your task is to accurately classify user intents based on their input and conversation context.

INTENT CATEGORIES:

1. **CALCULATION** - Mathematical operations, computations, numeric problems
   Examples: "2 + 2", "calculate 15% of 200", "what's 5 times 8", "solve x + 5 = 10"
   Keywords: calculate, compute, solve, math, equation, numbers, operators (+, -, *, /, %), percentage

2. **SUMMARIZATION** - Requests to summarize text, conversations, or documents
   Examples: "summarize this", "give me a summary", "what's the main point", "recap our conversation"
   Keywords: summarize, summary, recap, overview, main points, key takeaways, brief

3. **QA (Question-Answering)** - General questions, information requests, explanations
   Examples: "what is AI?", "how does this work?", "tell me about...", "explain the concept"
   Keywords: what, how, why, when, where, who, explain, define, tell me, describe

CLASSIFICATION INSTRUCTIONS:

1. **Primary Analysis**: Look for explicit keywords and phrases that indicate intent
2. **Context Analysis**: Consider conversation history for ambiguous cases
3. **Semantic Understanding**: Understand the underlying purpose, not just surface words
4. **Confidence Assessment**: 
   - HIGH (0.8-1.0): Clear keywords and unambiguous intent
   - MEDIUM (0.5-0.7): Some indicators but context-dependent 
   - LOW (0.0-0.4): Ambiguous or unclear intent

USER INPUT: {user_input}
CONVERSATION HISTORY: {conversation_history}

CLASSIFICATION RULES:
- If input contains mathematical expressions or computation requests → CALCULATION
- If input asks for summary, recap, or main points → SUMMARIZATION  
- If input is a general question or information request → QA
- Consider conversation context for ambiguous cases
- Default to QA for unclear cases

Provide your classification in the following structured format:

Intent: [CALCULATION|SUMMARIZATION|QA]
Confidence: [0.0-1.0]
Reasoning: [Detailed explanation of classification decision including key indicators, context considerations, and confidence factors]
Keywords_Found: [List specific keywords or phrases that influenced the decision]
Context_Influence: [How conversation history affected the classification, if applicable]
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
