from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

API_KEY = os.getenv("GEMINI_KEY")

MODEL_NAME = "models/gemini-1.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not API_KEY:
            return jsonify({"reply": "ERROR: GEMINI_KEY not set in Vercel"}), 500

        user_message = request.json.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please enter a message."})

        payload = {
            "contents": [
                {
                    "parts": [{"text": user_message}]
                }
            ]
        }

        response = requests.post(
            GEMINI_URL,
            params={"key": API_KEY},
            json=payload,
            timeout=30
        )

        data = response.json()

        if "candidates" not in data:
            return jsonify({"reply": f"Gemini API Error: {data}"}), 500

        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500


# ❌ DO NOT use app.run() on Vercel
