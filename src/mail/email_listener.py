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
        self.processed_events = set()  # Track processed events to prevent duplicates

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
            
            # Create a unique event identifier to prevent duplicates
            event_id = f"{thread_id}_{hash(sender)}_{hash(email_text[:50])}"
            
            # Check if we've already processed this event
            if event_id in self.processed_events:
                return  # Skip duplicate
            
            # Mark event as processed
            self.processed_events.add(event_id)
            
            # Process the email with AI if agent is available
            if self.ai_agent:
                self.ai_agent.process_incoming_email(sender, email_text, thread_id)
            else:
                self.process_email(sender, email_text, thread_id)
            
            # Clean up old events to prevent memory leaks
            if len(self.processed_events) > 100:
                old_events = list(self.processed_events)[:20]
                for old_event in old_events:
                    self.processed_events.discard(old_event)

    def process_email(self, sender: str, email_text: str, thread_id: str):
        """Basic email processing without AI."""
        print(f"📨 Processed email from: {sender}")
        print("-" * 50)

    def start_listening(self):
        """Start listening for new emails."""
        print("🔄 Starting email listener...")
        self.setup_listener()
        # Use a non-blocking approach
        import time
        try:
            while True:
                time.sleep(1)  # Small delay to prevent busy waiting
        except KeyboardInterrupt:
            print("🛑 Email listener stopped")
        except Exception as e:
            print(f"❌ Email listener error: {e}")
            import traceback
            traceback.print_exc()
