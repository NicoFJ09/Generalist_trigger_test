"""
Console manager for centralized console output and formatting.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from typing import Optional


class ConsoleManager:
    """Centralized console management for all UI output."""
    
    def __init__(self):
        self.console = Console()
    
    def print(self, message: str, style: Optional[str] = None):
        """Print a message with optional styling."""
        if style:
            self.console.print(message, style=style)
        else:
            self.console.print(message)
    
    def print_success(self, message: str):
        """Print a success message."""
        self.console.print(f"✅ {message}", style="bold green")
    
    def print_error(self, message: str):
        """Print an error message."""
        self.console.print(f"❌ {message}", style="bold red")
    
    def print_warning(self, message: str):
        """Print a warning message."""
        self.console.print(f"⚠️ {message}", style="bold yellow")
    
    def print_info(self, message: str):
        """Print an info message."""
        self.console.print(f"💡 {message}", style="bold blue")
    
    def print_panel(self, content: str, title: str, border_style: str = "blue"):
        """Print content in a panel."""
        panel = Panel(content, title=title, border_style=border_style)
        self.console.print(panel)
    
    def print_header(self, title: str):
        """Print a header message."""
        self.console.print(f"\n🚀 [bold cyan]{title}[/bold cyan]")
    
    def print_separator(self):
        """Print a separator line."""
        self.console.print("-" * 50)
    
    def flush(self):
        """Flush the console output."""
        self.console.file.flush()
    
    def ask_confirmation(self, question: str, default: bool = True) -> bool:
        """Ask for yes/no confirmation."""
        suffix = "[y/N]" if not default else "[Y/n]"
        answer = input(f"\n{question} {suffix}: ").strip().lower()
        
        if not answer:
            return default
        
        return answer in ['y', 'yes']
    
    def get_input(self, prompt: str) -> str:
        """Get user input with a prompt."""
        return input(f"{prompt}: ").strip()
