import requests
import sys
from PIL import Image
import numpy as np
import requests
#path_file = sys.argv[1]
myfile = {'myfile': open(path_file, 'rb')}
url = " http://44858c2d.ngrok.io"
im = Image.open(path_file)
np_im = np.array(im) 
try:
    re = requests.post(url=url, files=myfile)
except TimeoutError:
    print("Connection timed out!")
else:
    print(re.status_code)
print(re.json())
obj_dete = re.json()["object_detection"]
for clas in obj_dete:
    image = np_im[clas["top"]:clas["bottom"],clas["left"]:clas["right"]]
    im = Image.fromarray(image)
    im.show()