"""
Email processor for handling email processing logic.
"""

from typing import Optional
from .memory_manager import MemoryManager
from .sender_info_extractor import SenderInfoExtractor
from .response_generator import ResponseGenerator


class EmailProcessor:
    """Handles core email processing logic."""
    
    def __init__(self, memory_manager: MemoryManager, sender_info_extractor: SenderInfoExtractor, response_generator: ResponseGenerator):
        self.memory_manager = memory_manager
        self.sender_info_extractor = sender_info_extractor
        self.response_generator = response_generator
    
    def process_email(self, sender: str, email_text: str, thread_id: str, user_info: dict) -> dict:
        """Process incoming email and return processing result."""
        # Check if already processed
        if self.memory_manager.is_thread_processed(thread_id):
            return {
                "success": False,
                "reason": "already_processed",
                "thread_id": thread_id
            }
        
        # Mark as processed immediately to prevent duplicates
        self.memory_manager.mark_thread_processed(thread_id)
        
        try:
            # Extract sender information
            sender_info = self.sender_info_extractor.extract_sender_info(email_text)
            
            # Add sender info to memory if any was extracted
            if sender_info:
                self.memory_manager.add_sender_info(sender, sender_info)
            
            # Add email to memory
            self.memory_manager.add_email_to_memory(sender, email_text, thread_id)
            
            # Get context for response generation
            context = self.memory_manager.get_sender_context(sender)
            
            # Generate response
            response = self.response_generator.generate_response(sender, email_text, context, user_info)
            
            return {
                "success": True,
                "response": response,
                "context": context,
                "sender_info": sender_info,
                "thread_id": thread_id
            }
            
        except Exception as e:
            # Remove from processed threads if there was an error
            self.memory_manager.unmark_thread_processed(thread_id)
            return {
                "success": False,
                "reason": "processing_error",
                "error": str(e),
                "thread_id": thread_id
            }
    
    def update_memory_with_response(self, sender: str, email_text: str, thread_id: str, response: str):
        """Update memory with sent response."""
        self.memory_manager.add_email_to_memory(sender, email_text, thread_id, response)
    
    def get_memory_stats(self) -> dict:
        """Get memory statistics."""
        return self.memory_manager.get_memory_stats()
    
    def parse_sender_email(self, sender_email: str) -> str:
        """Parse sender email to extract just the email part."""
        if "<" in sender_email and ">" in sender_email:
            return sender_email.split("<")[1].split(">")[0].strip()
        return sender_email.strip()
    
    def generate_custom_response(self, prompt_text: str, user_info: dict) -> str:
        """Generate custom response for user prompts."""
        system_status = {
            "monitoring_active": True,
            "remembered_senders": len(self.memory_manager.sender_info),
            "processed_threads": len(self.memory_manager.processed_threads)
        }
        
        return self.response_generator.generate_custom_response(prompt_text, user_info, system_status)
