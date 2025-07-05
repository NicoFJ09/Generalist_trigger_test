"""
Email manager for coordinating email operations.
"""

import sys
from typing import Optional
from services.email_processor import EmailProcessor
from services.memory_manager import MemoryManager
from services.sender_info_extractor import SenderInfoExtractor
from services.response_generator import ResponseGenerator
from core.user_profile import UserProfile
from ui.user_interface import UserInterface


class EmailManager:
    """Manages email operations and coordinates between services."""
    
    def __init__(self, email_handler):
        self.email_handler = email_handler
        self.user_profile = UserProfile(email_handler)
        self.ui = UserInterface()
        
        # Initialize services
        self.memory_manager = MemoryManager()
        self.sender_info_extractor = SenderInfoExtractor()
        self.response_generator = ResponseGenerator()
        self.email_processor = EmailProcessor(
            self.memory_manager,
            self.sender_info_extractor,
            self.response_generator
        )
    
    def process_incoming_email(self, sender: str, email_text: str, thread_id: str):
        """Process incoming email and handle response."""
        try:
            sender_email = self.email_processor.parse_sender_email(sender)
            
            # Show processing start
            self.ui.show_email_processing_start(sender_email, thread_id)
            
            # Process email
            user_info = self.user_profile.get_user_info()
            result = self.email_processor.process_email(sender, email_text, thread_id, user_info)
            
            if not result["success"]:
                if result["reason"] == "already_processed":
                    self.ui.show_processing_status(f"Already processed thread {thread_id}, skipping...")
                else:
                    self.ui.show_error(f"Processing error: {result.get('error', 'Unknown error')}")
                return
            
            # Show sender info if learned
            if result.get("sender_info"):
                details = ", ".join([f"{k}: {v}" for k, v in result["sender_info"].items()])
                self.ui.show_sender_info_learned(details)
            
            # Show response generation
            self.ui.show_response_generation()
            
            # Get approval and send response
            self._handle_response_approval(sender, sender_email, email_text, result["response"], thread_id)
            
        except Exception as e:
            self.ui.show_error(f"Error processing email: {e}")
    
    def _handle_response_approval(self, sender: str, sender_email: str, email_text: str, response: str, thread_id: str):
        """Handle response approval and sending."""
        # Show response for approval
        approved = self.ui.show_email_for_approval(sender_email, email_text, response)
        
        if approved:
            success = self._send_response(sender_email, response, thread_id, sender, email_text)
            if success:
                self.ui.show_email_sent_success()
            else:
                self.ui.show_email_sent_failure()
        else:
            self.ui.show_response_cancelled()
        
        # Show command prompt
        self.ui.show_command_prompt()
    
    def _send_response(self, sender_email: str, response: str, thread_id: str, sender: str, email_text: str) -> bool:
        """Send the response email."""
        try:
            success = self.email_handler.reply_to_thread(
                recipient_email=sender_email,
                message_text=response,
                thread_id=thread_id
            )
            
            if success:
                # Update memory with the response
                self.email_processor.update_memory_with_response(sender, email_text, thread_id, response)
                
            return success
            
        except Exception as e:
            self.ui.show_error(f"Error sending response: {e}")
            return False
    
    def get_memory_stats(self) -> dict:
        """Get memory statistics."""
        return self.email_processor.get_memory_stats()
    
    def process_custom_prompt(self, prompt_text: str) -> str:
        """Process custom user prompt."""
        user_info = self.user_profile.get_user_info()
        return self.email_processor.generate_custom_response(prompt_text, user_info)
    
    def display_profile(self):
        """Display user profile."""
        self.user_profile.display_profile()
