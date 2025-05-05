from flask import Flask, jsonify, send_from_directory
import openai
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)

openai.api_key = "your-openai-api-key"
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
        return jsonify(reply="Sorry, I didn't understand that.")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": command}]
    ).choices[0].message.content.strip()

    # Speak out loud
    engine.say(response)
    engine.runAndWait()

    return jsonify(reply=response)

if __name__ == '__main__':
    app.run(debug=True)
