# N9NE-AI - Advanced Multilingual Voice Agent & Data Analysis Platform

A sophisticated **AI-powered conversational platform** that combines intelligent data analysis, multilingual voice translation, and persona-based voice interactions. Upload documents, analyze data, and interact through voice with customizable AI personas including anime characters like Nobita and Shinchan.

## 🚀 What It Does

**Core Capabilities**: 
- **Intelligent Data Analysis**: Upload CSV, PDF, or Excel files for AI-powered insights and conversational analysis
- **Real-time Voice Interaction**: Natural speech-to-text and text-to-speech conversations with persona support
- **Multilingual Voice Translation**: Speak in one language, hear responses in another with customizable voice personas
- **AI Persona System**: Choose from different AI characters (Nobita, Shinchan, Friendly Girl) with unique personalities

### Example Interactions

**Data Analysis Flow:**
👤 **User**: "Analyze this sales report."  
🤖 **Kiya**: "Your sales grew by 18% in Q2, with the highest increase in North America."  
👤 **User**: "Which region performed worst?"  
🤖 **Kiya**: "Europe saw a 5% decline in sales this quarter."

**Persona Interaction (Nobita):**
👤 **User**: "What is 2+2?"  
😴 **Nobita**: "Ugh, I'm so tired of math problems! Doraemon, where are you? I need your calculator gadget! *sigh* But I guess I have to do this myself... 2 plus 2 equals 4. There, I answered it! Can I take a nap now?"

**Multilingual Translation:**
👤 **User**: "Hello, how are you?" (English)  
🤪 **Shinchan**: "こんにちは、元気ですか？" (Japanese with playful personality)

## ✨ Key Features

### Core Functionality
- **🎤 Real-time Voice Input**: Advanced speech-to-text using AssemblyAI
- **🔊 AI Persona Voice Output**: Text-to-speech with character-based responses
- **🌍 Multilingual Support**: Translation between multiple languages
- **📊 Intelligent Data Processing**: CSV, PDF, Excel analysis with AI insights
- **💬 Conversational AI**: Context-aware dialogue powered by Google Gemini
- **🎭 AI Personas**: Unique character personalities (Nobita, Shinchan, Friendly Girl)

### Advanced Features
- **📱 Modern Responsive UI**: Beautiful glass-morphism design with dark theme
- **💾 Chat History Management**: Persistent conversation storage with sidebar
- **🔄 Real-time Updates**: WebSocket-based live communication
- **📈 Business Intelligence**: Automated insights and trend analysis
- **🎯 Context-aware Responses**: Data-driven conversational AI
- **⚙️ Dynamic Configuration**: Runtime API key management

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance async web framework
- **WebSocket**: Real-time bidirectional communication
- **Python**: Core application logic
- **Uvicorn**: ASGI server for production deployment

### AI & ML Services
- **Google Gemini 1.5 Flash**: Large Language Model for analysis and conversation
- **AssemblyAI**: Advanced speech-to-text transcription
- **Murf AI**: High-quality text-to-speech with voice personas

### Data Processing
- **pandas**: Data manipulation and analysis
- **pdfplumber**: PDF text and table extraction
- **openpyxl & xlrd**: Excel file processing

### Frontend
- **Modern HTML5/CSS3**: Responsive design with glass-morphism effects
- **Vanilla JavaScript**: Real-time UI updates and WebSocket handling
- **Custom CSS**: Professional dark theme with animations

## 📋 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables (Optional)
Create a `.env` file with your API keys, or configure them through the web interface:
```env
GEMINI_API_KEY=your_gemini_api_key_here
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
MURF_API_KEY=your_murf_api_key_here
```

### 3. Run the Application

**Local Development:**
```bash
uvicorn main:app --reload
```

**Production (Render Deployment):**
```bash
python start.py
```

Visit `http://localhost:8000` to access the application.

### 4. Configure API Keys
After starting the application:
1. Click the **Settings** button in the sidebar
2. Enter your API keys for Gemini, AssemblyAI, and Murf
3. Save the configuration
4. Start using the voice agent!

## 🎯 How to Use

### Main Interface
1. **Upload Data**: Click the "+" button to upload CSV, PDF, or Excel files
2. **Get Insights**: Kiya automatically analyzes and provides key findings
3. **Voice Interaction**: Click the microphone to start voice conversations
4. **Text Chat**: Type questions in the input field for text-based interaction

### Persona Voice Agent
1. Visit `/persona-voice-agent` for character-based interactions
2. Choose from available personas (Nobita, Shinchan, Friendly Girl)
3. Enjoy unique personality-driven responses

### Multilingual Voice Agent
1. Visit `/multilingual-voice-agent` for translation features
2. Enter text or record voice in one language
3. Select target language and persona
4. Receive translated response with character voice

## 📁 Project Structure

```
N9NE-AI/
├── main.py                          # FastAPI application with WebSocket support
├── start.py                         # Production startup script for Render
├── config.py                       # Dynamic API configuration management
├── personas.py                      # AI persona definitions and system instructions
├── schemas.py                       # Pydantic data models
├── requirements.txt                 # Python dependencies
├── render.yaml                      # Render deployment configuration
├── .gitignore                      # Git ignore rules
├── services/                        # Core service modules
│   ├── __init__.py                 # Package initialization
│   ├── data_processor.py           # File processing and data analysis
│   ├── llm.py                      # Google Gemini AI integration (Kiya assistant)
│   ├── stt.py                      # AssemblyAI speech-to-text
│   ├── tts.py                      # Murf text-to-speech
│   ├── translator.py               # Multilingual translation service
│   └── voice_changer.py            # Voice persona and effects
├── templates/                       # HTML templates
│   ├── index.html                  # Main application interface
│   ├── multilingual_voice_agent.html # Multilingual voice interface
│   ├── persona_voice_agent.html    # Persona-based voice interface
│   └── logo/                       # Logo assets
│       └── 1.png                   # Application logo
├── static/                         # Static assets
│   └── script.js                   # Frontend JavaScript logic
└── uploads/                        # File upload and audio storage
    └── *.wav                      # Generated audio files
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
  
- 🤪 **Shinchan**: Mischievous 5-year-old with funny attitude
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

**Built with ❤️ for next-generation conversational AI with anime-inspired personalities**