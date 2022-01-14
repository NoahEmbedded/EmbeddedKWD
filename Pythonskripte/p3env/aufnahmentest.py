import pyaudio
import numpy
import queue
class aufnahme:
    #Interne Variablen
    nimmt_auf = False
    frame_fifo = queue.Queue()
    aufnahmestream = None
    def __init__(self):
        #Konstruktorkram
        self.nimmt_auf = False
        self.frame_fifo = queue.Queue()
        self.aufnahmestream = None
    def callback(self, in_data, frame_count, time_info, status):
        if self.nimmt_auf:
            self.frame_fifo.put(in_data)
            return in_data, pyaudio.paContinue
        else:
            return in_data,pyaudio.paComplete