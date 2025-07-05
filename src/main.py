#!/usr/bin/env python3
"""
Main entry point for the AI Email Agent system.
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
        console.print("💡 [bold yellow]Note:[/bold yellow] Email responses are handled automatically with approval prompts\n")
        console.print("🔄 [bold green]Email listener is active. You can use commands or wait for emails.[/bold green]\n")
        
        while True:
            try:
                # Use a more basic input to avoid Rich conflicts
                command = input("Command> ").strip()
                
                if not command:
                    continue
                
                # Handle email approval responses differently
                if command.lower() in ['y', 'yes', 'n', 'no']:
                    console.print("💡 [dim]Email approval should be handled automatically. If you see this, there might be a timing issue.[/dim]")
                    continue
                    
                parts = command.split(None, 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if cmd == "help":
                    self.show_help()
                elif cmd == "prompt":
                    if args:
                        response = self.process_custom_prompt(args)
                        console.print(f"\n🤖 [bold green]Assistant Response:[/bold green]")
                        console.print(f"{response}\n")
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
        """Process a custom prompt with AI, providing email assistant context."""
        try:
            # Get assistant context from config
            from config.agent_config import AI_AGENT_CONFIG
            assistant_info = AI_AGENT_CONFIG.get("assistant_context", {})
            
            # Get user information from Gmail profile
            user_info = self.ai_agent.get_user_info()
            user_name = user_info.get('name', 'User')
            user_email = user_info.get('email', 'your email')
            
            # Add email assistant context to the prompt
            enhanced_prompt = f"""You are an {assistant_info.get('role', 'AI Email Assistant')} working for {user_name} ({user_email}). 
            
{assistant_info.get('description', 'You help with email management and responses.')}

Your capabilities include:
{chr(10).join(['- ' + cap for cap in assistant_info.get('capabilities', ['Email assistance'])])}

Your owner information:
- Name: {user_name}
- Email: {user_email}
- Role: Professional Email Assistant

Current email system status:
- Active email monitoring: {"✅ Active" if hasattr(self, 'ai_agent') else "❌ Inactive"}
- Remembered senders: {len(self.ai_agent.sender_info) if hasattr(self, 'ai_agent') else 0}
- Email threads processed: {len(self.ai_agent.processed_threads) if hasattr(self, 'ai_agent') else 0}

User question: {prompt_text}

Provide a helpful, professional response as {user_name}'s email assistant. Always refer to the user as {user_name}, not as generic terms like "User" or with placeholders.
"""
            
            messages = [HumanMessage(content=enhanced_prompt)]
            response = self.ai_agent.model.invoke(messages)
            return str(response.content)
        except Exception as e:
            return f"Error: {e}"
    
    def show_help(self):
        """Show help information."""
        console.print("\n📋 [bold cyan]Available Commands:[/bold cyan]")
        console.print("• [bold]prompt <text>[/bold] - Ask AI a question")
        console.print("• [bold]memory[/bold] - Show email memory and sender info")
        console.print("• [bold]profile[/bold] - Show Gmail profile")
        console.print("• [bold]quit[/bold] - Exit the application")
        console.print("\n💡 [bold yellow]Note:[/bold yellow] Email responses are handled automatically with approval prompts")
    
    def show_memory_stats(self):
        """Show memory statistics."""
        console.print(f"\n🧠 [bold cyan]Email Memory Statistics[/bold cyan]")
        console.print(f"📧 Total senders: {len(self.ai_agent.email_memory)}")
        console.print(f"🔄 Processed threads: {len(self.ai_agent.processed_threads)}")
        console.print(f"👤 Senders with extracted info: {len(self.ai_agent.sender_info)}")
        
        if self.ai_agent.email_memory:
            console.print(f"\n📊 [bold green]Email History:[/bold green]")
            for sender, emails in self.ai_agent.email_memory.items():
                sender_email = self.ai_agent.parse_sender_email(sender)
                console.print(f"  • {sender_email}: {len(emails)} emails")
        
        # Show sender info if available
        if self.ai_agent.sender_info:
            console.print(f"\n👤 [bold yellow]Sender Information:[/bold yellow]")
            for sender, info in self.ai_agent.sender_info.items():
                sender_email = self.ai_agent.parse_sender_email(sender)
                info_str = ", ".join([f"{k}: {v}" for k, v in info.items()])
                console.print(f"  • {sender_email}: {info_str}")
        else:
            console.print(f"\n👤 [bold dim]No sender information learned yet[/bold dim]")


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
