
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pdb

class DAQGUI:
    def __init__(self):
        self.root = Tk()
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()
        self.current_row = 0
        self.root.geometry('1000x400') 

    def add_label(self,text,settings_field):
        label = ttk.Label(self.frm, text=text)
        label.grid(column=0, row=self.current_row)
        setattr(self,settings_field+'_label',label)
        self.current_row = self.current_row+1
    
    def add_labeled_entry(self,text,settings_field):
        self.add_label(text,settings_field)
        self.add_entry(settings_field)

    def add_entry(self,settings_field):
        entry = ttk.Entry(self.frm)
        entry.grid(column=0, row=self.current_row)
        setattr(self,settings_field+'_entry',entry)
        self.current_row = self.current_row+1
    
    def update_frame_label(self,framei):
        self.frame_label.configure(text=f"Frame {framei}")

    def main(self,start_function = lambda :...,end_function = lambda :...):
        self.add_label('Frame 0','frame')
        self.add_labeled_entry('Frame Duration','binduration')
        self.add_labeled_entry('Stimulation Voltage','StimV')
        self.add_labeled_entry('Stimulation Hertz','stimHZ')
        self.add_labeled_entry('Number of Frames Before Stimulation','prestim_frames')
        self.add_labeled_entry('Number of Channels','n_channels')
        self.add_labeled_entry('Number of Frames During Stimulation','stim_frames')
        self.add_labeled_entry('Number of Frames After Stimulation','poststim_frames')
        self.add_button('Start',start_function)
        self.add_button('Stop',end_function)
        self.add_button('Exit',self.root.destroy)
        self.root.mainloop()

    def add_button(self,text,function):
        ttk.Button(self.frm, text=text, command=function).grid(column=0, row=self.current_row)
        self.current_row = self.current_row+1
    
    def update_image(self,image,title):
        img =  ImageTk.PhotoImage(image=Image.fromarray(image))
        self.label.imgtk = img
        self.label.configure(image=img, text=title)

    def add_image(self,image):
        img =  ImageTk.PhotoImage(image=Image.fromarray(image))
        self.label = ttk.Label(self.frm,text="your image here", compound="top")
        self.label.grid(column=1,row=0,rowspan=20)
        self.label.imgtk = img
        self.label.configure(image=img, text="Camera")
        return img