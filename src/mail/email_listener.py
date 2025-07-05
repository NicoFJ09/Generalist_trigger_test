"""
Email Listener using Composio's toolset for Gmail trigger handling.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mail.email_handler import EmailHandler


class EmailListener:
    """
    Handles email listening functionality for new Gmail messages.
    """
    TRIGGER_NAME = "GMAIL_NEW_GMAIL_MESSAGE"

    def __init__(self, email_handler: EmailHandler):
        self.email_handler = email_handler
        self.listener = self.email_handler.toolset.create_trigger_listener()

    def setup_listener(self):
        """Setup email listener with callback."""
        @self.listener.callback(
            filters={
                "trigger_name": self.TRIGGER_NAME,
            }
        )
        def handle_trigger(event):
            print("📧 New email received...")
            payload = event.payload

            # Extract email information from payload
            sender = payload.get("sender", "")
            email_text = payload.get("message_text", "")
            thread_id = payload.get("thread_id", "")

            print(f"From: {sender}")
            print(f"Thread ID: {thread_id}")
            print(f"Preview: {email_text}")

            # Process the email
            self.process_email(sender, email_text, thread_id)

    def process_email(self, sender: str, email_text: str, thread_id: str):
        """Process incoming email."""
        print(f"📨 Processing email from: {sender}")
        print(f"📝 Content preview: {email_text[:150]}...")
        print(f"🧵 Thread ID: {thread_id}")
        print("✅ Email processed successfully")
        print("-" * 50)

    def start_listening(self):
        """Start listening for new emails."""
        print("🔄 Starting email listener...")
        self.setup_listener()
        print("👂 Listening for new emails...")
        self.listener.wait_forever()
