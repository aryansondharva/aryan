# services/translator.py
import google.generativeai as genai
from typing import Dict, List
import logging
import config

logger = logging.getLogger(__name__)

def _get_configured_model():
    """Get a configured Gemini model with API key from config."""
    api_key = config.get_api_key("GEMINI_API_KEY")
    if not api_key or not api_key.strip():
        raise Exception("GEMINI_API_KEY not configured. Please set it in the configuration.")
    
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        raise Exception(f"Failed to configure Gemini model: {str(e)}")

# Supported languages with their codes
SUPPORTED_LANGUAGES = {
    "english": "en",
    "japanese": "ja", 
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "russian": "ru",
    "chinese": "zh",
    "korean": "ko",
    "hindi": "hi",
    "arabic": "ar"
}

def translate_text(text: str, target_language: str) -> Dict[str, str]:
    """
    Translate text to target language using Gemini AI.
    
    Args:
        text: Text to translate
        target_language: Target language (e.g., 'japanese', 'spanish')
    
    Returns:
        Dict with original text, translated text, and language info
    """
    try:
        if target_language.lower() not in SUPPORTED_LANGUAGES:
            return {
                "success": False,
                "error": f"Language '{target_language}' not supported. Available: {list(SUPPORTED_LANGUAGES.keys())}"
            }
        
        model = _get_configured_model()
        
        prompt = f"""
        Translate the following text to {target_language}. 
        Provide ONLY the translation, no explanations or additional text.
        
        Text to translate: "{text}"
        """
        
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            raise Exception("Empty response from Gemini API")
            
        translated_text = response.text.strip()
        
        if not translated_text:
            raise Exception("Translation returned empty text")
        
        return {
            "success": True,
            "original_text": text,
            "translated_text": translated_text,
            "source_language": "english",
            "target_language": target_language,
            "language_code": SUPPORTED_LANGUAGES[target_language.lower()]
        }
        
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return {
            "success": False,
            "error": f"Translation failed: {str(e)}"
        }

def get_supported_languages() -> List[str]:
    """Return list of supported languages."""
    return list(SUPPORTED_LANGUAGES.keys())

def detect_language(text: str) -> str:
    """
    Detect the language of input text using Gemini AI.
    
    Args:
        text: Text to analyze
    
    Returns:
        Detected language name
    """
    try:
        model = _get_configured_model()
        
        prompt = f"""
        Detect the language of this text and respond with ONLY the language name in lowercase:
        "{text}"
        
        Choose from: {', '.join(SUPPORTED_LANGUAGES.keys())}
        If unsure, respond with 'english'.
        """
        
        response = model.generate_content(prompt)
        detected_lang = response.text.strip().lower()
        
        if detected_lang in SUPPORTED_LANGUAGES:
            return detected_lang
        else:
            return "english"  # Default fallback
            
    except Exception as e:
        logger.error(f"Language detection error: {e}")
        return "english"  # Default fallback
