import os
from flask import Flask, jsonify, request, send_from_directory
import openai
from gtts import gTTS

app = Flask(__name__)

openai.api_key = os.getenv("0492Lamanee.")  # Replace with your actual key in Render environment vars

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        if "who created you" in user_message.lower():
            reply = "I was created by a programmer named AL-AMEEN."
        elif "where" in user_message.lower() and ("from" in user_message.lower() or "location" in user_message.lower()):
            reply = "I am based in Abuja, Nigeria."
        else:
            reply = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Yaaya, a helpful AI assistant."},
                    {"role": "user", "content": user_message}
                ]
            ).choices[0].message.content.strip()
            reply = f"I am Yaaya. {reply} I was created by a programmer named AL-AMEEN in Abuja, Nigeria."

        tts = gTTS(reply)
        tts.save("response.mp3")

        return jsonify(reply=reply)

    except Exception as e:
        return jsonify(reply=f"Error: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
