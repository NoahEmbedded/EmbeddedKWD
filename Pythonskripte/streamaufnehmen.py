import sounddevice as sd
import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt



#Pyplot
plt.ion()
plt.show()

#Streamkonfig:
samplerate = 16000
channelzahl = 1
blockgroesse = 640
dtype = np.int16
datenListe = []
fenster = np.hamming(blockgroesse)
def callback(indata, frames,time, status):
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
time.sleep(2)
aufnahmeStream.stop()


print(datenListe[0])



'''
plt.clf()
plt.plot(binned_slice)
plt.draw()
plt.pause(0.02)

zaehler+=1
img = Image.fromarray(spektrogramm,mode = 'I;16')
img.save(speicherpfad+"V"+str(zaehler)+".png")
'''
