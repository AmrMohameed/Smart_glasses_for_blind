from picamera import PiCamera
from time import sleep
from datetime import datetime
from gpiozero import Button
from io import BytesIO
from PIL import Image
import numpy as np
import requests
import pyaudio
from signal import pause
import wave
from gtts import gTTS
import os,sys
from pygame import mixer
import time
from pydub import AudioSegment

chunk = 1024  
camera = PiCamera()
button = Button(17)
now = datetime.now()
data = ''
def take_photo():
    global data,chunk
    camera.start_preview()
    sleep(2)
    path_file = "photo.jpg"
    camera.capture(path_file)
    camera.stop_preview()
    myfile = {'myfile': open(path_file, 'rb')}
    url = "http://ef5b9ce2.ngrok.io"
    #im = Image.open(path_file)
    #np_im = np.array(im) 
    try:
        re = requests.post(url=url, files=myfile)
    except TimeoutError:
        print("Connection timed out!")
    if re.status_code==200:
        print(re.status_code)
        data = re.json()
    else:
        print(re.status_code)
    print(data)
    for kind in data:
        print(data,kind)
        kind = data[kind]
        
        for cls in kind:
            print(cls)
            file_name = cls["class_name"]
            tts = gTTS(text=cls["class_name"],lang="en")
            tts.save(file_name+".mp3")
            sound = AudioSegment.from_mp3(file_name+".mp3")
            sound.export(file_name+".wav", format="wav")
            f = wave.open(r""+file_name+".wav","rb")
            #instantiate PyAudio  
            p = pyaudio.PyAudio()  
            #open stream  
            stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  
            #read data  
            data = f.readframes(chunk)  

            #play stream  
            while data:  
                stream.write(data)  
                data = f.readframes(chunk)  

            #stop stream  
            stream.stop_stream()  
            stream.close()  

            #close PyAudio  
            p.terminate()
    #image = np_im[clas["top"]:clas["bottom"],clas["left"]:clas["right"]]
    #im = Image.fromarray(image)
    #im.show()
    
button.when_pressed = take_photo
pause()