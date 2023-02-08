import tkinter as tk
from PyAq import PyAq

def add_labeled_input_field(window,label_string,default_value):
    label = tk.Label(text = label_string)
    v = tk.StringVar(window, value=default_value)
    input = tk.Entry(textvariable=v)
    label.pack()
    input.pack()
    return input

def start_experiment(pres_tim,stim,post_stm,bin_duration,stimv,stimhz,output_rate):
    settings = dict()
    settings['prestim_frames']=int(pres_tim)
    settings['stim_frames']=int(stim)
    settings['poststim_frames']=int(post_stm)
    settings['binduration']=float(bin_duration)
    settings['StimV']=int(stimv)
    settings['stimHZ']=int(stimhz)
    settings['output_rate']=int(output_rate)
    aq = PyAq(settings)
    aq.start()

def add_button(window,button_text,call_back):
    button = tk.Button(master=window, text=button_text,command=call_back)
    button.pack()

window = tk.Tk()
pres_tim = add_labeled_input_field(window,'Prestim frames','10')
stim = add_labeled_input_field(window,'stim frames','10')
post_stm = add_labeled_input_field(window,'Poststim frames','10')
bin_duration = add_labeled_input_field(window,'bin duration','0.1')
stimv = add_labeled_input_field(window,'StimV','1')
stimhz = add_labeled_input_field(window,'stimHZ','10')
output_rate = add_labeled_input_field(window,'output_rate','2000')
add_button(window,'Start',lambda: start_experiment(pres_tim.get(), stim.get(), \
    post_stm.get(), bin_duration.get(), stimv.get(), stimhz.get(),output_rate.get()))
# add_button(window,'End')
window.mainloop()