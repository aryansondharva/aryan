# config.py
import os
from dotenv import load_dotenv
import assemblyai as aai
import google.generativeai as genai
import logging
from typing import Dict, Optional

# Load environment variables from .env file
load_dotenv()

# Global API key storage (can be overridden by user input)
_api_keys = {
    "MURF_API_KEY": os.getenv("MURF_API_KEY"),
    "ASSEMBLYAI_API_KEY": os.getenv("ASSEMBLYAI_API_KEY"),
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY")
}

def set_api_keys(api_keys: Dict[str, str]):
    """Update API keys from user input."""
    global _api_keys
    for key, value in api_keys.items():
        if value and value.strip():
            _api_keys[key] = value.strip()
    
    # Reconfigure APIs with new keys
    configure_apis()

def get_api_key(key: str) -> Optional[str]:
    """Get API key by name."""
    return _api_keys.get(key)

def configure_apis():
    """Configure all APIs with current keys."""
    # Configure AssemblyAI
    if _api_keys.get("ASSEMBLYAI_API_KEY"):
        aai.settings.api_key = _api_keys["ASSEMBLYAI_API_KEY"]
    else:
        logging.warning("ASSEMBLYAI_API_KEY not configured.")
    
    # Configure Gemini AI
    if _api_keys.get("GEMINI_API_KEY"):
        genai.configure(api_key=_api_keys["GEMINI_API_KEY"])
    else:
        logging.warning("GEMINI_API_KEY not configured.")
    
    # Murf API key is accessed directly via get_api_key function
    if not _api_keys.get("MURF_API_KEY"):
        logging.warning("MURF_API_KEY not configured.")

# Legacy exports for backward compatibility
MURF_API_KEY = _api_keys["MURF_API_KEY"]
ASSEMBLYAI_API_KEY = _api_keys["ASSEMBLYAI_API_KEY"]
GEMINI_API_KEY = _api_keys["GEMINI_API_KEY"]

# Initial configuration
configure_apis()