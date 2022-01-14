from pydub import AudioSegment as AS 
import sounddevice as sd 
from numpy import array,append,hamming,int16,delete
#fifo-queue
class schlange:
    def __init__(self,max_groesse):
        self.__max_groesse = max_groesse
        self.__liste = []
    def anhaengen(self,ding):
        self.__liste.append(ding)
        if len(self.__liste) > self.__max_groesse:
            self.__liste.pop(0)
    def get_liste(self):
        return array(self.__liste)
    def gefuellt(self):
        if len(self.__liste)==self.__max_groesse:
            return True
        else:
            return False
print("Starte Vorbereitung")
#Einstellungen für die Aufnahme
sd.default.samplerate = 16000
sd.default.channels = 1
aufnahmenlaenge_sek = 2 # in Sekunden
aufnahmenlaenge_werte = aufnahmenlaenge_sek*sd.default.samplerate # Anzahl Messwerte pro Aufnahme
#Einstellungen für die Bufferqueue

ueberlappung = 0.5
fensterlaenge_sek = 0.04 # in Sekunden
fensterlaenge_werte = fensterlaenge_sek*sd.default.samplerate# Anzahl Messwerte pro fft-fenster
anzahl_frames = int((aufnahmenlaenge_werte-fensterlaenge_werte)/(fensterlaenge_werte*(1-ueberlappung))) 
buffer_slices = schlange(anzahl_frames)
#Fenstereinstellungen
fenster = hamming(fensterlaenge_werte)
#Buffer für vorratsaufnahme
buffer_aufnahme = sd.rec(aufnahmenlaenge_werte*2,dtype = int16)#nehme 2 buffer lang im vorraus auf
sd.wait()
while(buffer_slices.)
print("Vorbereitung abgeschlossen")
while(True):
    hintergrund_aufnahme = sd.rec(aufnahmenlaenge_werte,dtype = int16)
    if(hintergrund_aufnahme.)












