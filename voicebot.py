from flask import Flask, request, jsonify, session, send_file, render_template
from google import genai
from gtts import gTTS
from io import BytesIO
import sqlite3
import uuid
import os
import datetime
from dotenv import load_dotenv


base_dir = os.path.dirname(os.path.abspath(__file__))


load_dotenv(os.path.join(base_dir, ".env"))



app = Flask(__name__)
app.secret_key = "replace_with_your_secret_key"



API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        print("Successfully initialized Gemini client.")
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
else:
    print("Warning: GEMINI_API_KEY environment variable not found. Will run in local fallback mode.")



DB_FILE = os.path.join(base_dir, "chat_history.db")
LOG_FILE = os.path.join(base_dir, "chatlog.txt")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

init_db()



def save_chat(session_id, role, message):
 
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute(
            """
            INSERT INTO chats
            (session_id, role, message)
            VALUES (?, ?, ?)
            """,
            (session_id, role, message)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database save error: {e}")

    
    try:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            if role == "user":
                f.write(f"\n[{now_str}]\nUser: {message}\n")
            else:
                f.write(f"Bot: {message}\n----------------------------------------\n")
    except Exception as e:
        print(f"Chatlog text write error: {e}")



def load_memory(session_id, limit=20):
    try:
        conn = sqlite3.connect(DB_FILE)
        rows = conn.execute(
            """
            SELECT role, message
            FROM chats
            WHERE session_id=?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, limit)
        ).fetchall()
        conn.close()
        rows.reverse()
        
        memory = []
        for role, message in rows:
            memory.append({
                "role": role,
                "content": message
            })
        return memory
    except Exception as e:
        print(f"Database load error: {e}")
        return []


def generate_local_reply(user_text):
    text = user_text.lower()
    
   
    if any(greet in text for greet in ["namaste", "hello", "hi"]):
        return "Namaste ji, meeku ela help cheyyali? [Local Fallback Mode]"
        
   
    if "naa peru" in text:
        try:
            name = user_text.split("naa peru")[-1].strip()
            return f"Namaste {name} ji, aapko kaise help chahiye? [Local Fallback Mode]"
        except:
            return "Namaste ji, aapko kaise help chahiye? [Local Fallback Mode]"
            
    
    if "demo" in text:
        return "Sure, meeku software demo schedule chestanu. [Local Fallback Mode]"
        
    
    if "software" in text:
        return "Software details meeku explain chestanu. [Local Fallback Mode]"
        
  
    if "help" in text:
        return "Cheppandi, nenu help chestanu. [Local Fallback Mode]"
        
    if "thank" in text:
        return "Welcome ji! [Local Fallback Mode]"
        
   
    if not os.getenv("GEMINI_API_KEY"):
        return "Warning: GEMINI_API_KEY is not configured on the server. Please add GEMINI_API_KEY=your_key to the .env file in the project folder to enable Gemini. [Offline Local Mode]"
        
    return "Sorry, nenu ardham chesukoledu. Please malli cheppandi. [Offline Local Mode]"



def generate_ai_reply(user_text, session_id):
    history = load_memory(session_id)

    prompt = """
You are a friendly AI assistant.

Rules:
- Speak naturally.
- Mix Telugu and Hindi smoothly.
- Be respectful.
- Use conversational language.
- Remember previous conversation context.
- Keep replies concise unless user asks for details.
"""

    conversation = prompt + "\n\n"

    for item in history:
        conversation += (
            f"{item['role']}: "
            f"{item['content']}\n"
        )

    conversation += f"user: {user_text}\nassistant:"

    reply = None
    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=conversation
            )
            reply = response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}. Falling back to local responder.")
            reply = generate_local_reply(user_text)
    else:
        print("Gemini client not initialized. Falling back to local responder.")
        reply = generate_local_reply(user_text)

    
    save_chat(session_id, "user", user_text)
    save_chat(session_id, "assistant", reply)

    return reply



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    text = data.get("message", "").strip()

    if not text:
        return jsonify({"error": "Message required"}), 400

    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    session_id = session["session_id"]
    reply = generate_ai_reply(text, session_id)

    return jsonify({
        "reply": reply,
        "audio": "/voice?text=" + reply
    })



@app.route("/voice")
def voice():
    text = request.args.get("text", "")
    if not text:
        return ""

    tts = gTTS(text=text, lang="hi")
    mp3 = BytesIO()
    tts.write_to_fp(mp3)
    mp3.seek(0)

    return send_file(
        mp3,
        mimetype="audio/mpeg"
    )



@app.route("/history")
def history():
    if "session_id" not in session:
        return jsonify([])

    sid = session["session_id"]

    try:
        conn = sqlite3.connect(DB_FILE)
        rows = conn.execute(
            """
            SELECT role, message, created_at
            FROM chats
            WHERE session_id=?
            ORDER BY id
            """,
            (sid,)
        ).fetchall()
        conn.close()

        result = []
        for role, msg, dt in rows:
            result.append({
                "role": role,
                "message": msg,
                "time": dt
            })
        return jsonify(result)
    except Exception as e:
        print(f"Error reading history: {e}")
        return jsonify([])



@app.route("/clear", methods=["POST"])
def clear():
    if "session_id" not in session:
        return jsonify({"status": "ok"})

    sid = session["session_id"]

    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute(
            """
            DELETE FROM chats
            WHERE session_id=?
            """,
            (sid,)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "cleared"})
    except Exception as e:
        print(f"Error clearing memory: {e}")
        return jsonify({"status": "error", "message": str(e)})



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )