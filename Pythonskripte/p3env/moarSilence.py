from pydub import AudioSegment as AS
stille = AS.silent(duration = 2000,frame_rate = 16000)
pfad = "/home/noah/Schreibtisch/Bachelorarbeit/speechcommandCorpus/sehr_ruhig/"
for i in range(1800):
    stille.export(pfad + "stille" + str(i) +".wav", format="wav")
