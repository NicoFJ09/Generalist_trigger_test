"""
Sender information extractor for learning about email senders.
"""

import json
import re
from typing import Dict, Any, Optional
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
            
            # Create model for extraction
            model = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.1,
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
    
    def _ai_extract_info(self, email_text: str) -> Dict[str, Any]:
        """Advanced AI extraction with JSON parsing (fallback method)."""
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
            raise Exception(f"Could not parse AI extraction response: {e}")
        except Exception as e:
            raise Exception(f"AI extraction failed: {e}")
    
    def _extract_sender_info_regex(self, email_text: str) -> Dict[str, Any]:
        """Fallback regex-based extraction method."""
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
        
        return extracted
