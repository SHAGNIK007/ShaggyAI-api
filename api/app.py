from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.1-8b-instant"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json["message"]

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        r = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )

        data = r.json()

        if "choices" not in data:
            return jsonify({"reply": f"Groq Error: {data}"}), 500

        reply = data["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
