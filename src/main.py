#!/usr/bin/env python3
"""
Main entry point for the AI Email Agent system.
"""

import os
import sys
import threading
import time
from typing import Optional

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mail.email_handler import EmailHandler
from mail.email_listener import EmailListener
from agent.ai_agent import EmailAIAgent
from config.settings import GMAIL_INTEGRATION_ID
from rich.console import Console
from rich.prompt import Prompt
from langchain_core.messages import HumanMessage

console = Console()

class EmailAgentMain:
    """Main application class for the Email Agent system."""
    
    def __init__(self):
        self.email_handler: EmailHandler
        self.ai_agent: EmailAIAgent
        self.email_listener: EmailListener
        self.listening_thread: Optional[threading.Thread] = None
        self.user_id = "default_user"
        
    def initialize_system(self):
        """Initialize all system components."""
        try:
            console.print("🚀 [bold cyan]Starting AI Email Agent[/bold cyan]")
            
            # Initialize email handler
            self.email_handler = EmailHandler(GMAIL_INTEGRATION_ID, self.user_id)
            
            # Initialize AI agent
            self.ai_agent = EmailAIAgent(self.email_handler)
            
            # Initialize email listener
            self.email_listener = EmailListener(self.email_handler, self.ai_agent)
            
            # Enable email triggers
            self.email_handler.enable_trigger()
            
            console.print("✅ [bold green]System ready![/bold green]")
            
        except Exception as e:
            console.print(f"❌ [bold red]System initialization failed: {e}[/bold red]")
            raise
    
    def start_listening(self):
        """Start listening for emails in a background thread."""
        if self.email_listener and not self.listening_thread:
            self.listening_thread = threading.Thread(
                target=self.email_listener.start_listening, 
                daemon=True
            )
            self.listening_thread.start()
            console.print("👂 [bold green]Email listener active[/bold green]")
    
    def stop_listening(self):
        """Stop the email listening thread."""
        if self.listening_thread and self.listening_thread.is_alive():
            # Note: This is a simplified stop mechanism
            # In a real implementation, you'd want a proper shutdown signal
            console.print("⏹️  [bold yellow]Stopping email listener...[/bold yellow]")
    
    def run_interactive_cli(self):
        """Run the interactive command-line interface."""
        console.print("\n📋 [bold cyan]Commands:[/bold cyan] prompt <text> | memory | profile | quit")
        
        while True:
            try:
                command = Prompt.ask("\n[bold cyan]>[/bold cyan]").strip()
                
                if not command:
                    continue
                    
                parts = command.split(None, 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if cmd == "help":
                    self.show_help()
                elif cmd == "prompt":
                    if args:
                        response = self.process_custom_prompt(args)
                        console.print(f"🤖 {response}")
                    else:
                        console.print("❌ Usage: prompt <your question>")
                elif cmd == "memory":
                    self.show_memory_stats()
                elif cmd == "profile":
                    self.email_handler.display_profile()
                elif cmd in ["quit", "exit", "q"]:
                    break
                else:
                    console.print(f"❌ Unknown command. Available: prompt, memory, profile, quit")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"❌ Error: {e}")
        
        console.print("\n👋 [bold cyan]Goodbye![/bold cyan]")
    
    def process_custom_prompt(self, prompt_text: str) -> str:
        """Process a custom prompt with AI."""
        try:
            messages = [HumanMessage(content=prompt_text)]
            response = self.ai_agent.model.invoke(messages)
            return str(response.content)
        except Exception as e:
            return f"Error: {e}"
    
    def show_help(self):
        """Show help information."""
        console.print("\n📋 [bold cyan]Commands:[/bold cyan]")
        console.print("• [bold]prompt <text>[/bold] - Ask AI a question")
        console.print("• [bold]memory[/bold] - Show email memory stats")
        console.print("• [bold]profile[/bold] - Show Gmail profile")
        console.print("• [bold]quit[/bold] - Exit")
    
    def show_memory_stats(self):
        """Show memory statistics."""
        console.print(f"\n🧠 Memory: {len(self.ai_agent.email_memory)} senders")
        if self.ai_agent.email_memory:
            for sender, emails in self.ai_agent.email_memory.items():
                console.print(f"  • {sender}: {len(emails)} emails")


def main():
    """Main entry point."""
    try:
        # Create and initialize the system
        app = EmailAgentMain()
        app.initialize_system()
        
        # Start listening for emails
        app.start_listening()
        
        # Run interactive CLI
        app.run_interactive_cli()
        
    except KeyboardInterrupt:
        console.print("\n🛑 [bold yellow]System interrupted by user[/bold yellow]")
    except Exception as e:
        console.print(f"❌ [bold red]Fatal error: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
