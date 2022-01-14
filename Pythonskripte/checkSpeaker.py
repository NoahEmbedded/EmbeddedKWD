import os
import sys
#Sprecherliste Marvin
sprecherMarvin=[]
marvin=os.listdir('/home/noah/Schreibtisch/Bachelorarbeit/speechcommandCorpus/marvin')
for i in marvin:
    i=i[:8]
    if i not in sprecherMarvin:
        sprecherMarvin.append(i)
#Sprecherliste anderer
name=str(sys.argv[1])
sprecherAnderer=[]
anderer=os.listdir('/home/noah/Schreibtisch/Bachelorarbeit/speechcommandCorpus/'+name)
for i in anderer:
    i=i[:8]
    if i not in sprecherAnderer:
        sprecherAnderer.append(i)
#Abgleich
anzahlGleiche=0
for i in sprecherMarvin:
    if i in sprecherAnderer:
        anzahlGleiche+=1
print(str(anzahlGleiche) + " gleiche Sprecher fuer Marvin und " + name + ". Sprecher Marvin: "+str(len(sprecherMarvin))+" Sprecher "+name+" "+str(len(sprecherAnderer)))