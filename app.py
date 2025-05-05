import os
from flask import Flask, jsonify, send_from_directory
import openai
from gtts import gTTS
import speech_recognition as sr

app = Flask(__name__)

openai.api_key = os.getenv("0492Lamanee.")  # set this in Render environment variables

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/listen')
def listen_and_respond():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        command = recognizer.recognize_google(audio)
        print("You said:", command)

        # Get GPT response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Yaaya, a helpful AI assistant."},
                {"role": "user", "content": command}
            ]
        ).choices[0].message.content.strip()

        response = f"I am Yaaya. {response} I was created by a software engineer named AL-AMEEN in Abuja, Nigeria."

        # Convert to audio using gTTS and save (optional: for local testing only)
        tts = gTTS(response)
        tts.save("response.mp3")

    except Exception as e:
        return jsonify(reply=f"Error: {str(e)}")

    return jsonify(reply=response)

# Run for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
