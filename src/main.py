"""
Main entry point for the refactored AI Email Agent system.
Clean, modular architecture with separation of concerns.
"""

import os
import sys
import threading
from typing import Optional

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mail.email_handler import EmailHandler
from mail.email_listener import EmailListener
from agent.ai_agent import EmailAIAgent
from config.settings import GMAIL_INTEGRATION_ID
from ui.user_interface import UserInterface


class EmailAgentApp:
    """Main application class with clean architecture."""
    
    def __init__(self):
        # Core components
        self.email_handler: Optional[EmailHandler] = None
        self.ai_agent: Optional[EmailAIAgent] = None
        self.email_listener: Optional[EmailListener] = None
        self.ui = UserInterface()
        
        # Runtime state
        self.listening_thread: Optional[threading.Thread] = None
        self.user_id = "default_user"
        
    def initialize_system(self):
        """Initialize all system components."""
        try:
            self.ui.show_startup_message()
            
            # Initialize email handler
            self.email_handler = EmailHandler(GMAIL_INTEGRATION_ID, self.user_id)
            
            # Initialize AI agent
            self.ai_agent = EmailAIAgent(self.email_handler)
            
            # Initialize email listener
            self.email_listener = EmailListener(self.email_handler, self.ai_agent)
            
            # Enable email triggers
            self.email_handler.enable_trigger()
            
            self.ui.show_system_ready()
            
        except Exception as e:
            self.ui.show_system_error(str(e))
            raise
    
    def start_listening(self):
        """Start listening for emails in a background thread."""
        if self.email_listener and not self.listening_thread:
            self.listening_thread = threading.Thread(
                target=self.email_listener.start_listening, 
                daemon=True
            )
            self.listening_thread.start()
            self.ui.show_listening_started()
    
    def stop_listening(self):
        """Stop the email listening thread."""
        if self.listening_thread and self.listening_thread.is_alive():
            self.ui.show_listening_stopped()
    
    def run_interactive_cli(self):
        """Run the interactive command-line interface."""
        self.ui.show_commands_info()
        
        while True:
            try:
                command = self.ui.get_command_input()
                
                if not command:
                    continue
                
                # Handle email approval responses
                if command.lower() in ['y', 'yes', 'n', 'no']:
                    self.ui.show_processing_status("Email approval should be handled automatically")
                    continue
                    
                # Parse command
                parts = command.split(None, 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                # Execute command
                self._execute_command(cmd, args)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.ui.show_error(str(e))
        
        self.ui.show_goodbye()
    
    def _execute_command(self, cmd: str, args: str):
        """Execute a user command."""
        if cmd == "help":
            self.ui.show_help()
        elif cmd == "prompt":
            self._handle_prompt_command(args)
        elif cmd == "memory":
            self._handle_memory_command()
        elif cmd == "profile":
            self._handle_profile_command()
        elif cmd in ["quit", "exit", "q"]:
            sys.exit(0)
        else:
            self.ui.show_unknown_command()
    
    def _handle_prompt_command(self, args: str):
        """Handle prompt command."""
        if args and self.ai_agent:
            response = self.ai_agent.process_custom_prompt(args)
            self.ui.show_ai_response(response)
        else:
            self.ui.show_usage_error("prompt <your question>")
    
    def _handle_memory_command(self):
        """Handle memory command."""
        if self.ai_agent:
            stats = self.ai_agent.get_memory_stats()
            self.ui.show_memory_stats(stats)
    
    def _handle_profile_command(self):
        """Handle profile command."""
        if self.ai_agent:
            self.ai_agent.display_profile()


def main():
    """Main entry point."""
    try:
        # Create and initialize the system
        app = EmailAgentApp()
        app.initialize_system()
        
        # Start listening for emails
        app.start_listening()
        
        # Run interactive CLI
        app.run_interactive_cli()
        
    except KeyboardInterrupt:
        UserInterface().show_interrupt()
    except Exception as e:
        UserInterface().show_fatal_error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
