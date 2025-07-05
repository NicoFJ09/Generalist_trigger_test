"""
Memory manager for handling email memory and sender information.
"""

from typing import Dict, Any, Optional, List
from config.agent_config import MEMORY_CONFIG


class MemoryManager:
    """Manages email memory and sender information."""
    
    def __init__(self):
        self.email_memory: Dict[str, List[Dict[str, Any]]] = {}
        self.processed_threads: set = set()
        self.sender_info: Dict[str, Dict[str, Any]] = {}
    
    def add_email_to_memory(self, sender: str, email_text: str, thread_id: str, response: Optional[str] = None):
        """Add email to memory."""
        if sender not in self.email_memory:
            self.email_memory[sender] = []
        
        self.email_memory[sender].append({
            "email": email_text[:MEMORY_CONFIG.get("max_email_length", 1000)],
            "thread_id": thread_id,
            "response": response or ""
        })
        
        # Keep only last N emails per sender
        max_emails = MEMORY_CONFIG["max_emails_per_sender"]
        if len(self.email_memory[sender]) > max_emails:
            self.email_memory[sender] = self.email_memory[sender][-max_emails:]
    
    def add_sender_info(self, sender: str, info: Dict[str, Any]):
        """Add or update sender information."""
        if sender not in self.sender_info:
            self.sender_info[sender] = {}
        
        self.sender_info[sender].update(info)
    
    def get_sender_context(self, sender: str) -> str:
        """Get context about previous interactions with this sender."""
        context = ""
        
        # Add sender information if available
        if sender in self.sender_info and self.sender_info[sender]:
            context += "Known information about sender:\n"
            for info_type, value in self.sender_info[sender].items():
                context += f"- {info_type.title()}: {value}\n"
            context += "\n"
        
        # Add previous email context
        if sender not in self.email_memory:
            context += "No previous interactions."
        else:
            context_window = MEMORY_CONFIG["context_window"]
            recent_emails = self.email_memory[sender][-context_window:]
            context += f"Previous {len(recent_emails)} emails from {sender}:\n"
            for i, email in enumerate(recent_emails, 1):
                context += f"{i}. {email['email'][:100]}...\n"
        
        return context
    
    def is_thread_processed(self, thread_id: str) -> bool:
        """Check if thread has been processed."""
        return thread_id in self.processed_threads
    
    def mark_thread_processed(self, thread_id: str):
        """Mark thread as processed."""
        self.processed_threads.add(thread_id)
    
    def unmark_thread_processed(self, thread_id: str):
        """Remove thread from processed list (for error handling)."""
        self.processed_threads.discard(thread_id)
    
    def validate_sender_info(self, sender: str):
        """Validate and clean sender info to ensure it's in the correct format."""
        if sender not in self.sender_info:
            self.sender_info[sender] = {}
            return
            
        # Check if sender_info is a dictionary
        if not isinstance(self.sender_info[sender], dict):
            self.sender_info[sender] = {}
            return
            
        # Check each value in the dictionary
        cleaned_info = {}
        for key, value in self.sender_info[sender].items():
            if isinstance(value, (str, int, float)):
                # Valid types
                cleaned_info[key] = value
            elif isinstance(value, (list, tuple)):
                # Convert lists/tuples to strings
                if value:
                    cleaned_info[key] = str(value[0]) if len(value) > 0 else ""
            else:
                # Convert other types to string
                cleaned_info[key] = str(value)
        
        self.sender_info[sender] = cleaned_info
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics for display."""
        stats: Dict[str, Any] = {
            "total_senders": len(self.email_memory),
            "processed_threads": len(self.processed_threads),
            "senders_with_info": len(self.sender_info)
        }
        
        if self.email_memory:
            stats["email_history"] = {}
            for sender, emails in self.email_memory.items():
                # Parse sender email for display
                sender_email = self._parse_sender_email(sender)
                stats["email_history"][sender_email] = len(emails)
        
        if self.sender_info:
            stats["sender_info"] = {}
            for sender, info in self.sender_info.items():
                sender_email = self._parse_sender_email(sender)
                stats["sender_info"][sender_email] = info
        
        return stats
    
    def _parse_sender_email(self, sender_email: str) -> str:
        """Parse sender email to extract just the email part."""
        if "<" in sender_email and ">" in sender_email:
            return sender_email.split("<")[1].split(">")[0].strip()
        return sender_email.strip()
