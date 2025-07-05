"""
Email Listener using Composio's toolset for Gmail trigger handling with AI Agent integration.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mail.email_handler import EmailHandler


class EmailListener:
    """
    Handles email listening functionality for new Gmail messages with AI processing.
    """
    TRIGGER_NAME = "GMAIL_NEW_GMAIL_MESSAGE"

    def __init__(self, email_handler: EmailHandler, ai_agent=None):
        self.email_handler = email_handler
        self.ai_agent = ai_agent
        self.listener = self.email_handler.toolset.create_trigger_listener()

    def setup_listener(self):
        """Setup email listener with callback."""
        @self.listener.callback(
            filters={
                "trigger_name": self.TRIGGER_NAME,
            }
        )
        def handle_trigger(event):
            payload = event.payload

            # Extract email information from payload
            sender = payload.get("sender", "")
            email_text = payload.get("message_text", "")
            thread_id = payload.get("thread_id", "")

            # Process the email with AI if agent is available
            if self.ai_agent:
                self.ai_agent.process_incoming_email(sender, email_text, thread_id)
            else:
                self.process_email(sender, email_text, thread_id)

    def process_email(self, sender: str, email_text: str, thread_id: str):
        """Basic email processing without AI."""
        print(f"📨 Processed email from: {sender}")
        print("-" * 50)

    def start_listening(self):
        """Start listening for new emails."""
        print("🔄 Starting email listener...")
        self.setup_listener()
        print("👂 Listening for new emails...")
        self.listener.wait_forever()
