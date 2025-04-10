import requests
from flask import Flask, render_template, request
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def get_first_aid_advice(user_input):
    if not OPENROUTER_API_KEY:
        return "API key missing."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourfrontendsite.netlify.app",  # change to your real frontend URL
        "X-Title": "QuickAid First Aid Chat"
    }

    data = {
        "model": "x-ai/grok-3-mini-beta",
        "messages": [
            {"role": "system", "content": "You are a kind and simple first-aid assistant. Give only first-aid advice, not medical diagnosis."},
            {"role": "user", "content": f"Give simple first-aid steps (not diagnosis) for: {user_input}"}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return "Sorry, couldn't get a reply."

@app.route("/", methods=["POST"])
def get_response():
    user_msg = request.json.get("message", "")
    bot_reply = get_first_aid_advice(user_msg)
    return {"reply": bot_reply}

if __name__ == "__main__":
    from os import environ
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
