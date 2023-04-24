
from tkinter import *
from tkinter import ttk
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class DAQGUI:
    def __init__(self):
        self.root = Tk()
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()
        self.current_row = 0
        self.root.geometry('800x350') 

    def add_entry(self,text):
        ttk.Label(self.frm, text=text).grid(column=0, row=self.current_row)
        ttk.Entry(self.frm).grid(column=0, row=self.current_row+1)
        self.current_row = self.current_row+2

    def main(self):
        self.add_entry('Frame Duration')
        self.add_entry('Stimulation Voltage')
        self.add_entry('Stimulation Hertz')
        self.add_entry('Number of Frames Before Stimulation')
        self.add_entry('Number of Frames During Stimulation')
        self.add_entry('Number of Frames After Stimulation')
        self.add_button('Start',lambda :...)
        self.add_button('Stop',lambda :...)
        self.add_button('Exit',self.root.destroy)
        # img = self.add_image()
        self.root.mainloop()

    def add_button(self,text,function):
        ttk.Button(self.frm, text=text, command=function).grid(column=0, row=self.current_row)
        self.current_row = self.current_row+1

    def add_image(self,image):
        img =  ImageTk.PhotoImage(image=Image.fromarray(image))
        self.label = ttk.Label(self.frm,text="your image here", compound="top")
        self.label.grid(column=1,row=0,rowspan=20)
        self.label.configure(image=img, text="Camera")
        return img