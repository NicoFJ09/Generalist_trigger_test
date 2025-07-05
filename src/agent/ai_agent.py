"""
Simple AI Agent for email processing with memory and human oversight.
"""

import sys
import os
from typing import Dict, Any, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from composio_langgraph import Action
from config.settings import OPENAI_API_KEY
from config.agent_config import AI_AGENT_CONFIG


class EmailAIAgent:
    """Simple AI Agent for processing emails with memory and human oversight."""
    
    def __init__(self, email_handler):
        self.email_handler = email_handler
        self.model = ChatOpenAI(
            model=AI_AGENT_CONFIG["model"],
            temperature=AI_AGENT_CONFIG["temperature"],
            max_completion_tokens=AI_AGENT_CONFIG["max_tokens"]
        )
        
        # In-memory storage for this session only
        self.email_memory = {}  # sender -> list of emails
        self.processed_threads = set()  # Track processed thread IDs
    
    def add_to_memory(self, sender: str, email_text: str, thread_id: str, response: Optional[str] = None):
        """Add email to memory."""
        if sender not in self.email_memory:
            self.email_memory[sender] = []
        
        self.email_memory[sender].append({
            "email": email_text[:300],  # Limit size
            "thread_id": thread_id,
            "response": response or ""
        })
        
        # Keep only last 5 emails per sender
        if len(self.email_memory[sender]) > 5:
            self.email_memory[sender] = self.email_memory[sender][-5:]
    
    def get_sender_context(self, sender: str) -> str:
        """Get context about previous interactions with this sender."""
        if sender not in self.email_memory:
            return "No previous interactions."
        
        context = f"Previous emails from {sender}:\n"
        for email in self.email_memory[sender][-2:]:  # Last 2 emails
            context += f"- {email['email'][:50]}...\n"
        
        return context
    
    def process_incoming_email(self, sender: str, email_text: str, thread_id: str):
        """Process incoming email and respond automatically."""
        try:
            # Check if we already processed this thread
            if thread_id in self.processed_threads:
                return
            
            sender_email = self.parse_sender_email(sender)
            print(f"📧 New email from {sender_email}")
            
            # Add to memory
            self.add_to_memory(sender, email_text, thread_id)
            
            # Get context
            context = self.get_sender_context(sender)
            
            # Generate response
            response = self.generate_response(sender, email_text, context)
            
            # Send response
            success = self.email_handler.reply_to_thread(
                recipient_email=sender_email,
                message_text=response,
                thread_id=thread_id
            )
            
            if success:
                # Mark thread as processed
                self.processed_threads.add(thread_id)
                # Update memory with the response
                self.add_to_memory(sender, email_text, thread_id, response)
                print(f"✅ Response sent to {sender_email}")
            else:
                print(f"❌ Failed to send response to {sender_email}")
            
        except Exception as e:
            print(f"❌ Error processing email: {e}")
    
    def generate_response(self, sender: str, email_text: str, context: str) -> str:
        """Generate AI response."""
        prompt = f"""You are a professional email assistant. Respond naturally and helpfully to this email.

Email from: {sender}
Content: {email_text}

{context}

Write a professional, friendly response without placeholders. Use a natural tone and provide helpful information."""
        
        try:
            messages = [HumanMessage(content=prompt)]
            response = self.model.invoke(messages)
            return str(response.content)
        except Exception as e:
            return f"Thank you for your email. I appreciate you reaching out and will get back to you soon."
    
    def parse_sender_email(self, sender_email: str) -> str:
        """
        The sender email is expected to be in the format "Name <email>"
        This function extracts the email part.
        """
        if "<" in sender_email and ">" in sender_email:
            return sender_email.split("<")[1].split(">")[0].strip()
        return sender_email.strip()
