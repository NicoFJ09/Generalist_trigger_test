from dotenv import load_dotenv
import os
from pydantic import SecretStr

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_file = os.path.join(project_root, ".env.local")

# Load environment variables from .env.local
load_dotenv(dotenv_path=env_file)

# API Keys with default fallback to force non-None type
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY", "")
GMAIL_INTEGRATION_ID = os.getenv("GMAIL_INTEGRATION_ID", "")
_openai_api_key = os.getenv("OPENAI_API_KEY", "")

# Validation
if not COMPOSIO_API_KEY:
    raise ValueError("COMPOSIO_API_KEY not found in environment variables")
if not GMAIL_INTEGRATION_ID:
    raise ValueError("GMAIL_INTEGRATION_ID not found in environment variables")
if not _openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Convert OpenAI API key to SecretStr for ChatOpenAI compatibility
OPENAI_API_KEY = SecretStr(_openai_api_key)