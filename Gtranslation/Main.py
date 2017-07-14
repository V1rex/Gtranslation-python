import pyaudio
import wave
import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import os

# this part will record your voice 

CHUNK = 1024 
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2 
RATE = 44100 #sample rate
RECORD_SECONDS = 5 #so you can put the number of the second wanna record 
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data) # 2 bytes(16 bits) per channel

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

#so here we gonna use the speech recognition api of google to transform speech to text ps: this program need an internet connection 

AUDIO_FILE = ("output.wav")



r = sr.Recognizer()

with sr.AudioFile(AUDIO_FILE) as source:
	#reads the audio file. Here we use record instead of
	#listen
	audio = r.record(source) 

try:
	print("The audio file contains: " + r.recognize_google(audio))

except sr.UnknownValueError:
	print("Recognition could not understand audio")

except sr.RequestError as e:
	print("Could not request results from Recognition service; {0}".format(e))

name = r.recognize_google(audio) #this is an attributes for storing the speech that we transformed into text

#here we gonna translate speech to text into another language using the google traduction api 

translator= Translator(to_lang="fr") # you can define the language you wanna translate the speech to text
translation = translator.translate(name)
print (translation)

#we gonna transform here text to speech 
tts = gTTS(text= translation, lang='fr', slow=False)
tts.save("hello.mp3")

os.chdir("") #put here the directory where the file will be opened 
os.system("hello.mp3")# we gonna open the file of text to speech translated to another language 


