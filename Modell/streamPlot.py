import sounddevice as sd
import time
import numpy as np
import pygame

"""
Funktions- und Klassendefinitionen
"""
#Queue-Artige Liste, kann vollständigen inhalt als numpyarray ausgeben
class schlange:
    def __init__(self,max_groesse):
        self.__max_groesse = max_groesse
        self.__voll = False
        self.__liste = []
    #anhaengen: hänge ein objekt an die Schlange an, wenn die Liste dadurch zu groß wird, lösche den ältesten eintrag
    def anhaengen(self,ding):
        self.__liste.append(ding)
        if len(self.__liste) > self.__max_groesse:
            self.__voll=True
            self.__liste.pop(0)
    #get_liste: gib die komplette liste als numpy array aus
    def get_liste(self):
        return np.array(self.__liste)
    #nullen: setze alle Werte der Schlange auf 0
    def nullen(self):
        for i in range(len(self.__liste)):self.__liste[i]=0
    def ist_voll(self):
        return self.__voll

#fuehrt eine FFT bzw DFT auf einem bereits gefensterten datenslice aus(abhaengig von der Slicegroesse) und binned das ergebnis
def fft_auf_slice_binned(daten,slicegroesse,bingroesse):
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
    return slice_FFT

def pygameBild(bild,screen,framerate):
    bild = (bild/255).astype(np.uint8)#zu unsigned 8 bit 
    bild = np.stack((bild,bild,bild), axis=2)#"rgb"-bild fuer pygame
    screen.fill((255, 255, 255))
    surface = pygame.surfarray.make_surface(bild)
    screen.blit(surface,(100,100))
    pygame.display.flip()
    clock.tick(framerate)

def pygame_beenden():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False
#Erstelle ein Fenster und starte 
def pygame_init(breite,hoehe):
    pygame.init()
    pygame.display.set_caption('Echtzeitspektrogramm')
    screen = pygame.display.set_mode(size = (breite+2*100, hoehe+2*100))
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    return screen,clock

def callback(indata, frames,time, status):
    temp = np.array(indata).flatten()
    temp = np.multiply(temp,fenster).astype(np.int16)
    datenListe.append(temp)
    return indata,status


"""
Ab hier eigentlicher Programmablauf
"""

#Streamkonfig:
channelzahl = 1
blockgroesse = 512
dtype = np.int16
samplerate = 16384
Schluesselwortdauer = 2 #Sekunden
sliceanzahl = np.floor((Schluesselwortdauer * samplerate)/blockgroesse).astype(np.int16) # Ohne Ueberlappung
datenListe = []
fenster = np.hamming(blockgroesse)



#Starte Aufnahmestream
aufnahmeStream = sd.InputStream(samplerate=samplerate,
                                blocksize=blockgroesse,
                                channels=channelzahl,
                                dtype=dtype,
                                callback=callback)

aufnahmeStream.start()
#Pygame Konfiguration
screen,clock = pygame_init(breite=sliceanzahl,hoehe=int(blockgroesse/2))
done = False
#Starte Auswerteschleife
spektrogramm_schlange = schlange(sliceanzahl)
while not done:
    done = pygame_beenden()
    if len(datenListe) > 0:
        fft_Slice = fft_auf_slice(datenListe[0],blockgroesse)
        datenListe.pop(0)
        spektrogramm_schlange.anhaengen(fft_Slice.astype(np.int16))
        if spektrogramm_schlange.ist_voll(): 
            spektrogramm = spektrogramm_schlange.get_liste()#zu unsigned 8 bit 
            print(np.amin(spektrogramm))
            pygameBild(bild=spektrogramm,screen=screen,framerate=samplerate/blockgroesse)
    else : 
        print("warte auf stream")
        time.sleep(0.5)
aufnahmeStream.stop()  


