# main.py
from fastapi import FastAPI, Request, WebSocket, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import logging
import asyncio
import base64
import re

# Import services and config
import config
from services import stt, llm, tts
from services.data_processor import data_processor
from services.translator import translate_text, get_supported_languages
from services.voice_changer import apply_voice_effects, get_available_personas
from personas import get_persona, get_available_personas as get_persona_list, get_persona_display_info

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Mount static files for CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    """Serves the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/multilingual-voice-agent")
async def multilingual_voice_agent_page(request: Request):
    """Serves the Multilingual Voice Agent page."""
    return templates.TemplateResponse("multilingual_voice_agent.html", {"request": request})


@app.get("/persona-voice-agent")
async def persona_voice_agent_page(request: Request):
    """Serves the Persona Voice Agent page."""
    return templates.TemplateResponse("persona_voice_agent.html", {"request": request})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload and process data."""
    try:
        # Validate file type
        allowed_extensions = {'.csv', '.pdf', '.xlsx', '.xls'}
        file_extension = file.filename.split('.')[-1].lower()
        
        if f'.{file_extension}' not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Process file
        result = data_processor.process_file(file_content, file.filename)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Generate AI insights
        insights = llm.analyze_data_with_llm(result)
        result["ai_insights"] = insights
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connection for real-time transcription and voice response."""
    await websocket.accept()
    logging.info("WebSocket client connected.")

    loop = asyncio.get_event_loop()
    chat_history = []

    async def handle_transcript(text: str):
        """Processes the final transcript, gets LLM and TTS responses, and streams audio."""
        await websocket.send_json({"type": "final", "text": text})
        try:
            # Get data context if available
            data_context = data_processor.get_analysis_context()
            
            # 1. Get the full text response from the LLM (non-streaming)
            full_response, updated_history = llm.get_llm_response(text, chat_history, data_context)
            
            # Update history for the next turn
            chat_history.clear()
            chat_history.extend(updated_history)

            # Send the full text response to the UI
            await websocket.send_json({"type": "assistant", "text": full_response})

            # 2. Split the response into sentences
            sentences = re.split(r'(?<=[.?!])\s+', full_response.strip())
            
            # 3. Process each sentence for TTS and stream audio back
            for sentence in sentences:
                if sentence.strip():
                    # Run the blocking TTS function in a separate thread
                    audio_bytes = await loop.run_in_executor(
                        None, tts.speak, sentence.strip()
                    )
                    if audio_bytes:
                        b64_audio = base64.b64encode(audio_bytes).decode('utf-8')
                        await websocket.send_json({"type": "audio", "b64": b64_audio})

        except Exception as e:
            logging.error(f"Error in LLM/TTS pipeline: {e}")
            await websocket.send_json({"type": "llm", "text": "Sorry, I encountered an error."})


    def on_final_transcript(text: str):
        logging.info(f"Final transcript received: {text}")
        asyncio.run_coroutine_threadsafe(handle_transcript(text), loop)

    transcriber = None
    try:
        transcriber = stt.AssemblyAIStreamingTranscriber(on_final_callback=on_final_transcript)
        
        while True:
            data = await websocket.receive_bytes()
            transcriber.stream_audio(data)
    except Exception as e:
        logging.info(f"WebSocket connection closed: {e}")
    finally:
        if transcriber:
            transcriber.close()
        logging.info("Transcription resources released.")


@app.websocket("/ws/persona")
async def persona_websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connection for persona-based real-time transcription and voice response."""
    await websocket.accept()
    logging.info("Persona WebSocket client connected.")

    loop = asyncio.get_event_loop()
    chat_history = []
    current_persona = "girl"  # Default persona

    async def handle_transcript(text: str):
        """Processes the final transcript with persona-based response."""
        await websocket.send_json({"type": "final", "text": text})
        try:
            # Get persona configuration
            persona_config = get_persona(current_persona)
            
            # Get data context if available
            data_context = data_processor.get_analysis_context()
            
            # Get persona-based LLM response
            full_response, updated_history = llm.get_persona_response(
                text, chat_history, data_context, persona_config
            )
            
            # Update history for the next turn
            chat_history.clear()
            chat_history.extend(updated_history)

            # Send the full text response to the UI
            await websocket.send_json({"type": "assistant", "text": full_response})

            # Split the response into sentences and generate audio
            sentences = re.split(r'(?<=[.?!])\s+', full_response.strip())
            
            for sentence in sentences:
                if sentence.strip():
                    audio_bytes = await loop.run_in_executor(
                        None, tts.speak, sentence.strip()
                    )
                    if audio_bytes:
                        b64_audio = base64.b64encode(audio_bytes).decode('utf-8')
                        await websocket.send_json({"type": "audio", "b64": b64_audio})

        except Exception as e:
            logging.error(f"Error in persona LLM/TTS pipeline: {e}")
            await websocket.send_json({"type": "assistant", "text": "Sorry, I encountered an error."})

    def on_final_transcript(text: str):
        logging.info(f"Persona final transcript received: {text}")
        asyncio.run_coroutine_threadsafe(handle_transcript(text), loop)

    transcriber = None
    try:
        transcriber = stt.AssemblyAIStreamingTranscriber(on_final_callback=on_final_transcript)
        
        while True:
            message = await websocket.receive()
            
            if message['type'] == 'websocket.receive':
                if 'bytes' in message:
                    # Audio data
                    transcriber.stream_audio(message['bytes'])
                elif 'text' in message:
                    # Configuration message
                    try:
                        config_data = json.loads(message['text'])
                        if config_data.get('type') == 'persona_config':
                            current_persona = config_data.get('persona', 'girl')
                            logging.info(f"Persona switched to: {current_persona}")
                    except json.JSONDecodeError:
                        logging.warning("Invalid JSON received in persona websocket")
                        
    except Exception as e:
        logging.info(f"Persona WebSocket connection closed: {e}")
    finally:
        if transcriber:
            transcriber.close()
        logging.info("Persona transcription resources released.")


