import tkinter
from pylablib.devices import IMAQ
import numpy as np
from PIL import Image, ImageTk

camera = IMAQ.IMAQCamera('img0.iid')
camera.start_acquisition()
class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.label = tkinter.Label(text="your image here", compound="top")
        self.label.pack(side="top", padx=8, pady=8)
        self.iteration=0
        self.delay=10
        self.UpdateImage(self.delay)

    def UpdateImage(self, delay, event=None):
        self.iteration += 1
        self.image = self.get_image()
        self.label.configure(image=self.image, text="Iteration %s" % self.iteration)
        self.after(delay, self.UpdateImage, delay)

    def get_image(self):
        # data =  np.mean(camera.read_multiple_images(),axis=0)
        data =  camera.read_multiple_images()[0]
        # data = data-np.min(data)
        data = data/20
        image =  ImageTk.PhotoImage(image=Image.fromarray(data))
        return image

if __name__ == "__main__":
    app=App()
    app.mainloop()