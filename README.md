# N9NE - Advanced Multilingual Voice Agent & Data Analysis Platform

A sophisticated **AI-powered platform** that combines multilingual voice translation, conversational data analysis, and intelligent file processing. Upload documents, analyze data, and interact through voice in multiple languages with different personas.

## 🚀 What It Does

**Core Capabilities**: 
- **Multilingual Voice Translation**: Speak in one language, hear responses in another with customizable voice personas
- **Intelligent Data Analysis**: Upload CSV, PDF, or Excel files for AI-powered insights and conversational analysis
- **Real-time Voice Interaction**: Natural speech-to-text and text-to-speech conversations
- **Multi-persona Voice Generation**: Choose from different voice characters (Shinchan, Robot, Deep Voice, Girl, Normal)

### Example Interactions

**Data Analysis Flow:**
👤 **User**: "Analyze this sales report."  
🤖 **Agent**: "Your sales grew by 18% in Q2, with the highest increase in North America."  
👤 **User**: "Which region performed worst?"  
🤖 **Agent**: "Europe saw a 5% decline in sales this quarter."

**Multilingual Translation:**
👤 **User**: "Hello, how are you?" (English)  
🤖 **Agent**: "こんにちは、元気ですか？" (Japanese with Shinchan persona)

## ✨ Key Features

### Core Functionality
- **🎤 Real-time Voice Input**: Advanced speech-to-text using AssemblyAI
- **🔊 Multi-persona Voice Output**: Text-to-speech with character voices via Murf AI
- **🌍 Multilingual Support**: Translation between 12+ languages
- **📊 Intelligent Data Processing**: CSV, PDF, Excel analysis with AI insights
- **💬 Conversational AI**: Context-aware dialogue powered by Google Gemini
- **🎭 Voice Personas**: Multiple character voices (Shinchan, Robot, Girl, etc.)

### Advanced Features
- **📱 Modern Responsive UI**: Beautiful glass-morphism design
- **💾 Chat History Management**: Persistent conversation storage
- **🔄 Real-time Updates**: WebSocket-based live communication
- **📈 Business Intelligence**: Automated insights and trend analysis
- **🎯 Context-aware Responses**: Data-driven conversational AI

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance async web framework
- **WebSocket**: Real-time bidirectional communication
- **Python**: Core application logic

### AI & ML Services
- **Google Gemini**: Large Language Model for analysis and translation
- **AssemblyAI**: Advanced speech-to-text transcription
- **Murf AI**: High-quality text-to-speech with voice personas

### Data Processing
- **pandas**: Data manipulation and analysis
- **pdfplumber**: PDF text and table extraction
- **openpyxl**: Excel file processing

### Frontend
- **Modern HTML5/CSS3**: Responsive design with glass-morphism
- **Vanilla JavaScript**: Real-time UI updates and WebSocket handling
- **Font Awesome**: Professional iconography

