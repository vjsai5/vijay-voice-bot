🧠 AI Voice Chatbot (Flask + Gemini + Memory + Speech)

A full-stack AI chatbot web application built with Flask and Google Gemini AI, featuring conversation memory, voice output, and an offline fallback system. Designed as a lightweight AI assistant that works both online and offline.

✨ Features
💬 Intelligent AI chat powered by Google Gemini
🧠 Persistent conversation memory using SQLite
🎙️ Voice responses using Google Text-to-Speech (gTTS)
🔄 Offline fallback chatbot when API is unavailable
📜 Session-based chat history tracking
🌐 Simple and responsive Flask web interface
🔐 Secure API key management using environment variables
🖥️ Demo Flow
User sends a message via web UI
Flask backend receives the request
Gemini generates a response (or fallback logic runs)
Chat is stored in SQLite database
Response is converted into speech
Text + audio returned to frontend
🛠️ Tech Stack
Backend: Flask (Python)
AI Model: Google Gemini API
Database: SQLite
Voice Engine: gTTS
Frontend: HTML templates (Jinja2)
Environment Management: python-dotenv
📁 Project Structure
your-project/
│── app.py
│── requirements.txt
│── .env
│── chat_history.db
│── chatlog.txt
│
├── templates/
│     └── index.html
│
└── static/ (optional for CSS/JS)
⚙️ Installation
# Clone repository
git clone https://github.com/yourusername/yourrepo.git

# Enter project folder
cd yourrepo

# Install dependencies
pip install -r requirements.txt

# Run app
python app.py
🔐 Environment Variables

Create a .env file in root directory:

GEMINI_API_KEY=your_gemini_api_key
FLASK_SECRET_KEY=your_secret_key
🚀 Deployment (Render / Railway)
Start Command:
python app.py
Build Command:
pip install -r requirements.txt
Important:

Update Flask run configuration:

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
🔒 Security Notes
Never upload .env file to GitHub
Do not expose API keys publicly
Use environment variables in production
📌 Use Cases
AI assistant web apps
Chatbot learning projects
Voice-enabled AI systems
Flask + AI integration demos
Student final year projects
📈 Future Improvements
🔥 Streaming AI responses (real-time typing effect)
🎤 Voice input (speech-to-text)
⚡ WebSocket-based live chat
🌍 Multi-language auto detection
☁️ Docker + cloud deployment
👨‍💻 Author

Built as a full-stack AI learning project combining Flask, Gemini AI, and voice synthesis.

⭐ If you like this project

Give it a ⭐ on GitHub and feel free to fork and improve it!
