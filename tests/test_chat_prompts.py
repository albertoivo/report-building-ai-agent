"""Test the dynamic chat prompt selection functionality."""

import sys
import unittest
from pathlib import Path

# Add parent directory to path so we can import app module
sys.path.append(str(Path(__file__).parent.parent))

from app.prompts import get_chat_prompt_template
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage


class TestChatPrompts(unittest.TestCase):
    """Unit tests for dynamic chat prompt selection."""
    
    def test_qa_intent_prompt(self):
        """Test that QA intent returns appropriate ChatPromptTemplate."""
        prompt = get_chat_prompt_template("qa")
        
        # Verify it's a LangChain ChatPromptTemplate
        self.assertIsInstance(prompt, ChatPromptTemplate)
        
        # Test formatting with conversation history
        messages = prompt.format_messages(
            user_input="What is AI?",
            conversation_history=[
                HumanMessage(content="Hello"),
                AIMessage(content="Hi there!")
            ]
        )
        
        # Should have system message, conversation history, and user input
        self.assertGreater(len(messages), 2)
        self.assertEqual(messages[0].type, "system")
        self.assertIn("question-answering assistant", messages[0].content)
    
    def test_calculation_intent_prompt(self):
        """Test that calculation intent returns appropriate ChatPromptTemplate."""
        prompt = get_chat_prompt_template("calculation")
        
        self.assertIsInstance(prompt, ChatPromptTemplate)
        
        messages = prompt.format_messages(
            user_input="2 + 2",
            conversation_history=[]
        )
        
        self.assertGreater(len(messages), 0)
        self.assertEqual(messages[0].type, "system")
        self.assertIn("mathematical calculation assistant", messages[0].content)
    
    def test_summarization_intent_prompt(self):
        """Test that summarization intent returns appropriate ChatPromptTemplate."""
        prompt = get_chat_prompt_template("summarization")
        
        self.assertIsInstance(prompt, ChatPromptTemplate)
        
        messages = prompt.format_messages(
            user_input="Summarize our conversation",
            conversation_history=[]
        )
        
        self.assertGreater(len(messages), 0)
        self.assertEqual(messages[0].type, "system")
        self.assertIn("summarization assistant", messages[0].content)
    
    def test_default_intent_prompt(self):
        """Test that unknown intent returns default ChatPromptTemplate."""
        prompt = get_chat_prompt_template("unknown_intent")
        
        self.assertIsInstance(prompt, ChatPromptTemplate)
        
        messages = prompt.format_messages(
            user_input="Help me",
            conversation_history=[]
        )
        
        self.assertGreater(len(messages), 0)
        self.assertEqual(messages[0].type, "system")
        self.assertIn("helpful AI assistant", messages[0].content)
    
    def test_conversation_history_handling(self):
        """Test that conversation history is properly handled."""
        prompt = get_chat_prompt_template("qa")
        
        # Test with conversation history
        conversation_history = [
            HumanMessage(content="What is Python?"),
            AIMessage(content="Python is a programming language."),
            HumanMessage(content="What about Java?")
        ]
        
        messages = prompt.format_messages(
            user_input="Compare them",
            conversation_history=conversation_history
        )
        
        # Should include system message, conversation history, and current input
        self.assertGreater(len(messages), len(conversation_history))
        
        # Check that conversation history is preserved
        history_found = False
        for msg in messages:
            if hasattr(msg, 'content') and "Python is a programming language" in str(msg.content):
                history_found = True
                break
        
        self.assertTrue(history_found, "Conversation history should be included in messages")
    
    def test_empty_conversation_history(self):
        """Test that empty conversation history works correctly."""
        prompt = get_chat_prompt_template("qa")
        
        messages = prompt.format_messages(
            user_input="Hello",
            conversation_history=[]
        )
        
        # Should work without errors
        self.assertGreater(len(messages), 0)
        self.assertEqual(messages[-1].type, "human")
        self.assertEqual(messages[-1].content, "Hello")


if __name__ == "__main__":
    unittest.main()
