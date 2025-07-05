#!/usr/bin/env python3
"""
Gmail Handler with OAuth, profile fetching, and automatic email listening.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mail.email_handler import EmailHandler
from mail.email_listener import EmailListener
from config.settings import GMAIL_INTEGRATION_ID


def main():
    """
    Main function to authenticate, fetch Gmail profile, and start email listening.
    """
    print("🚀 Gmail Handler - Composio Integration")
    print("=" * 50)
    
    # Configuration
    integration_id = GMAIL_INTEGRATION_ID
    user_id = "gmail_user_1"
    
    try:
        # Initialize email handler
        print("🔧 Initializing Gmail connection...")
        email_handler = EmailHandler(integration_id, user_id)
        
        # Display user profile
        email_handler.display_profile()
        
        # Get user email
        user_email = email_handler.get_user_email()
        if user_email:
            print(f"\n✅ Successfully authenticated Gmail account: {user_email}")
        else:
            print("\n⚠️  Could not retrieve user email")
            
        # Enable trigger and start listening automatically
        print("\n🔔 Enabling email trigger...")
        email_handler.enable_trigger()
        
        # Start listening with separate listener
        email_listener = EmailListener(email_handler)
        email_listener.start_listening()
            
    except KeyboardInterrupt:
        print("\n⏸️  Operation stopped by user")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure your environment variables are set correctly")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
