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
    "auto_reply": False,  # Changed to require approval
    "system_prompt": """
You are responding to emails as the Gmail account owner. Be personal, professional, and helpful.

Key instructions:
- Use the account owner's information when responding
- Address specific details mentioned in the email (names, ages, questions, etc.)
- Reference previous conversations when relevant
- Be conversational but professional
- Don't use placeholders - respond as yourself
- Provide specific, helpful information
""",
    "user_info": {
        "extract_from_profile": True,
        "default_name": "Nicolas Florez",
        "default_role": "Professional Email Assistant"
    },
    "assistant_context": {
        "role": "AI Email Assistant",
        "description": "You are an intelligent email assistant working for Nicolas Florez. You help with email management, responses, and communication tasks. You have access to email memory, sender information, and conversation history.",
        "capabilities": [
            "Generate personalized email responses",
            "Remember sender information across conversations",
            "Provide email management advice",
            "Help with communication tasks",
            "Extract and use context from previous emails",
            "Maintain professional correspondence"
        ]
    }
}

# Email Processing Configuration
EMAIL_CONFIG = {
    "max_email_length": 10000,
    "include_original_message": True,
    "reply_delay_seconds": 2,
    "enable_thread_context": True,
    "max_retry_attempts": 3,
    "require_approval": True  # Require approval before sending
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

# Memory and Context Configuration
MEMORY_CONFIG = {
    "max_emails_per_sender": 10,
    "context_window": 3,  # Number of previous emails to include in context
    "extract_sender_info": True,  # Extract key details about senders using AI
    "ai_extraction": {
        "enabled": True,
        "model": "gpt-4o-mini",
        "temperature": 0.1,  # Low temperature for consistent extraction
        "extraction_categories": [
            "name",           # Full name of the person
            "age",            # Age in years
            "company",        # Company or organization they work for
            "job_title",      # Their role or position
            "location",       # City, country, or region they're based in
            "phone",          # Phone number if mentioned
            "interest",       # What they're interested in or looking for
            "education",      # University, degree, or educational background
            "experience",     # Years of experience or expertise area
            "project",        # Current projects they're working on
            "expertise",      # Skills or areas of expertise
            "goal"           # What they want to achieve or their objective
        ],
        "extraction_prompt": """
Extract key information about the sender from this email. Return ONLY a valid JSON object with the information that is explicitly mentioned in the email. Do not infer or assume anything.

IMPORTANT: 
- Return ONLY the JSON object, no other text
- Do not use markdown formatting or code blocks
- Only include fields that have actual information from the email
- If no relevant information is found, return an empty JSON object: {}

Example format:
{"name": "John Smith", "age": "30", "company": "Google", "job_title": "Engineer"}

Available fields to extract:
- name: Full name of the person
- age: Age in years
- company: Company or organization they work for
- job_title: Their role or position
- location: City, country, or region they're based in
- phone: Phone number if mentioned
- interest: What they're interested in or looking for
- education: Educational background if mentioned
- experience: Experience details if mentioned
- project: Current projects if mentioned
- expertise: Skills or expertise if mentioned
- goal: Their objective or what they want to achieve

Email content:
{email_text}

JSON response:"""
    },
    "max_email_length": 2000  # Increased to capture more context
}
