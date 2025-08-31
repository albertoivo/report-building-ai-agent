from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from ..schemas import AnswerResponse
from ..tools import langchain_calculate
from ..services import IntentClassifier

intent_classifier = IntentClassifier()


def classify_intent(state):
    """Classify user intent using enhanced LLM-based classification."""
    user_input = state["user_input"]
    messages = state.get("messages", [])

    # Build conversation history for context
    conversation_history = ""
    for msg in messages[-10:]:  # Last 10 messages for context
        if isinstance(msg, HumanMessage):
            conversation_history += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            conversation_history += f"Assistant: {msg.content}\n"

    # Classify intent
    intent = intent_classifier.classify_intent(user_input, conversation_history)

    return {
        "intent": intent,
        "current_step": "classify_intent",
        "messages": [
            HumanMessage(content=user_input),
            SystemMessage(
                content=f"Intent classified as: {intent.intent_type} (confidence: {intent.confidence:.2f}) - {intent.reasoning}"
            ),
        ],
    }


def qa_agent(state):
    """Handle Q&A requests using messages context."""
    user_input = state["user_input"]
    messages = state.get("messages", [])

    # Special case: memory recall
    if "what did i just ask" in user_input.lower():
        # Find last user question (excluding current one)
        last_user_msg = None
        for msg in reversed(messages):
            if (
                isinstance(msg, HumanMessage)
                and msg.content.lower() != user_input.lower()
            ):
                last_user_msg = msg.content
                break
        answer = (
            f"You asked: {last_user_msg}"
            if last_user_msg
            else "I don't see any previous questions in our conversation."
        )
    else:
        # For all other questions, use OpenAI via the intent classifier's LLM
        # Build conversation context
        conversation_context = ""
        for msg in messages[-10:]:
            if isinstance(msg, HumanMessage):
                conversation_context += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                conversation_context += f"Assistant: {msg.content}\n"

        # Use the LLM to generate the answer
        try:
            # Create a simple prompt for Q&A
            prompt = f"Please answer this question: {user_input}"
            if conversation_context:
                prompt += f"\n\nConversation context:\n{conversation_context}"

            answer = intent_classifier.llm.generate(prompt)
        except Exception:
            # Fallback if OpenAI fails
            if conversation_context:
                answer = (
                    f"Based on our conversation, here's my response to: {user_input}"
                )
            else:
                answer = f"I understand you're asking about: {user_input}. How can I help you with that?"

    logger = state.get("logger")
    logger.log_tool_call("qa", {"question": user_input}, answer)

    response = AnswerResponse(
        question=user_input,
        answer=answer,
        sources=["knowledge_base"],
        confidence=0.95,
        timestamp=datetime.now(),
    )
    return {
        "response": response,
        "current_step": "qa_agent",
        "messages": [AIMessage(content=answer)],
    }


def calculation_agent(state):
    """Handle calculations using messages for context."""
    user_input = state["user_input"]

    # Extract mathematical expression from input
    # Remove common prefixes like "calculate", "compute", etc.
    expression = user_input.lower()
    for prefix in ["calculate", "compute", "solve", "what is", "what's"]:
        if expression.startswith(prefix):
            expression = expression[len(prefix) :].strip()
            break

    # Remove question marks and other non-mathematical characters at the end
    expression = expression.rstrip("?!.")

    # Use calculator tool
    result = langchain_calculate.invoke({"expression": expression})

    logger = state.get("logger")
    logger.log_tool_call("calculator", {"expression": expression}, result)

    response = AnswerResponse(
        question=user_input,
        answer=result,
        sources=["calculator_tool"],
        confidence=1.0,
        timestamp=datetime.now(),
    )
    return {
        "response": response,
        "current_step": "calculation_agent",
        "messages": [AIMessage(content=f"Calculation result: {result}")],
    }


def summarization_agent(state):
    """Handle summarization requests."""
    user_input = state["user_input"]
    messages = state.get("messages", [])

    # Generate summary
    if len(messages) > 2:
        summary = (
            f"Summary of our conversation: We've discussed {len(messages)} messages."
        )
    else:
        summary = f"Summary: {user_input[:100]}..."

    logger = state.get("logger")
    logger.log_tool_call("summarization", {"input": user_input}, summary)

    response = AnswerResponse(
        question=user_input,
        answer=summary,
        sources=["document_processor"],
        confidence=0.8,
        timestamp=datetime.now(),
    )
    return {
        "response": response,
        "current_step": "summarization_agent",
        "messages": [AIMessage(content=summary)],
    }


def update_memory(state):
    """Update memory with conversation from messages."""
    messages = state.get("messages", [])
    current_memory = state.get("memory", [])

    # Add memory entry
    memory_entry = {
        "user_input": state["user_input"],
        "response": state["response"].answer if state["response"] else "",
        "timestamp": datetime.now().isoformat(),
        "messages_count": len(messages),
    }

    return {"memory": current_memory + [memory_entry], "current_step": "update_memory"}
