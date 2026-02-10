from flask import Flask , render_template , request , jsonify
import requests            
import os 

app = Flask(__name__, template_folder="../templates", static_folder="../static")

API_KEY = os.getenv("GEMINI_KEY")
MODEL_NAME = "models/gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/{MODEL_NAME}:generateContent"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    payload = {
        "contents": [
            {
                "parts": [{"text": user_message}]
            }
        ]
    }

    r = requests.post(
        GEMINI_URL,
        params={"key": API_KEY},
        json=payload,
        timeout=30
    )

    data = r.json()
    reply = data["candidates"][0]["content"]["parts"][0]["text"]

    return jsonify({"reply": reply})