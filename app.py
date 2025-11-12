"""
Main entry point for LangGraph Studio.
Exposes the compiled LangGraph app for use with LangGraph Studio.
"""
# from src.order_entry import app
from minimal.order_entry import app

# Export the app for LangGraph Studio
__all__ = ["app"]

