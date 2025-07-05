"""
Refactored AI Agent with clean separation of concerns.
"""

import sys
import os
from typing import Dict, Any, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.email_manager import EmailManager


class EmailAIAgent:
    """Clean AI Agent that delegates to specialized services."""
    
    def __init__(self, email_handler):
        self.email_handler = email_handler
        self.email_manager = EmailManager(email_handler)
    
    def process_incoming_email(self, sender: str, email_text: str, thread_id: str):
        """Process incoming email - delegates to EmailManager."""
        self.email_manager.process_incoming_email(sender, email_text, thread_id)
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get user information - delegates to UserProfile."""
        return self.email_manager.user_profile.get_user_info()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics - delegates to EmailManager."""
        return self.email_manager.get_memory_stats()
    
    def process_custom_prompt(self, prompt_text: str) -> str:
        """Process custom prompt - delegates to EmailManager."""
        return self.email_manager.process_custom_prompt(prompt_text)
    
    def display_profile(self):
        """Display user profile - delegates to EmailManager."""
        self.email_manager.display_profile()
    
    # Legacy compatibility properties for existing code
    @property
    def email_memory(self):
        """Legacy compatibility - access to email memory."""
        return self.email_manager.memory_manager.email_memory
    
    @property
    def processed_threads(self):
        """Legacy compatibility - access to processed threads."""
        return self.email_manager.memory_manager.processed_threads
    
    @property
    def sender_info(self):
        """Legacy compatibility - access to sender info."""
        return self.email_manager.memory_manager.sender_info
    
    def parse_sender_email(self, sender_email: str) -> str:
        """Legacy compatibility - parse sender email."""
        return self.email_manager.email_processor.parse_sender_email(sender_email)
