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
from glob import glob
chunk = 1024  
camera = PiCamera()
button = Button(17)
now = datetime.now()
data = ''
file_name=''
def take_photo():
    global data,chunk
    camera.start_preview()
    sleep(2)
    path_file = "photo.jpg"
    camera.capture(path_file)
    camera.stop_preview()
    myfile = {'myfile': open(path_file, 'rb')}
    url = "http://e0db209c.ngrok.io"
    im = Image.open(path_file)
    w,h = im.size
    first = w*(1/3)
    second = w*(2/3)
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
    clases = glob("mp3/*")
    detection = [data["object_detection"],data["face recognition"]]
    sent1,sent2,sent3="in left ","in front ", "in right "
    for typ in detection: 
        for obj in typ:
            center_x = ((obj["right"]-obj["left"])/2)+obj["left"]
            if center_x<= first:
                sent1 +=  obj["class_name"]+" "
            elif center_x<= second:
                sent2 +=  obj["class_name"]+" "
            else:
                sent3 +=  obj["class_name"]+" "
    sentens = [sent1,sent2,sent3]
    for typ in sentens:
        data= []
        lis_str = typ.split()
        print(lis_str)
        if len(lis_str) ==2:
            continue
        for ind,obj in enumerate(lis_str):
            if obj == " ":
                continue
            if not "mp3/"+obj+".mp3" in clases:
                print(obj)
                tts_obj = gTTS(text=obj,lang="en")
                tts_obj.save("mp3/"+obj+".mp3")
                sound = AudioSegment.from_mp3("mp3/"+obj+".mp3")
                sound.export("wav/"+obj+".wav", format="wav")
            if ind == (len(lis_str)-1):
                if not "mp3/"+"and"+".mp3" in clases:
                    tts_obj = gTTS(text="and",lang="en")
                    tts_obj.save("mp3/"+"and"+".mp3")
                    sound = AudioSegment.from_mp3("mp3/"+"and"+".mp3")
                    sound.export("wav/"+"and"+".wav", format="wav")
                
                w = wave.open("wav/"+"and"+".wav", 'rb')
                data.append( [w.getparams(), w.readframes(w.getnframes())] )
                w.close()    
            w = wave.open("wav/"+obj+".wav", 'rb')
            data.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()
        output = wave.open("sentens.wav", 'wb')
        output.setparams(data[0][0])
        for params,frames in data:
            output.writeframes(frames)
        output.close()
        f = wave.open(r"sentens.wav","rb")
        #instantiate PyAudio
        p = pyaudio.PyAudio()
        #instantiate PyAudio  
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
