import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

from ..schemas.logging import SessionLog, ToolCall


class SimpleLogger:
    """Simple logger for capturing tool calls and user sessions."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.current_session: Optional[SessionLog] = None
    
    def start_session(self, user_query: str) -> str:
        """Start a new session and return session ID."""
        session_id = str(uuid4())[:8]
        self.current_session = SessionLog(
            session_id=session_id,
            user_query=user_query
        )
        return session_id
    
    def log_tool_call(self, tool_name: str, parameters: dict, result: str = None):
        """Log a tool call to the current session."""
        if not self.current_session:
            return
        
        tool_call = ToolCall(
            tool_name=tool_name,
            parameters=parameters,
            result=result
        )
        self.current_session.tool_calls.append(tool_call)
    
    def end_session(self, response: str = None):
        """End the current session and save to file."""
        if not self.current_session:
            return
        
        self.current_session.response = response
        self.current_session.ended_at = datetime.now()
        
        # Save session to file
        session_file = self.log_dir / f"session_{self.current_session.session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(self.current_session.model_dump(), f, indent=2, default=str)
        
        self.current_session = None
