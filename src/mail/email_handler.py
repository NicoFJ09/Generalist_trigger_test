"""
Email Handler using Composio's toolset for Gmail OAuth and profile fetching.
"""

import os
import sys
from typing import Optional, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from composio_langgraph import Action, ComposioToolSet, App
from config.settings import COMPOSIO_API_KEY


class EmailHandler:
    """
    Handles Gmail OAuth authentication and profile fetching.
    """

    def __init__(self, integration_id: str, user_id: str):
        # Initialize Composio toolset and connection parameters
        self.toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
        self.integration_id = integration_id
        self.user_id = user_id
        self.entity = self.toolset.get_entity(user_id)
        self.active_connection = None
        self.user_profile = None

        # Establish connection and authenticate
        try:
            connection_request = self.initiate_connection()
            self.wait_for_activation(connection_request)
        except Exception as e:
            print(f"❌ Error connecting to Gmail: {e}")
            raise

    def initiate_connection(self):
        """Start OAuth connection process."""
        try:
            print("🔐 Initiating OAuth connection...")
            connection_request = self.toolset.initiate_connection(
                integration_id=self.integration_id,
                entity_id=self.user_id,
                app=App.GMAIL,
            )
            
            # Display OAuth URL and attempt to open browser
            if connection_request.redirectUrl:
                print(f"🌐 Please authorize the application by visiting:")
                print(f"   {connection_request.redirectUrl}")
                print("📝 Complete the OAuth flow in your browser to continue...")
                
                try:
                    import webbrowser
                    webbrowser.open(connection_request.redirectUrl)
                    print("🌐 Browser opened automatically")
                except:
                    print("💡 Please open the URL manually in your browser")
                
                return connection_request
            else:
                raise ValueError("No redirect URL received from OAuth flow")
        except Exception as e:
            print(f"❌ Error initiating connection: {e}")
            raise

    def wait_for_activation(self, connection_request, timeout=180):
        """Wait for OAuth completion and connection activation."""
        print("⏳ Waiting for user authorization and connection activation...")
        try:
            # Poll until connection is active
            self.active_connection = connection_request.wait_until_active(
                client=self.toolset.client,
                timeout=timeout,
            )

            # Fetch user profile after connection is established
            self.fetch_user_profile()
            
        except Exception as e:
            print(f"❌ Connection failed or timed out: {e}")
            raise

    def fetch_user_profile(self):
        """Fetch user profile using GMAIL_GET_PROFILE."""
        try:
            print("👤 Fetching user profile...")
            action = Action.GMAIL_GET_PROFILE
            user_info = self.toolset.execute_action(
                action=action, 
                entity_id=self.user_id, 
                params={}
            )
            
            # Parse profile data from response
            if user_info and 'data' in user_info:
                if 'response_data' in user_info['data']:
                    self.user_profile = user_info['data']['response_data']
                    email_address = self.user_profile.get('emailAddress', 'Unknown')
                    print(f"✅ Profile fetched successfully!")
                    print(f"📧 Email: {email_address}")
                elif 'successful' in user_info['data'] and user_info['data']['successful']:
                    profile_data = user_info['data'].get('data', {})
                    self.user_profile = profile_data
                    email_address = profile_data.get('emailAddress', 'Unknown')
                    print(f"✅ Profile fetched successfully!")
                    print(f"📧 Email: {email_address}")
                else:
                    print("⚠️  Warning: Profile data structure is unexpected")
                    print(f"Response structure: {user_info['data'].keys()}")
                    self.user_profile = user_info['data']
            else:
                print("❌ No profile data received")
                
        except Exception as e:
            print(f"❌ Error fetching user profile: {e}")
            raise
        
    def get_user_profile(self) -> Optional[Dict[str, Any]]:
        """Return the complete user profile information."""
        return self.user_profile

    def display_profile(self):
        """Display user profile information in formatted output."""
        if not self.user_profile:
            print("❌ No profile data available")
            return
            
        print("\n" + "="*50)
        print("👤 GMAIL PROFILE")
        print("="*50)
        
        email = self.user_profile.get('emailAddress', 'Unknown')
        messages_total = self.user_profile.get('messagesTotal', 'Unknown')
        threads_total = self.user_profile.get('threadsTotal', 'Unknown')
        history_id = self.user_profile.get('historyId', 'Unknown')
        
        print(f"📧 Email Address: {email}")
        print(f"💬 Total Messages: {messages_total}")
        print(f"🧵 Total Threads: {threads_total}")
        print(f"🔄 History ID: {history_id}")
        print("="*50)

    def enable_trigger(self):
        """Enable the Gmail trigger for new messages."""
        try:
            res = self.entity.enable_trigger(
                app=App.GMAIL, 
                trigger_name="GMAIL_NEW_GMAIL_MESSAGE", 
                config={}
            )
            if res["status"] != "success":
                raise Exception(f"Failed to enable trigger: {res['message']}")
            print("✅ Email trigger enabled successfully")
        except Exception as e:
            print(f"❌ Error enabling trigger: {e}")
            raise

    def reply_to_thread(self, recipient_email: str, message_text: str, thread_id: str):
        """Reply to a Gmail thread."""
        try:
            action = Action.GMAIL_REPLY_TO_THREAD
            response = self.toolset.execute_action(
                action=action,
                entity_id=self.user_id,
                params={
                    "recipient_email": recipient_email,
                    "message_body": message_text,
                    "thread_id": thread_id,
                },
            )
            return True
            
        except Exception as e:
            print(f"❌ Error replying to thread: {e}")
            return False
