import sounddevice as sd
from PIL import Image
import time
import numpy as np
import tensorflow as tf
class schlange:
    def __init__(self,max_groesse):
        self.__max_groesse = max_groesse
        self.__voll = False
        self.__liste = []
    def anhaengen(self,ding):
        self.__liste.append(ding)
        if len(self.__liste) > self.__max_groesse:
            self.__voll=True
            self.__liste.pop(0)
    def get_liste(self):
        return np.array(self.__liste)
    def nullen(self):
        for i in range(len(self.__liste)):self.__liste[i]=0
    def ist_voll(self):
        return self.__voll

def fft_auf_slice(daten,slicegroesse):
    slice_FFT = abs(np.fft.fft(daten,slicegroesse)[0:int(slicegroesse/2)])
    slice_FFT = np.uint8(np.clip(slice_FFT,0,65535)/256)
    return slice_FFT

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="final.tflite")
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

Schluesselwortdauer = 2 #Sekunden
samplerate = 16000
channelzahl = 1
blockgroesse = 512
slicedauer = blockgroesse/samplerate # Sekunden
sliceanzahl = np.floor((Schluesselwortdauer * samplerate)/blockgroesse).astype(np.int16) # Ohne Ueberlappung
dtype = np.int16
datenListe = []

while(1):
    input("Press Enter to continue...")
    spektrogramm = []
    aufnahme = sd.rec(samplerate= samplerate,channels=channelzahl,dtype=dtype,frames=samplerate*2)
    sd.wait()
    aufnahme = aufnahme.flatten()
    fenster = np.hamming(blockgroesse)
    start = 0
    ende = blockgroesse
    while(ende<len(aufnahme)):
        teilaufnahme = aufnahme[start:ende]
        teilaufnahme = teilaufnahme*fenster
        teilaufnahme_FFT = abs(np.fft.fft(teilaufnahme,blockgroesse)[0:int(blockgroesse/2)])
        spektrogramm.append(teilaufnahme_FFT)
        start += blockgroesse
        ende += blockgroesse
    spektrogramm = np.array(spektrogramm)
    hoehe,breite = spektrogramm.shape
    for i in range(hoehe):
        for j in range(breite):
            if(spektrogramm[i,j]>65535):
                spektrogramm[i,j]=65535
            spektrogramm[i,j]=np.uint8(spektrogramm[i,j]/256)
    #bild = Image.fromarray(spektrogramm)
    #bild.show()
    spektrogramm = np.expand_dims(spektrogramm.reshape(62, 256, 1),axis = 0)
    spektrogramm = spektrogramm.astype(np.float32)
    interpreter.set_tensor(input_details[0]['index'], spektrogramm)
    interpreter.invoke()
    ergebnis = interpreter.get_tensor(output_details[0]['index'])
    print((ergebnis*100).astype(np.int))