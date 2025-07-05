#!/usr/bin/env python3
"""
Gmail Profile Fetcher using Composio's toolset.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mail.email_handler import EmailHandler
from config.settings import GMAIL_INTEGRATION_ID


def main():
    """
    Main function to authenticate and fetch Gmail profile.
    """
    print("🚀 Gmail Profile Fetcher - Composio Integration")
    print("=" * 50)
    
    # Configuration
    integration_id = GMAIL_INTEGRATION_ID
    user_id = "gmail_user_1"
    
    try:
        # Initialize the email handler
        print("🔧 Initializing Gmail connection...")
        email_handler = EmailHandler(integration_id, user_id)
        
        # Display the user's profile
        email_handler.display_profile()
        
        # Get user email
        user_email = email_handler.get_user_email()
        if user_email:
            print(f"\n✅ Successfully authenticated Gmail account: {user_email}")
        else:
            print("\n⚠️  Could not retrieve user email")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure your environment variables are set correctly")
        print("💡 Check that your Composio integration ID is valid")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
