"""Node functions for the agent workflow."""

from datetime import datetime
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from ..schemas import UserIntent, AnswerResponse
from ..prompts import SimpleLLMSimulator
from ..tools import calculate, langchain_calculate

llm = SimpleLLMSimulator()

def classify_intent(state):
    """Classify user intent and add to messages."""
    user_input = state["user_input"]
    
    # Add user message to conversation
    user_message = HumanMessage(content=user_input)
    
    # Classify intent
    if any(word in user_input.lower() for word in ["calculate", "compute", "+", "-", "*", "/"]):
        intent_type = "calculation"
    elif any(word in user_input.lower() for word in ["summarize", "summary"]):
        intent_type = "summarization"
    else:
        intent_type = "qa"
    
    intent = UserIntent(
        intent_type=intent_type,
        confidence=0.9,
        reasoning=f"Classified as {intent_type} based on keywords"
    )
    
    # Add system message about intent classification
    system_message = SystemMessage(
        content=f"Intent classified as: {intent_type} (confidence: {intent.confidence})"
    )
    
    return {
        "intent": intent,
        "current_step": "classify_intent",
        "messages": [user_message, system_message]
    }

def qa_agent(state):
    """Handle Q&A requests using messages context."""
    user_input = state["user_input"]
    messages = state.get("messages", [])
    
    # Look at conversation history in messages
    conversation_context = ""
    for msg in messages[-10:]:  # Last 10 messages for context
        if isinstance(msg, HumanMessage):
            conversation_context += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            conversation_context += f"Assistant: {msg.content}\n"
    
    # Generate answer with context
    if "what did i just ask" in user_input.lower():
        # Find last user question (excluding current one)
        last_user_msg = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage) and msg.content.lower() != user_input.lower():
                last_user_msg = msg.content
                break
        
        if last_user_msg:
            answer = f"You asked: {last_user_msg}"
        else:
            answer = "I don't see any previous questions in our conversation."
    elif "capital of france" in user_input.lower():
        answer = "Paris"
    elif "what is ai" in user_input.lower():
        answer = "AI stands for Artificial Intelligence, which refers to computer systems that can perform tasks typically requiring human intelligence."
    else:
        # Use conversation context if available
        if conversation_context:
            answer = f"Based on our conversation, here's my response to: {user_input}"
        else:
            answer = f"I understand you're asking about: {user_input}. How can I help you with that?"
    
    response = AnswerResponse(
        question=user_input,
        answer=answer,
        sources=["knowledge_base"],
        confidence=0.95,
        timestamp=datetime.now()
    )
    
    # Add assistant response to messages
    assistant_message = AIMessage(content=answer)
    
    return {
        "response": response,
        "current_step": "qa_agent",
        "messages": [assistant_message]
    }

def calculation_agent(state):
    """Handle calculations using messages for context."""
    user_input = state["user_input"]
    
    # Use LangChain calculator tool (with parameter schema)
    # langchain_calculate expects a keyword argument 'expression'
    result = langchain_calculate(expression=user_input)
    
    response = AnswerResponse(
        question=user_input,
        answer=result,
        sources=["calculator_tool"],
        confidence=1.0,
        timestamp=datetime.now()
    )
    
    # Add messages
    assistant_message = AIMessage(content=f"Calculation result: {result}")
    
    return {
        "response": response,
        "current_step": "calculation_agent",
        "messages": [assistant_message]
    }

def summarization_agent(state):
    """Handle summarization requests."""
    user_input = state["user_input"]
    messages = state.get("messages", [])
    
    # Get conversation to summarize
    if len(messages) > 2:
        summary = f"Summary of our conversation: We've discussed {len(messages)} messages."
    else:
        summary = f"Summary: {user_input[:100]}..."
    
    response = AnswerResponse(
        question=user_input,
        answer=summary,
        sources=["document_processor"],
        confidence=0.8,
        timestamp=datetime.now()
    )
    
    assistant_message = AIMessage(content=summary)
    
    return {
        "response": response,
        "current_step": "summarization_agent",
        "messages": [assistant_message]
    }

def update_memory(state):
    """Update memory with conversation from messages."""
    messages = state.get("messages", [])
    current_memory = state.get("memory", [])
    
    # Convert recent messages to memory format
    memory_entry = {
        "user_input": state["user_input"],
        "response": state["response"].answer if state["response"] else "",
        "timestamp": datetime.now().isoformat(),
        "messages_count": len(messages)
    }
    
    # Add to memory
    updated_memory = current_memory + [memory_entry]
    
    return {
        "memory": updated_memory,
        "current_step": "update_memory"
    }
