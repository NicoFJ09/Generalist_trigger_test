"""
Sender information extractor for learning about email senders.
"""

import re
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from config.agent_config import MEMORY_CONFIG


class SenderInfoExtractor:
    """Extracts and manages sender information from emails."""
    
    def __init__(self):
        self.extraction_enabled = MEMORY_CONFIG.get("extract_sender_info", True)
    
    def extract_sender_info(self, email_text: str) -> Dict[str, Any]:
        """Extract information about the sender from email text."""
        if not self.extraction_enabled:
            return {}
        
        # Try AI extraction first, fall back to basic if it fails
        try:
            return self._simple_ai_extract(email_text)
        except Exception:
            return self._basic_extract_info(email_text)
    
    def _simple_ai_extract(self, email_text: str) -> Dict[str, Any]:
        """Simple AI extraction with robust error handling."""
        try:
            # Get prompt from configuration
            ai_config = MEMORY_CONFIG.get("ai_extraction", {})
            prompt_template = ai_config.get("simple_extraction_prompt", "")
            prompt = prompt_template.format(email_text=email_text)
            
            # Create model for extraction
            model = ChatOpenAI(
                model=ai_config.get("model", "gpt-4o-mini"),
                temperature=ai_config.get("temperature", 0.1),
                max_completion_tokens=500
            )
            
            messages = [HumanMessage(content=prompt)]
            response = model.invoke(messages)
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
            raise Exception(f"Simple AI extraction failed: {e}")
    
    def _basic_extract_info(self, email_text: str) -> Dict[str, Any]:
        """Basic extraction using simple string matching."""
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
                            age_match = re.search(r'\d+', value)
                            if age_match:
                                extracted[info_type] = age_match.group()
                        else:
                            extracted[info_type] = value.title()
                        break
        
        return extracted