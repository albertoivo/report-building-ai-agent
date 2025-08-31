from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class PromptTemplate:
    """Simple prompt template class."""

    def __init__(self, input_variables: list, template: str):
        self.input_variables = input_variables
        self.template = template

    def format(self, **kwargs) -> str:
        """Format the template with provided variables."""
        return self.template.format(**kwargs)


# Intent Classification Prompt
intent_classification_prompt = PromptTemplate(
    input_variables=["user_input", "conversation_history"],
    template="""Classify user intent:

CALCULATION: Math operations (+, -, *, /)
SUMMARIZATION: Summary requests  
QA: Questions, information requests

USER INPUT: {user_input}
CONVERSATION: {conversation_history}

Format:
Intent: [CALCULATION|SUMMARIZATION|QA]
Confidence: [0.0-1.0] 
Reasoning: [Brief explanation]
Keywords_Found: [Key terms found]
""",
)


# System Prompts
QA_SYSTEM_PROMPT = (
    "You are a helpful question-answering assistant. Answer questions clearly."
)

SUMMARIZATION_SYSTEM_PROMPT = (
    "You are a summarization assistant. Create concise summaries."
)

CALCULATION_SYSTEM_PROMPT = (
    "You are a mathematical calculation assistant. Solve problems step-by-step."
)

DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."


def get_chat_prompt_template(intent_type: str) -> ChatPromptTemplate:
    """Get ChatPromptTemplate based on intent type."""
    prompts = {
        "qa": QA_SYSTEM_PROMPT,
        "summarization": SUMMARIZATION_SYSTEM_PROMPT,
        "calculation": CALCULATION_SYSTEM_PROMPT,
    }

    system_prompt = prompts.get(intent_type, DEFAULT_SYSTEM_PROMPT)

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="conversation_history", optional=True),
            ("human", "{user_input}"),
        ]
    )
