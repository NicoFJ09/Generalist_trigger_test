"""
Simple AI Agent for email processing with memory and human oversight.
"""

import sys
import os
import json
from typing import Dict, Any, Optional
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from config.agent_config import AI_AGENT_CONFIG, MEMORY_CONFIG
from rich.console import Console
from rich.panel import Panel


class EmailAIAgent:
    """Simple AI Agent for processing emails with memory and human oversight."""
    
    def __init__(self, email_handler):
        self.email_handler = email_handler
        self.console = Console()
        self.model = ChatOpenAI(
            model=AI_AGENT_CONFIG["model"],
            temperature=AI_AGENT_CONFIG["temperature"],
            max_completion_tokens=AI_AGENT_CONFIG["max_tokens"]
        )
        
        # In-memory storage for this session only
        self.email_memory = {}  # sender -> list of emails
        self.processed_threads = set()  # Track processed thread IDs
        self.sender_info = {}  # sender -> extracted info (name, age, etc.)
        self.user_profile = None  # Will be set from email_handler
    
    def add_to_memory(self, sender: str, email_text: str, thread_id: str, response: Optional[str] = None):
        """Add email to memory and extract sender information."""
        if sender not in self.email_memory:
            self.email_memory[sender] = []
        
        # Extract information from email if enabled
        if MEMORY_CONFIG["extract_sender_info"]:
            self.extract_sender_info(sender, email_text)
        
        self.email_memory[sender].append({
            "email": email_text[:MEMORY_CONFIG.get("max_email_length", 1000)],
            "thread_id": thread_id,
            "response": response or ""
        })
        
        # Keep only last N emails per sender
        max_emails = MEMORY_CONFIG["max_emails_per_sender"]
        if len(self.email_memory[sender]) > max_emails:
            self.email_memory[sender] = self.email_memory[sender][-max_emails:]
    
    def extract_sender_info(self, sender: str, email_text: str):
        """Extract information about the sender using a simple approach."""
        if sender not in self.sender_info:
            self.sender_info[sender] = {}
        
        # Use simple AI extraction with fallback to basic patterns
        try:
            extracted_info = self.simple_ai_extract(email_text)
            if extracted_info:
                # Merge new information with existing
                self.sender_info[sender].update(extracted_info)
                
                # Show what was learned in a simple format
                if extracted_info:
                    details = []
                    for key, value in extracted_info.items():
                        details.append(f"{key}: {value}")
                    
                    details_str = ", ".join(details)
                    self.console.print(f"💡 Learned key details about sender: {details_str}")
        except Exception as e:
            self.console.print(f"⚠️ Could not extract sender info: {e}")
            # Fallback to basic extraction
            self.basic_extract_info(sender, email_text)
    
    def simple_ai_extract(self, email_text: str) -> dict:
        """Simple AI extraction with robust error handling."""
        try:
            # Create a simple prompt
            prompt = f"""
Extract key information from this email. Return a simple list of key-value pairs.
Only extract information that is clearly mentioned. 

Examples:
- If they say "My name is John", extract: name: John
- If they say "I'm 25 years old", extract: age: 25  
- If they say "I work at Google", extract: company: Google

Email: {email_text}

Extract information in this format - one per line:
name: [if mentioned]
age: [if mentioned]
company: [if mentioned]
location: [if mentioned]
job_title: [if mentioned]
interest: [if mentioned]

Only include lines for information that is actually mentioned in the email.
"""
            
            # Use the main model for extraction
            messages = [HumanMessage(content=prompt)]
            response = self.model.invoke(messages)
            response_text = str(response.content).strip()
            
            # Parse the simple format
            extracted = {}
            lines = response_text.split('\n')
            
            for line in lines:
                line = line.strip()
                if ':' in line and not line.startswith('#') and not line.startswith('-'):
                    try:
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        # Only add if value is meaningful
                        if value and value.lower() not in ['[if mentioned]', 'not mentioned', 'none', 'n/a', '']:
                            extracted[key] = value
                    except:
                        continue
            
            return extracted
            
        except Exception as e:
            self.console.print(f"⚠️ Simple AI extraction failed: {e}")
            return {}
    
    def basic_extract_info(self, sender: str, email_text: str):
        """Basic extraction using simple string matching."""
        # Ensure sender info is properly initialized
        if sender not in self.sender_info:
            self.sender_info[sender] = {}
            
        extracted = {}
        email_lower = email_text.lower()
        
        # Simple patterns - just look for common phrases
        patterns = {
            'name': ['my name is ', "i'm ", 'i am ', 'call me '],
            'age': [' years old', 'age is ', "i'm "],
            'company': ['work at ', 'from ', 'company '],
            'location': ['based in ', 'from ', 'live in ']
        }
        
        for info_type, phrases in patterns.items():
            for phrase in phrases:
                if phrase in email_lower:
                    # Find the phrase and extract what comes after
                    start = email_lower.find(phrase) + len(phrase)
                    # Take next 20 characters and clean up
                    value = email_text[start:start+20].split('.')[0].split(',')[0].split('\n')[0].strip()
                    
                    if value and len(value) > 1:
                        if info_type == 'age':
                            # Extract just numbers for age
                            import re
                            age_match = re.search(r'\d+', value)
                            if age_match:
                                extracted[info_type] = age_match.group()
                        else:
                            extracted[info_type] = value.title()
                        break
        
        if extracted:
            # Safely update sender info
            self.sender_info[sender].update(extracted)
            details = ", ".join([f"{k}: {v}" for k, v in extracted.items()])
            self.console.print(f"💡 Learned key details about sender: {details}")
    
    def ai_extract_info(self, email_text: str) -> dict:
        """Use AI to extract sender information from email."""
        ai_config = MEMORY_CONFIG.get("ai_extraction", {})
        prompt = ai_config.get("extraction_prompt", "").format(email_text=email_text)
        
        try:
            # Create a separate model instance for extraction with low temperature
            extraction_model = ChatOpenAI(
                model=ai_config.get("model", "gpt-4o-mini"),
                temperature=ai_config.get("temperature", 0.1),
                max_completion_tokens=500
            )
            
            messages = [HumanMessage(content=prompt)]
            response = extraction_model.invoke(messages)
            
            # Try to parse JSON response
            response_text = str(response.content).strip()
            
            # Clean up response - remove markdown, extra whitespace, etc.
            if "```json" in response_text:
                # Extract JSON from markdown code block
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                if end != -1:
                    response_text = response_text[start:end].strip()
                else:
                    response_text = response_text[start:].strip()
            elif "```" in response_text:
                # Handle generic code blocks
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                if end != -1:
                    response_text = response_text[start:end].strip()
                else:
                    response_text = response_text[start:].strip()
            
            # Remove any leading/trailing whitespace and newlines
            response_text = response_text.strip()
            
            # Try to find JSON object in the response
            if not response_text.startswith("{"):
                # Look for the first { in the response
                start_idx = response_text.find("{")
                if start_idx != -1:
                    response_text = response_text[start_idx:]
            
            if not response_text.endswith("}"):
                # Look for the last } in the response
                end_idx = response_text.rfind("}")
                if end_idx != -1:
                    response_text = response_text[:end_idx + 1]
            
            # Parse JSON
            extracted_data = json.loads(response_text)
            
            # Filter out empty values and clean up
            cleaned_data = {}
            for key, value in extracted_data.items():
                if value and isinstance(value, str) and value.strip() and value.lower() not in ["not mentioned", "none", "n/a", "", "null"]:
                    cleaned_data[key] = value.strip()
            
            return cleaned_data
            
        except json.JSONDecodeError as e:
            self.console.print(f"⚠️ Could not parse AI extraction response: {e}")
            self.console.print(f"🔍 Raw response: {response_text[:100]}...")
            return {}
        except Exception as e:
            self.console.print(f"⚠️ AI extraction failed: {e}")
            return {}
    
    def extract_sender_info_regex(self, sender: str, email_text: str):
        """Fallback regex-based extraction method."""
        # Ensure sender info is properly initialized
        if sender not in self.sender_info:
            self.sender_info[sender] = {}
            
        # Legacy patterns for basic extraction
        basic_patterns = {
            "name": [r"my name is ([^,\n\.]+)", r"i'm ([^,\n\.]+)", r"i am ([^,\n\.]+)"],
            "age": [r"i am (\d+) years old", r"i'm (\d+) years old", r"(\d+) years old"],
            "company": [r"i work at ([^,\n\.]+)", r"from ([^,\n\.]+)", r"at ([^,\n\.]+)"]
        }
        
        email_lower = email_text.lower()
        extracted = {}
        
        for info_type, patterns in basic_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, email_lower)
                if match:
                    value = match.group(1).strip()
                    if info_type == "name":
                        value = value.title()
                    extracted[info_type] = value
                    break
        
        if extracted:
            # Safely update sender info
            self.sender_info[sender].update(extracted)
            extracted_str = ", ".join([f"{k}: {v}" for k, v in extracted.items()])
            self.console.print(f"💡 Learned key details about sender: {extracted_str}")
    
    def get_sender_context(self, sender: str) -> str:
        """Get context about previous interactions with this sender."""
        context = ""
        
        # Add sender information if available
        if sender in self.sender_info and self.sender_info[sender]:
            context += "Known information about sender:\n"
            for info_type, value in self.sender_info[sender].items():
                context += f"- {info_type.title()}: {value}\n"
            context += "\n"
        
        # Add previous email context
        if sender not in self.email_memory:
            context += "No previous interactions."
        else:
            context_window = MEMORY_CONFIG["context_window"]
            recent_emails = self.email_memory[sender][-context_window:]
            context += f"Previous {len(recent_emails)} emails from {sender}:\n"
            for i, email in enumerate(recent_emails, 1):
                context += f"{i}. {email['email'][:100]}...\n"
        
        return context
    
    def process_incoming_email(self, sender: str, email_text: str, thread_id: str):
        """Process incoming email and handle response."""
        try:
            # Check if we already processed this thread
            if thread_id in self.processed_threads:
                self.console.print(f"🔄 Already processed thread {thread_id}, skipping...")
                return
            
            # Mark as processed immediately to prevent duplicates
            self.processed_threads.add(thread_id)
            
            sender_email = self.parse_sender_email(sender)
            self.console.print(f"\n📧 Processing email from {sender_email} (Thread: {thread_id})")
            
            # Add to memory (this also extracts sender info)
            self.add_to_memory(sender, email_text, thread_id)
            
            # Get context
            context = self.get_sender_context(sender)
            
            # Generate response
            self.console.print(f"🤖 Generating response...")
            response = self.generate_response(sender, email_text, context)
            
            # Show response and ask for approval directly - this will pause any CLI activity
            self.show_response_for_approval(sender, sender_email, email_text, response, thread_id, context)
            
        except Exception as e:
            self.console.print(f"❌ Error processing email: {e}")
            # Remove from processed threads if there was an error
            self.processed_threads.discard(thread_id)
    
    def show_response_for_approval(self, sender: str, sender_email: str, email_text: str, response: str, thread_id: str, context: str):
        """Display the generated response for user approval - simplified."""
        
        # Display email content
        email_panel = Panel(
            email_text,
            title=f"📧 Email from {sender_email}",
            border_style="blue"
        )
        self.console.print(email_panel)
        
        # Display generated response
        response_panel = Panel(
            response,
            title="🤖 Generated Response",
            border_style="green"
        )
        self.console.print(response_panel)
        
        # Force flush to ensure panels are displayed immediately
        sys.stdout.flush()
        
        # Simple approval question
        while True:
            try:
                answer = input("\n💡 Send this response? [y/n]: ").strip().lower()
                
                if answer in ['y', 'yes']:
                    self.console.print("📤 Sending response...")
                    success = self.send_response(sender_email, response, thread_id, sender, email_text)
                    if success:
                        self.console.print("✅ Response sent successfully!")
                    else:
                        self.console.print("❌ Failed to send response")
                    break
                elif answer in ['n', 'no']:
                    self.console.print("❌ Response cancelled")
                    break
                else:
                    self.console.print("❌ Please answer 'y' for yes or 'n' for no")
                    continue
                    
            except KeyboardInterrupt:
                self.console.print("\n❌ Response cancelled")
                break
            except Exception as e:
                self.console.print(f"❌ Error reading input: {e}")
                self.console.print("❌ Response cancelled")
                break
        
        # Show CLI prompt immediately after completion
        print("Command> ", end="")
        sys.stdout.flush()
    
    def send_response(self, sender_email: str, response: str, thread_id: str, sender: str, email_text: str):
        """Send the response email."""
        try:
            self.console.print(f"📧 Sending to: {sender_email}")
            self.console.print(f"🔗 Thread ID: {thread_id}")
            
            success = self.email_handler.reply_to_thread(
                recipient_email=sender_email,
                message_text=response,
                thread_id=thread_id
            )
            
            if success:
                # Update memory with the response
                self.add_to_memory(sender, email_text, thread_id, response)
                self.console.print(f"💾 Updated memory for {sender_email}")
                
            return success
            
        except Exception as e:
            self.console.print(f"❌ Error sending response: {e}")
            return False
    
    def generate_response(self, sender: str, email_text: str, context: str) -> str:
        """Generate AI response using user profile and context."""
        # Get user information
        user_info = self.get_user_info()
        
        prompt = f"""You are {user_info['name']} responding to an email from your {user_info['email']} account.

{AI_AGENT_CONFIG['system_prompt']}

Your information:
- Name: {user_info['name']}
- Email: {user_info['email']}
- Role: {user_info.get('role', 'Professional')}

Email from: {sender}
Content: {email_text}

Context about sender:
{context}

Write a personal, helpful response as {user_info['name']}. Address any specific questions or information mentioned in the email (like names, ages, etc.). Be natural and conversational."""
        
        try:
            messages = [HumanMessage(content=prompt)]
            response = self.model.invoke(messages)
            return str(response.content)
        except Exception as e:
            return f"Thank you for your email. I appreciate you reaching out and will get back to you soon.\n\nBest regards,\n{user_info['name']}"
    
    def get_user_info(self) -> dict:
        """Get user information from profile or defaults."""
        if self.user_profile is None and hasattr(self.email_handler, 'user_profile'):
            self.user_profile = self.email_handler.user_profile
        
        # Extract name from email if available
        email = ""
        name = "Assistant"  # Default fallback
        
        if self.user_profile:
            email = self.user_profile.get('emailAddress', '')
            
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
    
    def parse_sender_email(self, sender_email: str) -> str:
        """
        The sender email is expected to be in the format "Name <email>"
        This function extracts the email part.
        """
        if "<" in sender_email and ">" in sender_email:
            return sender_email.split("<")[1].split(">")[0].strip()
        return sender_email.strip()
    
    def validate_sender_info(self, sender: str):
        """Validate and clean sender info to ensure it's in the correct format."""
        if sender not in self.sender_info:
            self.sender_info[sender] = {}
            return
            
        # Check if sender_info is a dictionary
        if not isinstance(self.sender_info[sender], dict):
            self.console.print(f"⚠️ Fixing invalid sender info format for {sender}")
            self.sender_info[sender] = {}
            return
            
        # Check each value in the dictionary
        cleaned_info = {}
        for key, value in self.sender_info[sender].items():
            if isinstance(value, (str, int, float)):
                # Valid types
                cleaned_info[key] = value
            elif isinstance(value, (list, tuple)):
                # Convert lists/tuples to strings
                if value:
                    cleaned_info[key] = str(value[0]) if len(value) > 0 else ""
            else:
                # Convert other types to string
                cleaned_info[key] = str(value)
        
        self.sender_info[sender] = cleaned_info
