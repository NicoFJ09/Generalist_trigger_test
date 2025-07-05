"""
Core services for the email agent.
"""

from .email_processor import EmailProcessor
from .memory_manager import MemoryManager
from .response_generator import ResponseGenerator
from .sender_info_extractor import SenderInfoExtractor

__all__ = ['EmailProcessor', 'MemoryManager', 'ResponseGenerator', 'SenderInfoExtractor']
