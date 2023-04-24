import tkinter
from pylablib.devices import IMAQ
import numpy as np
from PIL import Image, ImageTk

camera = IMAQ.IMAQCamera('img0.iid')
camera.start_acquisition()

def get_image():
    data =  np.mean(camera.read_multiple_images(),axis=0)
    data = data-np.min(data)
    data = data/np.max(data)*255
    image =  ImageTk.PhotoImage(image=Image.fromarray(data))
    return image

self = tkinter.Tk()
self.label = tkinter.Label(text="your image here", compound="top")
self.label.pack(side="top", padx=8, pady=8)
self.iteration=0
self.delay=100
self.image = get_image()
self.label.configure(image=self.image, text="Iteration %s" % self.iteration)
self.mainloop()