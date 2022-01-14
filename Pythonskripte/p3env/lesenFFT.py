from pydub import AudioSegment as AS 
import numpy as np
from numpy.fft import fft
import matplotlib.pyplot as plt

pfad = "/home/noah/Schreibtisch/Bachelorarbeit/speechcommandCorpus/marvin/0a7c2a8d_nohash_0.wav"
test = AS.from_wav(pfad)
rohDaten=test.raw_data
daten = np.frombuffer(rohDaten,dtype=np.int16)
fig = plt.figure()
plt.plot(daten)
fig.savefig('roh.png', bbox_inches='tight')
frequenzen = fft(daten)
fig = plt.figure()
haelfte=int(len(frequenzen)/2)
plt.plot(abs(frequenzen[:haelfte]))
fig.savefig('fft.png', bbox_inches='tight')

