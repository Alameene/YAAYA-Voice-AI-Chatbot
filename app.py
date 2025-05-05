import os
from flask import Flask, jsonify, send_from_directory
import openai
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)

openai.api_key = os.getenv("0492Lamanee.")
# Replace with your real key
engine = pyttsx3.init()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/listen')
def listen_and_respond():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
    except:
        reply = "Sorry, I didn't understand that."
        engine.say(reply)
        engine.runAndWait()
        return jsonify(reply=reply)

    print("You said:", command)

    # Get GPT response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": command}]
    ).choices[0].message.content.strip()

    # Add AL-AMEEN signature
    response += " I was created by a software engineer named AL-AMEEN in Abuja, Nigeria."

    # Speak the reply
    engine.say(response)
    engine.runAndWait()

    return jsonify(reply=response)

if __name__ == '__main__':
    app.run(debug=True)

