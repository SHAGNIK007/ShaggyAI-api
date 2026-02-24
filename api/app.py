from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

API_KEY = os.getenv("GEMINI_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

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

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(user_message)

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500
