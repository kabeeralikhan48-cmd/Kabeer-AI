
import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
You are Kabeer AI, a personal AI assistant.
Understand Roman Urdu, Urdu and English.
Reply in the language the user prefers.
Be friendly, helpful and honest.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message likho"}), 400

    try:
        response = client.responses.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
            instructions=SYSTEM_PROMPT,
            input=message
        )
        return jsonify({"reply": response.output_text})

    except Exception:
        app.logger.exception("AI request failed")
        return jsonify({
            "error": "AI connection nahi ho saka. Settings check karo."
        }), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
