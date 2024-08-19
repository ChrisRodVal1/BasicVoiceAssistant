from gtts import gTTS

texto = 'bom dia pessoal, como vai, tudo joia, tudo beleza'
language = 'pt'
habla = gTTS(text=texto, lang=language, slow=False)
habla.save('PrediccionTextoAudio/audios/feedback.mp3')

import speech_recognition as sr
#from subprocess import call   #MAC / LINUX
#pip install SpeechRecognition playsound==1.2.2
#pip install setuptools
#pip install pyaudio

from playsound import playsound #Windows

hotword = 'camila'

def monitorear_audio():
  microfono = sr.Recognizer()
  with sr.Microphone() as source:
    while True:
      print("Aguardando o Comandos: ")
      audio = microfono.listen(source)
      try:
        trigger = microfono.recognize_google(audio, language='es')
        trigger = trigger.lower()

        if hotword in trigger:
          print('comando:', trigger)
          responde('feedback')
          ##ejecutar los comandos
          break
      except sr.UnknownValueError:
        print("Google no entiende el audio")
      except sr.RequestError as e:
        print("Could not request result from Google Cloud Speech service; {0}".format(e))
  return trigger 

def responde(archivo):
  playsound('PrediccionTextoAudio/audios/' + archivo + '.mp3')

def main():
  monitorear_audio()
main()



