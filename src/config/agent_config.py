"""
Configuration for the AI Agent behavior and responses.
"""

# AI Agent Configuration
AI_AGENT_CONFIG = {
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1000,
    "response_tone": "professional",
    "enable_memory": True,
    "auto_reply": True,
    "system_prompt": """
You are a professional AI assistant that responds to emails on behalf of the user. 
Your responses should be:
- Professional and courteous
- Clear and concise
- Helpful and informative
- Appropriate to the context of the email
- Respectful of the sender's time

When responding:
1. Acknowledge the sender's email
2. Address their main points or questions
3. Provide helpful information or next steps
4. Use a professional closing

Always maintain a helpful and professional tone.
""",
    "response_templates": {
        "general_inquiry": "Thank you for your email. I've received your message and will address your inquiry promptly.",
        "meeting_request": "Thank you for reaching out. I'd be happy to discuss the meeting details with you.",
        "business_inquiry": "Thank you for your business inquiry. I appreciate your interest and will provide you with the information you need.",
        "support_request": "Thank you for contacting us. I understand your concern and will help resolve this matter.",
        "feedback": "Thank you for your feedback. Your input is valuable and helps us improve our services."
    }
}

# Email Processing Configuration
EMAIL_CONFIG = {
    "max_email_length": 10000,
    "include_original_message": True,
    "reply_delay_seconds": 2,
    "enable_thread_context": True,
    "max_retry_attempts": 3
}

# Security and Privacy Settings
SECURITY_CONFIG = {
    "enable_content_filtering": True,
    "blocked_senders": [],
    "allowed_domains": [],  # Empty means all domains allowed
    "enable_phishing_detection": True,
    "log_conversations": True,
    "anonymize_logs": False
}
