"""
Email display components for formatting email-related UI.
"""

from rich.panel import Panel
from typing import Dict, Any, List
from .console_manager import ConsoleManager


class EmailDisplay:
    """Handles all email-related display logic."""
    
    def __init__(self, console_manager: ConsoleManager):
        self.console = console_manager
    
    def show_email_panel(self, sender_email: str, email_content: str):
        """Display email content in a formatted panel."""
        self.console.print_panel(
            email_content,
            title=f"📧 Email from {sender_email}",
            border_style="blue"
        )
    
    def show_response_panel(self, response: str):
        """Display generated response in a formatted panel."""
        self.console.print_panel(
            response,
            title="🤖 Generated Response",
            border_style="green"
        )
    
    def show_memory_stats(self, memory_stats: Dict[str, Any]):
        """Display email memory statistics."""
        self.console.print_header("Email Memory Statistics")
        
        stats = memory_stats
        self.console.print(f"📧 Total senders: {stats.get('total_senders', 0)}")
        self.console.print(f"🔄 Processed threads: {stats.get('processed_threads', 0)}")
        self.console.print(f"👤 Senders with extracted info: {stats.get('senders_with_info', 0)}")
        
        if stats.get('email_history'):
            self.console.print(f"\n📊 [bold green]Email History:[/bold green]")
            for sender, count in stats['email_history'].items():
                self.console.print(f"  • {sender}: {count} emails")
        
        if stats.get('sender_info'):
            self.console.print(f"\n👤 [bold yellow]Sender Information:[/bold yellow]")
            for sender, info in stats['sender_info'].items():
                info_str = ", ".join([f"{k}: {v}" for k, v in info.items()])
                self.console.print(f"  • {sender}: {info_str}")
        else:
            self.console.print(f"\n👤 [bold dim]No sender information learned yet[/bold dim]")
    
    def show_sender_info_learned(self, details: str):
        """Show when sender information is learned."""
        self.console.print_info(f"Learned key details about sender: {details}")
    
    def show_email_processing_start(self, sender_email: str, thread_id: str):
        """Show when email processing starts."""
        self.console.print(f"\n📧 Processing email from {sender_email} (Thread: {thread_id})")
    
    def show_response_generation(self):
        """Show when response is being generated."""
        self.console.print("🤖 Generating response...")
    
    def show_email_sent_success(self):
        """Show when email is sent successfully."""
        self.console.print_success("Response sent successfully!")
    
    def show_email_sent_failure(self):
        """Show when email sending fails."""
        self.console.print_error("Failed to send response")
    
    def show_response_cancelled(self):
        """Show when response is cancelled."""
        self.console.print_error("Response cancelled")
    
    def ask_send_approval(self) -> bool:
        """Ask user for approval to send response."""
        return self.console.ask_confirmation("Send this response?", default=True)
    
    def show_processing_status(self, status: str):
        """Show processing status."""
        status_icons = {
            "ready": "✅",
            "listening": "👂",
            "processing": "🔄",
            "error": "❌",
            "warning": "⚠️"
        }
        
        icon = status_icons.get(status.lower(), "ℹ️")
        self.console.print(f"{icon} {status}")
    
    def show_help(self):
        """Show help information."""
        self.console.print("\n📋 [bold cyan]Available Commands:[/bold cyan]")
        self.console.print("• [bold]prompt <text>[/bold] - Ask AI a question")
        self.console.print("• [bold]memory[/bold] - Show email memory and sender info")
        self.console.print("• [bold]profile[/bold] - Show Gmail profile")
        self.console.print("• [bold]quit[/bold] - Exit the application")
        self.console.print("\n💡 [bold yellow]Note:[/bold yellow] Email responses are handled automatically with approval prompts")
    
    def show_commands_info(self):
        """Show available commands at startup."""
        self.console.print("\n📋 [bold cyan]Commands:[/bold cyan] prompt <text> | memory | profile | quit")
        self.console.print("💡 [bold yellow]Note:[/bold yellow] Email responses are handled automatically with approval prompts\n")
        self.console.print("🔄 [bold green]Email listener is active. You can use commands or wait for emails.[/bold green]\n")