## 📋 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file with your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
MURF_API_KEY=your_murf_api_key_here
```

### 3. Run the Application
```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000` to access the application.

## 🎯 How to Use

1. **Upload Data**: Click "Upload Data File" to upload CSV, PDF, or Excel files
2. **Get Insights**: The AI automatically analyzes and speaks key findings
3. **Ask Questions**: Use the microphone to ask follow-up questions
4. **Voice Responses**: Listen to conversational explanations of your data

## 📁 Project Structure

```
N9NE/
├── main.py                          # FastAPI application with WebSocket support
├── config.py                       # API configuration and environment setup
├── requirements.txt                 # Python dependencies
├── schemas.py                       # Pydantic data models
├── env_template.txt                 # Environment variables template
├── install_dependencies.py         # Automated dependency installer
├── sample_data.csv                  # Example dataset for testing
├── services/                        # Core service modules
│   ├── __init__.py                 # Package initialization
│   ├── data_processor.py           # File processing and data analysis
│   ├── llm.py                      # Google Gemini AI integration
│   ├── stt.py                      # AssemblyAI speech-to-text
│   ├── tts.py                      # Murf text-to-speech
│   ├── translator.py               # Multilingual translation service
│   └── voice_changer.py            # Voice persona and effects
├── templates/                       # HTML templates
│   ├── index.html                  # Main application interface
│   └── multilingual_voice_agent.html # Multilingual voice interface
├── static/                         # Static assets
│   ├── script.js                   # Frontend JavaScript logic
│   └── fallback.mp3               # Audio fallback file
├── uploads/                        # File upload storage
│   └── *.wav                      # Generated audio files
├── models/                         # AI model configurations
└── node_modules/                   # Node.js dependencies (if any)
```

## 🔧 API Endpoints

### Main Application
- `GET /` - Main application interface
- `GET /multilingual-voice-agent` - Multilingual voice interface

### Data Processing
- `POST /upload` - File upload and AI analysis
- `POST /chat` - Text-based chat endpoint

### Voice & Translation
- `WebSocket /ws` - Real-time voice communication
- `POST /multilingual_voice` - Text translation with voice generation
- `POST /process_voice_translation` - Voice-to-voice translation
- `GET /multilingual-voice/config` - Available languages and personas

## 🎭 Supported Languages & Personas

### Languages (12+)
- 🇺🇸 English
- 🇯🇵 Japanese (日本語)
- 🇪🇸 Spanish (Español)
- 🇫🇷 French (Français)
- 🇩🇪 German (Deutsch)
- 🇮🇳 Hindi (हिन्दी)
- 🇨🇳 Chinese (中文)
- 🇰🇷 Korean (한국어)
- 🇮🇹 Italian (Italiano)
- 🇵🇹 Portuguese (Português)
- 🇷🇺 Russian (Русский)
- 🇸🇦 Arabic (العربية)

### Voice Personas
- 👤 **Normal**: Standard conversational voice
- 🧒 **Shinchan**: Playful, energetic child-like voice
- 🤖 **Robot**: Mechanical, robotic voice
- 🎭 **Deep Voice**: Deep, authoritative voice
- 👧 **Girl**: Sweet, cheerful girl voice

## 💡 Why This Is Impressive

### Technical Innovation
- **Multi-modal AI Integration**: Combines LLM, STT, TTS, and translation in one platform
- **Real-time Processing**: WebSocket-based live voice interaction
- **Advanced Voice Synthesis**: Character-based voice personas with emotional context
- **Intelligent Data Analysis**: Automated business intelligence from raw files

### User Experience
- **Accessibility**: Voice-first interface for data analysis
- **Personalization**: Multiple voice personas and languages
- **Conversational Flow**: Natural dialogue with context retention
- **Professional UI**: Modern glass-morphism design

## 🎪 Demo Scenarios

### Data Analysis Demo
1. Upload the included `sample_data.csv` file
2. Listen as N9NE explains sales trends across regions
3. Ask "Which product category performed best?"
4. Get spoken insights about performance metrics
5. Continue with follow-up questions

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
- **Real-time Data Streaming**: Live dashboard updates
- **Advanced Visualizations**: AI-generated charts and graphs
- **Custom Voice Training**: User-specific voice personas
- **Multi-file Analysis**: Comparative analysis across datasets
- **API Integration**: Connect with business intelligence tools

### Feature Expansion
- **Video Analysis**: Support for video file processing
- **Collaborative Features**: Multi-user voice sessions
- **Mobile App**: Native iOS/Android applications
- **Voice Commands**: System control via voice
- **Custom Workflows**: User-defined analysis pipelines

## 🔒 Security & Privacy

- **API Key Management**: Secure environment variable handling
- **File Sanitization**: Safe file upload processing
- **Data Encryption**: Secure data transmission
- **Session Management**: Isolated user sessions
- **Temporary Storage**: Automatic file cleanup

---

**Built with ❤️ for next-generation conversational AI**