@app.post("/multilingual_voice")
async def multilingual_voice_agent(request: Request):
    """Handle multilingual voice agent requests."""
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        target_language = data.get("target_language", "japanese").lower()
        persona = data.get("persona", "normal").lower()
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Step 1: Translate the text
        translation_result = translate_text(text, target_language)
        
        if not translation_result.get("success"):
            raise HTTPException(status_code=400, detail=translation_result.get("error"))
        
        translated_text = translation_result["translated_text"]
        
        # Step 2: Generate voice with persona
        audio_bytes = apply_voice_effects(
            text=translated_text,
            persona=persona,
            language=target_language,
            output_file=f"multilingual_{persona}_{target_language}.wav"
        )
        
        if not audio_bytes:
            raise HTTPException(status_code=500, detail="Voice generation failed")
        
        # Step 3: Return response with audio
        b64_audio = base64.b64encode(audio_bytes).decode('utf-8')
        
        return JSONResponse(content={
            "success": True,
            "original_text": text,
            "translated_text": translated_text,
            "target_language": target_language,
            "persona": persona,
            "audio_url": f"/uploads/multilingual_{persona}_{target_language}.wav"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Multilingual voice agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process_voice_translation")
async def process_voice_translation(
    audio: UploadFile = File(...),
    target_language: str = "japanese",
    persona: str = "normal"
):
    """Process voice recording, transcribe, translate, and generate voice response."""
    try:
        # Save uploaded audio
        audio_content = await audio.read()
        audio_path = f"uploads/recorded_audio.wav"
        
        with open(audio_path, "wb") as f:
            f.write(audio_content)
        
        # Step 1: Transcribe audio to text
        original_text = stt.transcribe_audio_file(audio_path)
        
        if not original_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")
        
        # Step 2: Translate the text
        translation_result = translate_text(original_text, target_language)
        
        if not translation_result.get("success"):
            raise HTTPException(status_code=400, detail=translation_result.get("error"))
        
        translated_text = translation_result["translated_text"]
        
        # Step 3: Generate voice with persona
        audio_bytes = apply_voice_effects(
            text=translated_text,
            persona=persona,
            language=target_language,
            output_file=f"voice_translation_{persona}_{target_language}.wav"
        )
        
        if not audio_bytes:
            raise HTTPException(status_code=500, detail="Voice generation failed")
        
        return JSONResponse(content={
            "success": True,
            "original_text": original_text,
            "translated_text": translated_text,
            "target_language": target_language,
            "persona": persona,
            "audio_url": f"/uploads/voice_translation_{persona}_{target_language}.wav"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Voice translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat_endpoint(request: Request):
    """Handle text-based chat messages."""
    try:
        data = await request.json()
        message = data.get("message", "").strip()
        chat_id = data.get("chat_id")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Get data context if available
        data_context = data_processor.get_analysis_context()
        
        # Get LLM response
        response, _ = llm.get_llm_response(message, [], data_context)
        
        # Generate audio response
        audio_bytes = tts.speak(response)
        b64_audio = None
        if audio_bytes:
            b64_audio = base64.b64encode(audio_bytes).decode('utf-8')
        
        return JSONResponse(content={
            "success": True,
            "response": response,
            "audio": b64_audio,
            "chat_id": chat_id
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/persona_chat")
async def persona_chat_endpoint(request: Request):
    """Handle text-based chat messages with persona support."""
    try:
        data = await request.json()
        message = data.get("message", "").strip()
        persona_key = data.get("persona", "girl")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Get persona configuration
        persona_config = get_persona(persona_key)
        
        # Get data context if available
        data_context = data_processor.get_analysis_context()
        
        # Get persona-based LLM response
        response, _ = llm.get_persona_response(message, [], data_context, persona_config)
        
        # Generate audio response
        audio_bytes = tts.speak(response)
        b64_audio = None
        if audio_bytes:
            b64_audio = base64.b64encode(audio_bytes).decode('utf-8')
        
        return JSONResponse(content={
            "success": True,
            "response": response,
            "audio": b64_audio,
            "persona": persona_key
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Persona chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/multilingual-voice/config")
async def get_multilingual_config():
    """Get available languages and personas for multilingual voice agent."""
    return JSONResponse(content={
        "languages": get_supported_languages(),
        "personas": get_available_personas()
    })


@app.get("/persona-voice/config")
async def get_persona_config():
    """Get available personas for persona voice agent."""
    return JSONResponse(content={
        "personas": get_persona_display_info()
    })


@app.post("/config/api-keys")
async def update_api_keys(request: Request):
    """Update API keys from user input."""
    try:
        data = await request.json()
        api_keys = data.get("api_keys", {})
        
        # Validate required keys
        valid_keys = {"GEMINI_API_KEY", "ASSEMBLYAI_API_KEY", "MURF_API_KEY"}
        filtered_keys = {k: v for k, v in api_keys.items() if k in valid_keys}
        
        # Update configuration
        config.set_api_keys(filtered_keys)
        
        return JSONResponse(content={
            "success": True,
            "message": "API keys updated successfully",
            "configured_keys": list(filtered_keys.keys())
        })
        
    except Exception as e:
        logging.error(f"Error updating API keys: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/config/api-keys/status")
async def get_api_keys_status():
    """Get the status of configured API keys (without exposing the actual keys)."""
    try:
        status = {}
        for key in ["GEMINI_API_KEY", "ASSEMBLYAI_API_KEY", "MURF_API_KEY"]:
            api_key = config.get_api_key(key)
            status[key] = {
                "configured": bool(api_key and api_key.strip()),
                "masked_key": f"***{api_key[-4:]}" if api_key and len(api_key) > 4 else None
            }
        
        return JSONResponse(content={
            "success": True,
            "api_keys": status
        })
        
    except Exception as e:
        logging.error(f"Error getting API keys status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Add JSON import for persona websocket
import json

# Render deployment configuration
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)