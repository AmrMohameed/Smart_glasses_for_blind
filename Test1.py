from picamera import PiCamera
from time import sleep
from datetime import datetime
from gpiozero import Button

camera = PiCamera()
button = Button(17)
now = datetime.now()
filename = ''
def take_photo():
    global filename
    filename = "amrrrr"
    camera.start_preview(alpha=190)
    sleep(1)
    camera.capture('example.jpg')
    camera.stop_preview()
    
button.when_pressed = take_photo
    from picamera import PiCamera
from time import sleep
from datetime import datetime
from gpiozero import Button

camera = PiCamera()
button = Button(17)
now = datetime.now()
filename = ''
def take_photo():
    global filename
    filename = "amrrrr"
    camera.start_preview(alpha=190)
    sleep(1)
    camera.capture('example.jpg')
    camera.stop_preview()
    
button.when_pressed = take_photo
    