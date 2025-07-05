"""
Main user interface coordinator for the email agent.
"""

from typing import Dict, Any
from .console_manager import ConsoleManager
from .email_display import EmailDisplay


class UserInterface:
    """Main UI coordinator that manages all user interactions."""
    
    def __init__(self):
        self.console = ConsoleManager()
        self.email_display = EmailDisplay(self.console)
    
    def show_startup_message(self):
        """Show application startup message."""
        self.console.print_header("Starting AI Email Agent")
    
    def show_system_ready(self):
        """Show system ready message."""
        self.console.print_success("System ready!")
    
    def show_system_error(self, error: str):
        """Show system initialization error."""
        self.console.print_error(f"System initialization failed: {error}")
    
    def show_listening_started(self):
        """Show that email listening has started."""
        self.console.print_success("Email listener active")
    
    def show_listening_stopped(self):
        """Show that email listening has stopped."""
        self.console.print_warning("Stopping email listener...")
    
    def show_goodbye(self):
        """Show goodbye message."""
        self.console.print("\n👋 [bold cyan]Goodbye![/bold cyan]")
    
    def show_commands_info(self):
        """Show available commands."""
        self.email_display.show_commands_info()
    
    def show_help(self):
        """Show help information."""
        self.email_display.show_help()
    
    def show_memory_stats(self, stats: Dict[str, Any]):
        """Show memory statistics."""
        self.email_display.show_memory_stats(stats)
    
    def show_ai_response(self, response: str):
        """Show AI response to user prompt."""
        self.console.print(f"\n🤖 [bold green]Assistant Response:[/bold green]")
        self.console.print(f"{response}\n")
    
    def show_unknown_command(self):
        """Show unknown command message."""
        self.console.print_error("Unknown command. Available: prompt, memory, profile, quit")
    
    def show_usage_error(self, usage: str):
        """Show usage error."""
        self.console.print_error(f"Usage: {usage}")
    
    def get_command_input(self) -> str:
        """Get command input from user."""
        return input("Command> ").strip()
    
    def show_error(self, error: str):
        """Show general error message."""
        self.console.print_error(f"Error: {error}")
    
    def show_interrupt(self):
        """Show keyboard interrupt message."""
        self.console.print("\n🛑 [bold yellow]System interrupted by user[/bold yellow]")
    
    def show_fatal_error(self, error: str):
        """Show fatal error message."""
        self.console.print_error(f"Fatal error: {error}")
    
    # Email-specific UI methods
    def show_email_for_approval(self, sender_email: str, email_content: str, response: str) -> bool:
        """Show email and response for approval."""
        self.email_display.show_email_panel(sender_email, email_content)
        self.email_display.show_response_panel(response)
        self.console.flush()
        return self.email_display.ask_send_approval()
    
    def show_email_processing_start(self, sender_email: str, thread_id: str):
        """Show email processing start."""
        self.email_display.show_email_processing_start(sender_email, thread_id)
    
    def show_response_generation(self):
        """Show response generation."""
        self.email_display.show_response_generation()
    
    def show_email_sent_success(self):
        """Show email sent success."""
        self.email_display.show_email_sent_success()
    
    def show_email_sent_failure(self):
        """Show email sent failure."""
        self.email_display.show_email_sent_failure()
    
    def show_response_cancelled(self):
        """Show response cancelled."""
        self.email_display.show_response_cancelled()
    
    def show_sender_info_learned(self, details: str):
        """Show sender information learned."""
        self.email_display.show_sender_info_learned(details)
    
    def show_processing_status(self, status: str):
        """Show processing status."""
        self.email_display.show_processing_status(status)
    
    def show_command_prompt(self):
        """Show command prompt."""
        print("Command> ", end="")
        self.console.flush()
