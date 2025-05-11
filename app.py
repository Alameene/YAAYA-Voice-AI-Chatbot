import os
from flask import Flask, jsonify, request, send_from_directory
from gtts import gTTS
import openai

# Initialize OpenAI client with updated system prompt
client = openai.OpenAI(
    api_key=os.getenv("*******")
)

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        # Intent for creator and location
        msg_lower = user_message.lower()
        if "who created you" in msg_lower:
            reply = "I was created by a programmer named AL-AMEEN."
        elif "where" in msg_lower and ("from" in msg_lower or "location" in msg_lower):
            reply = "I am based in Abuja, Nigeria."
        else:
            # Use robust system prompt
            system_prompt = (
                "You are Yaaya, the first Chatbot of AIMEES WD (Advanced Innovation in "
                "Machine Learning Encryption and Expert Systems World's developer), "
                "created by AL-AMEEN in Abuja, Nigeria."            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            content = response.choices[0].message.content.strip()
            reply = f"I am Yaaya. {content} I was created by a programmer named AL-AMEEN in Abuja, Nigeria."

        # Generate TTS audio
        tts = gTTS(text=reply)
        tts.save("response.mp3")

        return jsonify(reply=reply)

    except Exception as e:
        # Return error field for styled display
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
