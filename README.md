# 🚀 N9NE-AI 

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-green.svg)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
[![Murf AI](https://img.shields.io/badge/Murf%20AI-Voice%20Synthesis-orange.svg)](https://murf.ai/)

A sophisticated **AI-powered conversational platform** that combines intelligent data analysis, multilingual voice translation, and persona-based voice interactions. Upload documents, analyze data, and interact through voice with customizable AI personas including anime characters like Nobita and Shinchan.

## 📋 Table of Contents

- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Configuration](#️-configuration)
- [📁 Project Structure](#-project-structure)
- [🎯 Usage Guide](#-usage-guide)
- [🌐 API Endpoints](#-api-endpoints)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

### 🎯 Core Capabilities
- **📊 Intelligent Data Analysis**
  - Upload and analyze CSV, PDF, or Excel files
  - AI-powered insights using Google Gemini
  - Interactive data exploration through natural language
  - Real-time business intelligence and trend analysis

- **🎤 Real-time Voice Interaction**
  - Advanced speech-to-text using AssemblyAI streaming
  - High-quality text-to-speech with Murf AI
  - WebSocket-based low-latency communication
  - Voice activity detection and audio processing

- **🌍 Multilingual Support**
  - Real-time translation between 12+ languages
  - Support for English, Japanese, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Korean, Hindi, Arabic
  - Cultural context awareness in translations
  - Language detection capabilities

- **🎭 AI Persona System**
  - **Nobita**: Tired student character with authentic anime personality
  - **Shinchan**: Mischievous 5-year-old with playful responses
  - **Friendly Girl**: Sweet and helpful conversational partner
  - Unique voice characteristics and response patterns for each persona

### 🎬 Example Interactions

**Data Analysis Flow:**
```
👤 User: "Analyze this sales report."
🤖 Kiya: "Your sales grew by 18% in Q2, with the highest increase in North America."
👤 User: "Which region performed worst?"
🤖 Kiya: "Europe saw a 5% decline in sales this quarter."
```

**Persona Interaction (Nobita):**
```
👤 User: "What is 2+2?"
😴 Nobita: "Ugh, I'm so tired of math problems! Doraemon, where are you? 
          I need your calculator gadget! *sigh* But I guess I have to do 
          this myself... 2 plus 2 equals 4. There, I answered it! 
          Can I take a nap now?"
```

**Multilingual Translation:**
```
👤 User: "Hello, how are you?" (English)
🤪 Shinchan: "こんにちは、元気ですか？" (Japanese with playful personality)
```

### 🌟 Advanced Features
- **📱 Modern Glass-morphism UI**: Beautiful dark theme with responsive design
- **💾 Persistent Chat History**: Save and manage multiple conversation sessions
- **🔄 Real-time WebSocket Communication**: Low-latency voice and text processing
- **📈 Business Intelligence**: Automated insights and trend analysis from data
- **🎯 Context-aware AI**: Data-driven conversational responses
- **⚙️ Dynamic Configuration**: Runtime API key management through web interface
- **🎵 Audio Queue Management**: Seamless audio playback with voice personas
- **📊 Multi-format Data Support**: CSV, PDF, Excel file processing

## 🛠️ Tech Stack

### 🖥️ Backend Architecture
- **FastAPI** - High-performance async web framework with automatic API documentation
- **WebSocket** - Real-time bidirectional communication for voice streaming
- **Python 3.9+** - Core application logic with async/await support
- **Uvicorn** - Lightning-fast ASGI server for production deployment
- **Jinja2** - Template engine for dynamic HTML rendering

### 🤖 AI & ML Services
- **Google Gemini 1.5 Flash** - Large Language Model for conversation and data analysis
- **AssemblyAI Streaming** - Real-time speech-to-text transcription with voice activity detection
- **Murf AI** - High-quality text-to-speech with multiple voice personas and languages

### 📊 Data Processing
- **pandas** - Advanced data manipulation and statistical analysis
- **pdfplumber** - PDF text extraction and table parsing
- **openpyxl & xlrd** - Excel file processing (.xlsx, .xls)
- **python-multipart** - File upload handling

### 🎨 Frontend Technologies
- **Modern HTML5/CSS3** - Responsive design with glass-morphism effects
- **Vanilla JavaScript** - Real-time UI updates and WebSocket handling
- **Web Audio API** - Audio processing and playback management
- **LocalStorage** - Client-side data persistence for chat history and settings

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** installed on your system
- **Git** for cloning the repository
- API keys for the required services (can be configured later)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd N9NE-AI
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional)**
   Create a `.env` file in the root directory:
   ```env
   # API Keys (can also be configured via web interface)
   GEMINI_API_KEY=your_gemini_api_key_here
   ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
   MURF_API_KEY=your_murf_api_key_here
   
   # Optional Configuration
   DEBUG=True
   HOST=0.0.0.0
   PORT=8000
   ```

### Running the Application

**Development Mode:**
```bash
uvicorn main:app --reload
```

**Production Mode:**
```bash
python start.py
```

Access the application at `http://localhost:8000`

## ⚙️ Configuration

### API Keys Setup
After starting the application:
1. Click the **Settings** ⚙️ button in the sidebar
2. Enter your API keys for the required services:
   - **Gemini API Key**: For AI conversation and data analysis
   - **AssemblyAI API Key**: For speech-to-text transcription
   - **Murf API Key**: For text-to-speech voice generation
3. Save the configuration
4. Start using the voice agent!

### Required API Keys

| Service | Purpose | Get API Key |
|---------|---------|-------------|
| **Google Gemini** | AI conversation & data analysis | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| **AssemblyAI** | Speech-to-text transcription | [AssemblyAI Dashboard](https://www.assemblyai.com/dashboard/) |
| **Murf AI** | Text-to-speech voice generation | [Murf AI Platform](https://murf.ai/) |

## 🎯 Usage Guide

### 🏠 Main Interface
1. **📊 Upload Data**: Click the "+" button to upload CSV, PDF, or Excel files
2. **🔍 Get AI Insights**: Kiya automatically analyzes and provides key findings
3. **🎤 Voice Chat**: Click the microphone to start real-time voice conversations
4. **💬 Text Chat**: Type messages in the input field for text-based interaction
5. **💾 Chat History**: Access previous conversations from the sidebar

### 🎭 Persona Voice Agent (`/persona-voice-agent`)
1. Choose from available AI personas:
   - **😴 Nobita**: Tired student who needs Doraemon's help
   - **🤪 Shinchan**: Mischievous 5-year-old with playful attitude
   - **👧 Friendly Girl**: Sweet and helpful conversational partner
2. Experience unique personality-driven responses and voice characteristics
3. Real-time voice interaction with character-specific behaviors

### 🌍 Multilingual Voice Agent (`/multilingual-voice-agent`)
1. Enter text or record voice in your preferred language
2. Select target language from 12+ supported options
3. Choose voice persona for the translated response
4. Receive real-time translation with character voice output

## 🌐 API Endpoints

### Core Endpoints
- `GET /` - Main application interface
- `GET /health` - Health check endpoint
- `GET /multilingual-voice-agent` - Multilingual voice interface
- `GET /persona-voice-agent` - Persona-based voice interface

### WebSocket Endpoints
- `WS /ws` - Real-time voice communication for main interface
- `WS /ws/persona` - Real-time voice communication with persona support

### API Endpoints
- `POST /upload` - File upload and analysis (CSV, PDF, Excel)
- `POST /chat` - Text-based chat messages
- `POST /persona_chat` - Text-based chat with persona support
- `POST /multilingual_voice` - Text translation with voice generation
- `POST /process_voice_translation` - Voice recording translation
- `POST /config/api-keys` - Update API keys configuration
- `GET /config/api-keys/status` - Check API keys status
- `GET /multilingual-voice/config` - Get available languages and personas
- `GET /persona-voice/config` - Get available personas information

## 📁 Project Structure

```
N9NE-AI/
├── main.py                          # FastAPI application with WebSocket support
├── start.py                         # Production startup script for Render deployment
├── config.py                        # Dynamic API configuration management
├── personas.py                      # AI persona definitions and system instructions
├── schemas.py                       # Pydantic data models
├── requirements.txt                 # Python dependencies
├── render.yaml                      # Render deployment configuration
├── .gitignore                       # Git ignore patterns
├── README.md                        # Project documentation
│
├── services/                        # Core service modules
│   ├── __init__.py                 # Package initialization
│   ├── data_processor.py           # File processing and data analysis
│   ├── llm.py                      # Google Gemini integration
│   ├── stt.py                      # AssemblyAI speech-to-text
│   ├── tts.py                      # Murf AI text-to-speech
│   ├── translator.py               # Multilingual translation service
│   └── voice_changer.py            # Voice persona and effects
│
├── templates/                       # HTML templates
│   ├── index.html                  # Main application interface
│   ├── multilingual_voice_agent.html # Multilingual translation page
│   └── persona_voice_agent.html    # Persona interaction page
│
├── static/                          # Static assets
│   └── script.js                   # Frontend JavaScript logic
│
└── uploads/                         # File upload directory (auto-created)
```

## 🔧 API Endpoints

### Main Application
- `GET /` - Main application interface
- `GET /health` - Health check endpoint
- `GET /multilingual-voice-agent` - Multilingual voice interface
- `GET /persona-voice-agent` - Persona-based voice interface

### Data Processing
- `POST /upload` - File upload and AI analysis
- `POST /chat` - Text-based chat with Kiya
- `POST /persona_chat` - Text-based chat with persona support

### Voice & Translation
- `WebSocket /ws` - Real-time voice communication (main)
- `WebSocket /ws/persona` - Real-time voice communication with personas
- `POST /multilingual_voice` - Text translation with voice generation
- `POST /process_voice_translation` - Voice-to-voice translation

### Configuration
- `GET /multilingual-voice/config` - Available languages and personas
- `GET /persona-voice/config` - Available personas for voice agent
- `POST /config/api-keys` - Update API keys dynamically
- `GET /config/api-keys/status` - Check API key configuration status

## 🎭 AI Personas & Features

### AI Personas (Character-based Interactions)
- 😴 **Nobita**: Tired student who needs Doraemon's help
  - Always complains and calls for Doraemon
  - Reluctant but eventually provides answers
  - Ends responses wanting to sleep or rest
  
- 🤪 **Shinchan**: Mischievous 5-year-old with playful attitude
  - Playful, cheeky, and energetic
  - Makes silly jokes and references to "butt dance"
  - Uses simple but surprisingly mature language
  
- 👧 **Friendly Girl**: Sweet and helpful voice
  - Always positive and encouraging
  - Warm, caring tone with gentle language
  - Offers help willingly and shows empathy

### Multilingual Support
- 🇺🇸 English
- 🇯🇵 Japanese (日本語)
- 🇪🇸 Spanish (Español)
- 🇫🇷 French (Français)
- 🇩🇪 German (Deutsch)
- 🇮🇳 Hindi (हिन्दी)
- 🇨🇳 Chinese (中文)
- 🇰🇷 Korean (한국어)
- And more languages supported through translation service

### Voice Personas (Multilingual Agent)
- 👤 **Normal**: Standard conversational voice
- 🧒 **Shinchan**: Playful, energetic child-like voice
- 🤖 **Robot**: Mechanical, robotic voice
- 🎭 **Deep Voice**: Deep, authoritative voice
- 👧 **Girl**: Sweet, cheerful girl voice

## 💡 Why This Is Impressive

### Technical Innovation
- **Multi-modal AI Integration**: Combines LLM, STT, TTS, and translation in one platform
- **Real-time Processing**: Dual WebSocket endpoints for different interaction modes
- **Advanced Persona System**: Character-based AI with unique personality instructions
- **Dynamic Configuration**: Runtime API key management without restart
- **Intelligent Data Analysis**: Automated business intelligence from raw files
- **Production Ready**: Render deployment with proper startup scripts

### User Experience
- **Accessibility**: Voice-first interface for data analysis
- **Character Interaction**: Anime-inspired personas with authentic personalities
- **Conversational Flow**: Natural dialogue with context retention
- **Professional UI**: Modern glass-morphism design with dark theme
- **Multi-Interface**: Separate interfaces for different use cases
- **Real-time Feedback**: Live status updates and configuration management

## 🎪 Demo Scenarios

### Data Analysis Demo
1. Upload a CSV, PDF, or Excel file using the "+" button
2. Listen as Kiya explains key insights and trends
3. Ask follow-up questions like "Which category performed best?"
4. Get conversational explanations of your data
5. Continue the dialogue with voice or text

### Persona Interaction Demo
1. Visit `/persona-voice-agent`
2. Select Nobita persona and ask "What is 5+3?"
3. Enjoy the character's tired, reluctant response style
4. Try Shinchan for playful, energetic interactions
5. Switch to Friendly Girl for supportive conversations

### Multilingual Voice Demo
1. Visit `/multilingual-voice-agent`
2. Enter "Hello, how are you today?"
3. Select Japanese as target language
4. Choose Shinchan persona
5. Listen to the translated response with character voice

### Voice-to-Voice Translation
1. Record voice message in English
2. Select target language (e.g., Spanish)
3. Choose voice persona (e.g., Girl)
4. Receive translated audio response

## 🚀 Future Enhancements

### Technical Roadmap
- **Enhanced Persona System**: More anime characters and custom personalities
- **Advanced Visualizations**: AI-generated charts and graphs
- **Custom Voice Training**: User-specific voice personas
- **Multi-file Analysis**: Comparative analysis across datasets
- **Real-time Data Streaming**: Live dashboard updates
- **API Integration**: Connect with business intelligence tools

### Feature Expansion
- **More Anime Characters**: Doraemon, Goku, Naruto personas
- **Video Analysis**: Support for video file processing
- **Collaborative Features**: Multi-user voice sessions
- **Mobile App**: Native iOS/Android applications
- **Voice Commands**: System control via voice
- **Custom Workflows**: User-defined analysis pipelines
- **Emotion Recognition**: Voice emotion analysis for better responses

## 🔒 Security & Privacy

- **Dynamic API Key Management**: Runtime configuration without exposing keys
- **File Sanitization**: Safe file upload processing with type validation
- **Data Encryption**: Secure data transmission via HTTPS
- **Session Management**: Isolated user sessions with WebSocket security
- **Temporary Storage**: Automatic file cleanup in uploads directory
- **Environment Isolation**: Separate development and production configurations

## 🚀 Deployment

### Render Deployment
The application is configured for easy deployment on Render:

1. Connect your GitHub repository to Render
2. Use the included `render.yaml` configuration
3. Set environment variables in Render dashboard
4. Deploy with automatic builds

### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd N9NE-AI

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload
```

---

**Built with ❤️ BY ARYAN SONDHARVA**