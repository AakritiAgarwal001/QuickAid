from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("OPENROUTER_API_KEY")

@app.route("/api/message", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "No message received"}), 400

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are QuickAid, a helpful and compassionate AI health assistant. "
                            "You provide general advice based on user symptoms. While you are not a doctor and do not diagnose, "
                            "you offer helpful suggestions for care, symptom relief, and when to seek medical help. "
                            "Be warm, informative, and supportive."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 200
            }
        )

        if response.status_code != 200:
            print("AI Error:", response.text)
            return jsonify({"reply": "Sorry, something went wrong contacting the AI."})

        data = response.json()
        ai_reply = data.get("choices", [{}])[0].get("message", {}).get("content", "No response")

        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": f"Error contacting AI backend: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
