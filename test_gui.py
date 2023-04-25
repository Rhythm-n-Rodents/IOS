from DAQGUI import DAQGUI
from pylablib.devices import IMAQ
import numpy as np
import time

camera = IMAQ.IMAQCamera('img0.iid')
camera.start_acquisition()
time.sleep(1)
def get_image():
    data =  np.mean(camera.read_multiple_images(),axis=0)
    data = data-np.min(data)
    data = data/np.max(data)*255
    return data

image = get_image()
gui = DAQGUI()
# gui.add_image(image)
gui.main()