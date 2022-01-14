import os
import sys
from pydub import AudioSegment as AS 
ordner = str(sys.argv[1])
pfad = '/home/noah/Schreibtisch/Bachelorarbeit/speechcommandCorpus/'+ordner+'/'
namen = os.listdir(pfad)
genau1=0
kleiner1=0
groesser1=0
for i in namen:
    temp = AS.from_file(pfad+i,format = "wav")
    if(len(temp)>1000):
        groesser1+=1
    elif len(temp)==1000:
        genau1+=1
    else:
        kleiner1+=1
print("kuerzer als 1 sek:"+str(kleiner1)+"\ngenau 1 sek:"+str(genau1)+"\nlaenger als 1 sek:"+str(groesser1))

