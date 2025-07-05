"""
User profile management for extracting and managing user information.
"""

from typing import Dict, Any, Optional
from config.agent_config import AI_AGENT_CONFIG


class UserProfile:
    """Manages user profile information."""
    
    def __init__(self, email_handler):
        self.email_handler = email_handler
        self._user_profile = None
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get user information from profile or defaults."""
        if self._user_profile is None and hasattr(self.email_handler, 'user_profile'):
            self._user_profile = self.email_handler.user_profile
        
        # Extract name from email if available
        email = ""
        name = "Assistant"  # Default fallback
        
        if self._user_profile:
            email = self._user_profile.get('emailAddress', '')
            
            # Extract name from email with better logic
            if email:
                name_part = email.split('@')[0]  # Get part before @
                
                # Handle specific case: florezjnicolas@gmail.com
                if 'florezjnicolas' in name_part.lower():
                    name = "Nicolas Florez"
                elif 'florez' in name_part.lower() and 'nicolas' in name_part.lower():
                    name = "Nicolas Florez"
                elif 'nicolas' in name_part.lower() and 'florez' in name_part.lower():
                    name = "Nicolas Florez"
                # General patterns for other emails
                elif '.' in name_part:
                    # Handle firstname.lastname format
                    parts = name_part.split('.')
                    name = ' '.join(part.capitalize() for part in parts)
                else:
                    # Handle firstnamelastname format - try to split common names
                    name_lower = name_part.lower()
                    if 'nicolas' in name_lower:
                        # Extract Nicolas and try to find surname
                        if name_lower.startswith('nicolas'):
                            surname = name_lower.replace('nicolas', '')
                            name = f"Nicolas {surname.capitalize()}" if surname else "Nicolas"
                        else:
                            name = "Nicolas"
                    else:
                        # Default: capitalize the whole thing
                        name = name_part.capitalize()
        
        return {
            'name': name,
            'email': email,
            'role': AI_AGENT_CONFIG["user_info"]["default_role"]
        }
    
    def display_profile(self):
        """Display user profile using email handler."""
        if hasattr(self.email_handler, 'display_profile'):
            self.email_handler.display_profile()
    
    def update_profile(self, profile_data: Dict[str, Any]):
        """Update user profile."""
        self._user_profile = profile_data
