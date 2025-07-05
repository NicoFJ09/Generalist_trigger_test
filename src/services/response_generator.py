"""
Response generator for creating AI-powered email responses.
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from config.agent_config import AI_AGENT_CONFIG


class ResponseGenerator:
    """Generates AI-powered email responses."""
    
    def __init__(self):
        self.model = ChatOpenAI(
            model=AI_AGENT_CONFIG["model"],
            temperature=AI_AGENT_CONFIG["temperature"],
            max_completion_tokens=AI_AGENT_CONFIG["max_tokens"]
        )
    
    def generate_response(self, sender: str, email_text: str, context: str, user_info: Dict[str, Any]) -> str:
        """Generate AI response using user profile and context."""
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
    
    def generate_custom_response(self, prompt_text: str, user_info: Dict[str, Any], system_status: Dict[str, Any]) -> str:
        """Generate response for custom user prompts."""
        try:
            # Get assistant context from config
            assistant_info = AI_AGENT_CONFIG.get("assistant_context", {})
            
            # Add email assistant context to the prompt
            enhanced_prompt = f"""You are an {assistant_info.get('role', 'AI Email Assistant')} working for {user_info['name']} ({user_info['email']}). 
            
{assistant_info.get('description', 'You help with email management and responses.')}

Your capabilities include:
{chr(10).join(['- ' + cap for cap in assistant_info.get('capabilities', ['Email assistance'])])}

Your owner information:
- Name: {user_info['name']}
- Email: {user_info['email']}
- Role: Professional Email Assistant

Current email system status:
- Active email monitoring: {"✅ Active" if system_status.get('monitoring_active') else "❌ Inactive"}
- Remembered senders: {system_status.get('remembered_senders', 0)}
- Email threads processed: {system_status.get('processed_threads', 0)}

User question: {prompt_text}

Provide a helpful, professional response as {user_info['name']}'s email assistant. Always refer to the user as {user_info['name']}, not as generic terms like "User" or with placeholders.
"""
            
            messages = [HumanMessage(content=enhanced_prompt)]
            response = self.model.invoke(messages)
            return str(response.content)
        except Exception as e:
            return f"Error: {e}"
