from flask import Flask, render_template, request, jsonify
import threading
import time
import os
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound

app = Flask(__name__)

# Global variable to control monitoring
monitoring = False
hotword = 'camila'

# Get the directory path of the current script
current_dir = os.path.dirname(__file__)
audio_file_path = os.path.join(current_dir, 'audios', 'feedback.mp3')

# Generate audio file if it doesn't exist
if not os.path.exists(audio_file_path):
    texto = 'bom dia pessoal, como vai, tudo joia, tudo beleza'
    language = 'pt'
    habla = gTTS(text=texto, lang=language, slow=False)
    habla.save(audio_file_path)

def monitorear_audio():
    global monitoring
    microfono = sr.Recognizer()
    with sr.Microphone() as source:
        while monitoring:
            print("Aguardando o Comandos: ")
            audio = microfono.listen(source)
            try:
                trigger = microfono.recognize_google(audio, language='es')
                trigger = trigger.lower()
                if hotword in trigger:
                    print('comando:', trigger)
                    responde('feedback')
                    ##ejecutar los comandos
                    monitoring = False  # stop monitoring after trigger
                    break
            except sr.UnknownValueError:
                print("Google no entiende el audio")
            except sr.RequestError as e:
                print(f"Could not request result from Google Cloud Speech service; {e}")
            time.sleep(1)  # slight delay to prevent excessive looping

def responde(archivo):
    playsound(audio_file_path)  # Use the correct file path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    global monitoring
    monitoring = True
    threading.Thread(target=monitorear_audio).start()
    return jsonify({'status': 'Monitoring started'})

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    global monitoring
    monitoring = False
    return jsonify({'status': 'Monitoring stopped'})

if __name__ == '__main__':
    app.run(debug=True)
