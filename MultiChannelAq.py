import pdb
import time
import threading
import numpy as np
import threading
import nidaqmx
import pickle 
from pylablib.devices import IMAQ
from scipy import signal
from DAQGUI import DAQGUI

def snap_frame(camera,frames,i):
    frames[i] = np.mean(camera.read_multiple_images(),axis=0)

def get_image(camera):
    data =  np.mean(camera.read_multiple_images(),axis=0)
    data = data-np.min(data)
    data = data/np.max(data)*255
    return data

defalut_settings = {}
defalut_settings['prestim_frames']=10
defalut_settings['stim_frames']=10
defalut_settings['poststim_frames']=10
defalut_settings['binduration']=0.1
defalut_settings['StimV']=1
defalut_settings['stimHZ']=10
defalut_settings['output_rate']=2000
defalut_settings['n_channels'] = 3

class MultiChannelAq:
    def __init__(self,settings = defalut_settings):
        self.camera = IMAQ.IMAQCamera('img0.iid')
        self.camera.start_acquisition()
        self.gui = DAQGUI()
        self.load_settings(settings)
        self.triali = 1
        self.stop=False
        self.data = {}
        self.dir = r'C:\Users\dklab\Desktop\save_location'
        time.sleep(0.5)
        image = get_image(self.camera)
        self.gui.add_image(image)
        self.gui.main(self.start_experiment,self.stop_experiment)
        
    def load_settings(self,settings):
        self.prestim_frames = settings['prestim_frames']
        self.stim_frames = settings['stim_frames']
        self.poststim_frames = settings['poststim_frames']
        self.total_frames = self.prestim_frames+self.stim_frames+self.poststim_frames
        self.binduration = settings['binduration']
        self.total_time = self.total_frames*self.binduration
        self.pre_stim_time = self.prestim_frames*self.binduration
        self.stim_time = self.stim_frames*self.binduration
        self.StimV = settings['StimV']
        self.stimHZ = settings['stimHZ']
        self.output_rate= settings['output_rate']
    
    def plot_trial_result(self,result):
        self.gui.update_image(result,f'Trial {self.triali}')

    def monitor(self):
        starting_frame = [None]
        while True:
            time.sleep(0.5)
            snap_frame(self.camera,starting_frame,0)
            self.plot_trial_result(starting_frame[0])

    def generate_stim_output(self):
        output = np.zeros(int(self.total_time*self.output_rate))
        stim_start = int(self.pre_stim_time*self.output_rate)
        stim_Stop = int((self.pre_stim_time+self.stim_time)*self.output_rate)
        stim_length = stim_Stop-stim_start
        stim_cycle = self.output_rate/self.stimHZ
        t = np.linspace(0, 1, stim_length, endpoint=False)
        stim = signal.square(2 * np.pi * t * (stim_length/stim_cycle), duty=0.5)
        output[stim_start:stim_Stop]=stim
        return output

    def start_stimuli(self,wait = False):
        output = self.generate_stim_output()
        self.stim_task = nidaqmx.Task()
        self.stim_task.ao_channels.add_ao_voltage_chan('Dev1/ao1')
        self.stim_task.timing.cfg_samp_clk_timing(self.output_rate,samps_per_chan= len(output))
        self.stim_task.write(output)
        self.stim_task.start()
        if wait:
            self.stim_task.wait_until_done()

    def trial_clean_up(self):
        self.stim_task.stop()
        self.stim_task.close()

    def session_clean_up(self):
        self.camera.stop_acquisition()
        self.camera.close()
        pickle.save(self.dir )

    def acquire_image(self):
        frames = [None]*self.stim_frames
        threads = [None]*self.stim_frames
        for i in range(self.total_frames):
            if i>self.prestim_frames and i<(self.prestim_frames+self.stim_frames+1):
                threadi = i-self.prestim_frames-1
                threads[threadi] = threading.Thread(target=snap_frame,args = [self.camera,frames,threadi])
                threads[threadi].start()
            self.gui.update_frame_label(i)
            time.sleep(self.binduration)
        for threadi in threads:
            threadi.join()
        return frames
    
    def stop_experiment(self):
        self.stop = True

    def start_experiment(self):
        print('trial started')
        while ~self.stop:
            self.start_stimuli()
            frames = self.acquire_image()
            self.trial_clean_up()
            self.triali = self.triali+1
            self.data[self.triali] = frames
            self.plot_trial_result(frames[0])
            time.sleep(1)
        self.session_clean_up()
        print('done')