from gtts import gTTS
import os,sys
from pygame import mixer
import time
start_time = time.time()

tts = gTTS(text=("Hello World"),lang="en")
tts.save("voice.wav")
print("start")

print("done")
print(str(time.time-start_time))