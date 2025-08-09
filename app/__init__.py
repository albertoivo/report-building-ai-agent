"""
Report-Building Agent Application Package.

This package contains the core schemas and functionality for the Report-Building Agent
built as part of the Udacity AI course project.
"""

from .schemas import AnswerResponse, UserIntent
from .log_schemas import SimpleLog

__version__ = "1.0.0"
__author__ = "Report-Building Agent Team"

__all__ = [
    "AnswerResponse",
    "UserIntent", 
    "SimpleLog"
]
