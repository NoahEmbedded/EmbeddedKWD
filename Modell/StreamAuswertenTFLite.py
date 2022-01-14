import sounddevice as sd
import time
import numpy as np
import tensorflow as tf
"""
Funktions- und Klassendefinitionen
"""
#Queue-Artige Liste, kann vollständigen inhalt als numpyarray ausgeben
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

def fft_auf_slice_binned(daten,slicegroesse):
    slice_FFT = abs(np.fft.fft(daten,slicegroesse)[0:int(slicegroesse/2)])
    binned_slice = []
    iterator = 0
    bin_wert = 0
    for i in slice_FFT:
        if iterator > 4:
            binned_slice.append(bin_wert/5)
            iterator = 0                
            bin_wert = 0
        bin_wert += i
        iterator += 1
    binned_slice.append(bin_wert/5)
    binned_slice = np.array(binned_slice)
    return binned_slice

def fft_auf_slice(daten,slicegroesse):
    slice_FFT = abs(np.fft.fft(daten,slicegroesse)[0:int(slicegroesse/2)])
    slice_FFT = np.uint8(np.clip(slice_FFT,0,65535)/256)
    return slice_FFT

"""
Ab hier eigentlicher Programmablauf
"""
# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="final.tflite")
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#Streamkonfig:
Schluesselwortdauer = 2 #Sekunden
samplerate = 16000
channelzahl = 1
blockgroesse = 512
slicedauer = blockgroesse/samplerate # Sekunden
sliceanzahl = np.floor((Schluesselwortdauer * samplerate)/blockgroesse).astype(np.int16) # Ohne Ueberlappung
dtype = np.int16
datenListe = []
def callback(indata, frames,time, status):
    fenster = np.hamming(blockgroesse)
    temp = np.array(indata).flatten()
    temp = np.multiply(temp,fenster).astype(np.int16)
    datenListe.append(temp)
    return indata,status
    

#Starte Aufnahmestream
aufnahmeStream = sd.InputStream(samplerate=samplerate,
                                blocksize=blockgroesse,
                                channels=channelzahl,
                                dtype=dtype,
                                callback=callback)
aufnahmeStream.start()

#Starte Auswerteschleife
spektrogramm_schlange = schlange(sliceanzahl)
ergebnis_Marvin = schlange(sliceanzahl)
while True:
    if len(datenListe) > 0:
        fft_Slice = fft_auf_slice(datenListe[0],blockgroesse)
        datenListe.pop(0)
        spektrogramm_schlange.anhaengen(fft_Slice.astype(np.int16))
        if spektrogramm_schlange.ist_voll():
            spektrogramm = spektrogramm_schlange.get_liste().reshape(62, 256, 1)
            spektrogramm = np.expand_dims(spektrogramm,axis = 0)
            spektrogramm = spektrogramm.astype(np.float32)
            #inference des tflite modells
            interpreter.set_tensor(input_details[0]['index'], spektrogramm)
            interpreter.invoke()
            ergebnis = interpreter.get_tensor(output_details[0]['index'])

            ausgabe = [round(ergebnis[0][0],2),round(ergebnis[0][1],2),round(ergebnis[0][2],2)]
            print(ausgabe)
            '''
            ergebnis_Marvin.anhaengen(ergebnis[0][1])
            if ergebnis_Marvin.ist_voll():
                zaehler_marvin = 0
                for i in ergebnis_Marvin.get_liste():
                    if i >=0.7:
                        zaehler_marvin += 1
                if(zaehler_marvin)>=10:
                    print("Marvin Go erkannt")
                    ergebnis_Marvin.nullen()
            '''
            
    else : 
        print("idle - not enough data in stream yet")
        time.sleep(0.5)
aufnahmeStream.stop()    
