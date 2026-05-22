# vijay-voice-bot
🧠 AI Chatbot (Flask + Gemini + Voice Assistant)

This is a smart AI-powered chatbot web application built using Flask and Google Gemini AI. It provides a conversational interface that supports natural language chat, remembers conversation history, and converts responses into speech using text-to-speech.

The system includes a fallback offline mode, ensuring the chatbot still responds even when the AI API is unavailable.

🚀 Features
💬 AI chat using Google Gemini API
🧠 Conversation memory using SQLite database
🎙️ Text-to-Speech (voice replies using gTTS)
🔄 Offline fallback chatbot system
📜 Chat history storage per session
🌐 Simple web UI using Flask templates
🔐 Environment variable support for API security
🛠️ Tech Stack
Python
Flask
Google Gemini API
SQLite
gTTS (Google Text-to-Speech)
HTML (Frontend templates)
dotenv (environment management)
📦 How it works
User sends a message from the web interface
Flask backend processes the request
Gemini AI generates a response (or fallback system if offline)
Response is stored in SQLite chat history
Response is converted into speech using gTTS
Both text and audio are returned to the user
🔐 Environment Variables

Create a .env file:

GEMINI_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
📌 Purpose

This project demonstrates how to build a full-stack AI assistant with:

real-time conversation
persistent memory
voice output
fallback intelligence system

It can be used as a base for:

AI customer support bots
virtual assistants
educational chat systems
voice-enabled AI apps
