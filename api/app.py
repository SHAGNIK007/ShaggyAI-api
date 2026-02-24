from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not GROQ_API_KEY:
            return jsonify({"reply": "ERROR: GROQ_API_KEY not set in Vercel"}), 500

        user_message = request.json.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please enter a message."})

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            },
            timeout=30
        )

        data = response.json()

        if "choices" not in data:
            return jsonify({"reply": f"Groq Error: {data}"}), 500

        reply = data["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500
