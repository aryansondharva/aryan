# services/stt.py
import assemblyai as aai
from fastapi import UploadFile
from config import get_api_key
from assemblyai.streaming.v3 import (
    StreamingClient,
    StreamingClientOptions,
    StreamingParameters,
    StreamingSessionParameters,
    StreamingEvents,
    BeginEvent,
    TurnEvent,
    TerminationEvent,
    StreamingError,
)

# Configure API key dynamically
def _configure_assemblyai():
    api_key = get_api_key("ASSEMBLYAI_API_KEY")
    if api_key:
        aai.settings.api_key = api_key
    return api_key

# Initial configuration
_configure_assemblyai()


def _on_begin(client: StreamingClient, event: BeginEvent):
    print(f"AAI session started: {event.id}")


def _on_termination(client: StreamingClient, event: TerminationEvent):
    print(f"AAI session terminated after {event.audio_duration_seconds} s")


def _on_error(client: StreamingClient, error: StreamingError):
    print("AAI error:", error)


class AssemblyAIStreamingTranscriber:
    """
    Wrapper around AAI StreamingClient that exposes:
      - on_partial_callback(text) for interim results
      - on_final_callback(text)   when end_of_turn=True
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        on_partial_callback=None,
        on_final_callback=None,
    ):
        self.on_partial_callback = on_partial_callback
        self.on_final_callback = on_final_callback

        # Ensure API key is configured
        api_key = _configure_assemblyai()
        if not api_key:
            raise Exception("ASSEMBLYAI_API_KEY not configured")

        self.client = StreamingClient(
            StreamingClientOptions(
                api_key=api_key,
                api_host="streaming.assemblyai.com",
            )
        )

        # register events
        self.client.on(StreamingEvents.Begin, _on_begin)
        self.client.on(StreamingEvents.Error, _on_error)
        self.client.on(StreamingEvents.Termination, _on_termination)
        self.client.on(
            StreamingEvents.Turn,
            lambda client, event: self._on_turn(client, event),
        )

        self.client.connect(
            StreamingParameters(
                sample_rate=sample_rate,
                format_turns=False,
            )
        )

    def _on_turn(self, client: StreamingClient, event: TurnEvent):
        text = (event.transcript or "").strip()
        print(f"DEBUG: Turn event - text: '{text}', end_of_turn: {event.end_of_turn}")
        
        if not text:
            return

        if event.end_of_turn:
            print(f"DEBUG: Final transcript: '{text}'")
            if self.on_final_callback:
                self.on_final_callback(text)

            if not event.turn_is_formatted:
                try:
                    client.set_params(StreamingSessionParameters(format_turns=True))
                except Exception as set_err:
                    print("set_params error:", set_err)
        else:
            print(f"DEBUG: Partial transcript: '{text}'")
            if self.on_partial_callback:
                self.on_partial_callback(text)

    def stream_audio(self, audio_chunk: bytes):
        self.client.stream(audio_chunk)

    def close(self):
        self.client.disconnect(terminate=True)


def transcribe_audio(audio_file: UploadFile) -> str:
    """Transcribes audio to text using AssemblyAI."""
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file.file)

    if transcript.status == aai.TranscriptStatus.error or not transcript.text:
        raise Exception(f"Transcription failed: {transcript.error or 'No speech detected'}")

    return transcript.text


def transcribe_audio_file(audio_file_path: str) -> str:
    """Transcribes audio file from path to text using AssemblyAI."""
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path)

    if transcript.status == aai.TranscriptStatus.error or not transcript.text:
        raise Exception(f"Transcription failed: {transcript.error or 'No speech detected'}")

    return transcript.text