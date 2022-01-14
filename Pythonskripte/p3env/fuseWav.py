from pydub import AudioSegment as AS
import os
def fuse(in0,in1,out):
    sound0 = AS.from_wav(in0)
    sound1 = AS.from_wav(in1)
    kombi_sound = sound0 + sound1
    if len(kombi_sound) < 2000:
        kombi_sound = kombi_sound + AS.silent(duration=(2000-len(kombi_sound)),frame_rate=16000)
    kombi_sound.export(out, format="wav")

pfad_marvin = "/home/noah/Schreibtisch/Bachelorarbeit/speechcommandCorpus/marvin"
pfad_go = "/home/noah/Schreibtisch/Bachelorarbeit/speechcommandCorpus/go"
pfad_marvin_go = "/home/noah/Schreibtisch/Bachelorarbeit/speechcommandCorpus/marvin_go"
marvin_wav_list = os.listdir(pfad_marvin)
go_wav_list = os.listdir(pfad_go)
#Iteriere über alle Dateinamen im angegebenen Verzeichnis der "Marvin"-Dateien
for marvin in marvin_wav_list:
    sprecher = marvin[:8]
    subset_go = []
    #Iteriere über alle Dateinamen im angegebenen Verzeichnis der "Go"-Dateien
    for go in go_wav_list:
        if go[:8] == sprecher:
            subset_go.append(go)
    #Fusioniere alle gefundenen "Go"-Dateien mit der momentanen "Marvin"-Datei
    pfad_input_0 = pfad_marvin + "/" + marvin
    zaehler = 0
    for go in subset_go:
        pfad_input_1 = pfad_go + "/" + go
        pfad_output = pfad_marvin_go + "/" + sprecher + "_" + marvin[-5] + "_" + str(zaehler) + ".wav" 
        zaehler += 1
        fuse(pfad_input_0,pfad_input_1,pfad_output)
    
