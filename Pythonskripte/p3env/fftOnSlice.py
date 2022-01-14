from pydub import AudioSegment as AS 
from PIL import Image
import numpy as np
import os

def spektrogramm_von_pfad_binned(pfad):
    audiogesamt=AS.from_wav(pfad)
    spektrogramm = []
    start = 0
    ende = 40
    anzahl_frame_werte = 0.04*audiogesamt.frame_rate
    fenster = np.hamming(anzahl_frame_werte)
    while(ende <= len(audiogesamt)):
        tempSlice = audiogesamt[start:ende]
        rohDaten = tempSlice.raw_data
        daten = np.frombuffer(rohDaten,dtype=np.int16)
        daten = daten*fenster
        sliceFFT = abs(np.fft.fft(daten,anzahl_frame_werte)[0:int(anzahl_frame_werte/2)])
        iterator = 0
        bin_wert = 0
        binned_slice = []
        for i in sliceFFT:
            if iterator > 4:
                binned_slice.append(bin_wert/5)
                iterator = 0
                bin_wert = 0
            bin_wert += i
            iterator += 1
        binned_slice.append(bin_wert/5)
        binned_slice = np.array(binned_slice)
        spektrogramm.append(binned_slice)
        start += 20
        ende += 20
    return spektrogramm

def spektrogramm_von_pfad(pfad,blockgroesse):
    audiogesamt=AS.from_wav(pfad)
    spektrogramm = []
    rohDaten = audiogesamt.raw_data
    daten = np.frombuffer(rohDaten,dtype=np.int16)
    fenster = np.hamming(blockgroesse)
    start = 0
    ende = blockgroesse
    while(ende<len(daten)):
        teildaten = daten[start:ende]
        teildaten = teildaten*fenster
        teildaten_FFT = abs(np.fft.fft(teildaten,blockgroesse)[0:int(blockgroesse/2)])
        spektrogramm.append(teildaten_FFT)
        start += blockgroesse
        ende += blockgroesse
    return np.array(spektrogramm)

#Noise
pfad_wav = "D:/Bachelorarbeit/speechcommandCorpus/random_noise"
pfad_spektrogramme = "D:/Bachelorarbeit/Spektrogramme_Noise"
blockgroesse = 512
wav_liste = os.listdir(pfad_wav)
print("Beginne Spektrogrammerstellung Noise")
for sample in wav_liste:
    pfad_input = pfad_wav + "/" + sample
    pfad_output = pfad_spektrogramme + "/" + sample[:-4] + ".png"
    spektro = spektrogramm_von_pfad(pfad_input,blockgroesse)
    hoehe,breite = spektro.shape
    for i in range(hoehe):
        for j in range(breite):
            if(spektro[i,j]>65535):
                spektro[i,j]=65535
            spektro[i,j]=np.uint8(spektro[i,j]/256)
    bild = Image.fromarray(spektro)
    bild.convert("L").save(pfad_output)
print("Noise fertig!")
#Marvin
pfad_wav = "D:/Bachelorarbeit/speechcommandCorpus/marvin_go"
pfad_spektrogramme = "D:/Bachelorarbeit/Spektrogramme_MarvinGo"
blockgroesse = 512
wav_liste = os.listdir(pfad_wav)
print("Beginne Spektrogrammerstellung MarvinGo")
for sample in wav_liste:
    pfad_input = pfad_wav + "/" + sample
    pfad_output = pfad_spektrogramme + "/" + sample[:-4] + ".png"
    spektro = spektrogramm_von_pfad(pfad_input,blockgroesse)
    hoehe,breite = spektro.shape
    for i in range(hoehe):
        for j in range(breite):
            if(spektro[i,j]>65535):
                spektro[i,j]=65535
            spektro[i,j]=np.uint8(spektro[i,j]/256)
    bild = Image.fromarray(spektro)
    bild.convert("L").save(pfad_output)
print("MarvinGo fertig!")
#Silence
pfad_wav = "D:/Bachelorarbeit/speechcommandCorpus/sehr_ruhig"
pfad_spektrogramme = "D:/Bachelorarbeit/Spektrogramme_Stille"
blockgroesse = 512
wav_liste = os.listdir(pfad_wav)
print("Beginne Spektrogrammerstellung Stille")
for sample in wav_liste:
    pfad_input = pfad_wav + "/" + sample
    pfad_output = pfad_spektrogramme + "/" + sample[:-4] + ".png"
    spektro = spektrogramm_von_pfad(pfad_input,blockgroesse)
    hoehe,breite = spektro.shape
    for i in range(hoehe):
        for j in range(breite):
            if(spektro[i,j]>65535):
                spektro[i,j]=65535
            spektro[i,j]=np.uint8(spektro[i,j]/256)
    bild = Image.fromarray(spektro)
    bild.convert("L").save(pfad_output)
print("Stille fertig!")