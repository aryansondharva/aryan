# services/voice_changer.py
import requests
from typing import Dict, Any
from config import MURF_API_KEY
from murf import Murf
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Ensure uploads folder exists
UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# Voice personas with their characteristics
VOICE_PERSONAS = {
    "shinchan": {
        "voice_id": "en-US-davis",  # Child-like voice
        "style": "Excited",
        "speed": "1.2",
        "pitch": "high",
        "description": "Playful, energetic child-like voice like Shinchan"
    },
    "robot": {
        "voice_id": "en-US-ken", 
        "style": "Newscaster",
        "speed": "0.9",
        "pitch": "medium",
        "description": "Mechanical, robotic voice"
    },
    "deep_voice": {
        "voice_id": "en-US-clint",
        "style": "Conversational", 
        "speed": "0.8",
        "pitch": "low",
        "description": "Deep, authoritative voice"
    },
    "normal": {
        "voice_id": "en-US-natalie",
        "style": "Conversational",
        "speed": "1.0", 
        "pitch": "medium",
        "description": "Standard conversational voice"
    },
    "girl": {
        "voice_id": "en-US-aria",
        "style": "Cheerful",
        "speed": "1.1",
        "pitch": "high",
        "description": "Sweet, cheerful girl voice"
    }
}

# Language-specific voice mappings
LANGUAGE_VOICES = {
    "japanese": {
        "shinchan": "ja-JP-kenji",
        "robot": "ja-JP-ayumi", 
        "deep_voice": "ja-JP-kenji",
        "normal": "ja-JP-ayumi",
        "girl": "ja-JP-ayumi"
    },
    "spanish": {
        "shinchan": "es-ES-alvaro",
        "robot": "es-ES-elvira",
        "deep_voice": "es-ES-alvaro", 
        "normal": "es-ES-elvira",
        "girl": "es-ES-elvira"
    },
    "french": {
        "shinchan": "fr-FR-antoine",
        "robot": "fr-FR-brigitte",
        "deep_voice": "fr-FR-antoine",
        "normal": "fr-FR-brigitte",
        "girl": "fr-FR-brigitte"
    },
    "german": {
        "shinchan": "de-DE-bernd",
        "robot": "de-DE-claudia",
        "deep_voice": "de-DE-bernd",
        "normal": "de-DE-claudia",
        "girl": "de-DE-claudia"
    },
    "english": {
        "shinchan": "en-US-davis",
        "robot": "en-US-ken",
        "deep_voice": "en-US-clint", 
        "normal": "en-US-natalie",
        "girl": "en-US-aria"
    },
    "hindi": {
        "shinchan": "hi-IN-madhur",
        "robot": "hi-IN-swara",
        "deep_voice": "hi-IN-madhur",
        "normal": "hi-IN-swara",
        "girl": "hi-IN-swara"
    }
}

def get_voice_for_language_and_persona(language: str, persona: str) -> str:
    """Get appropriate voice ID for language and persona combination."""
    language = language.lower()
    persona = persona.lower()
    
    # Default to English if language not supported
    if language not in LANGUAGE_VOICES:
        language = "english"
    
    # Default to normal if persona not found
    if persona not in LANGUAGE_VOICES[language]:
        persona = "normal"
    
    return LANGUAGE_VOICES[language][persona]

def apply_voice_effects(text: str, persona: str, language: str = "english", output_file: str = "voice_output.wav") -> bytes:
    """
    Apply voice effects based on persona and language.
    
    Args:
        text: Text to convert to speech
        persona: Voice persona ('shinchan', 'robot', 'deep_voice', 'normal')
        language: Target language for speech
        output_file: Output file name
    
    Returns:
        Audio bytes
    """
    try:
        if not MURF_API_KEY:
            raise Exception("MURF_API_KEY not configured.")
        
        client = Murf(api_key=MURF_API_KEY)
        file_path = UPLOADS_DIR / output_file
        
        # Get voice ID for language and persona
        voice_id = get_voice_for_language_and_persona(language, persona)
        
        # Get persona settings
        persona_settings = VOICE_PERSONAS.get(persona.lower(), VOICE_PERSONAS["normal"])
        
        # Clean file
        open(file_path, "wb").close()
        
        # Generate speech with persona effects
        res = client.text_to_speech.stream(
            text=text,
            voice_id=voice_id,
            style=persona_settings["style"]
        )
        
        audio_bytes = b""
        for audio_chunk in res:
            audio_bytes += audio_chunk
            with open(file_path, "ab") as f:
                f.write(audio_chunk)
        
        logger.info(f"Generated {persona} voice in {language} for text: {text[:50]}...")
        return audio_bytes
        
    except Exception as e:
        logger.error(f"Voice generation error: {e}")
        # Fallback to normal voice
        return generate_fallback_voice(text, output_file)

def generate_fallback_voice(text: str, output_file: str = "fallback_output.wav") -> bytes:
    """Generate fallback voice when main generation fails."""
    try:
        client = Murf(api_key=MURF_API_KEY)
        file_path = UPLOADS_DIR / output_file
        
        open(file_path, "wb").close()
        
        res = client.text_to_speech.stream(
            text=text,
            voice_id="en-US-natalie",
            style="Conversational"
        )
        
        audio_bytes = b""
        for audio_chunk in res:
            audio_bytes += audio_chunk
            with open(file_path, "ab") as f:
                f.write(audio_chunk)
        
        return audio_bytes
        
    except Exception as e:
        logger.error(f"Fallback voice generation failed: {e}")
        return b""

def get_available_personas() -> Dict[str, Any]:
    """Return available voice personas with descriptions."""
    return {
        persona: {
            "description": data["description"],
            "supported_languages": list(LANGUAGE_VOICES.keys())
        }
        for persona, data in VOICE_PERSONAS.items()
    }

def get_supported_languages_for_voices() -> Dict[str, list]:
    """Return supported languages for voice generation."""
    return {
        "languages": list(LANGUAGE_VOICES.keys()),
        "personas": list(VOICE_PERSONAS.keys())
    }
