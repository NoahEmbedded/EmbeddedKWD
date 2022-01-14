from pydub import AudioSegment as AS
from random import randint
from os import listdir
def fuse(in0,in1,out):
    sound0 = AS.from_wav(in0)
    sound1 = AS.from_wav(in1)
    kombi_sound = sound0 + sound1
    if len(kombi_sound) < 2000:
        kombi_sound = kombi_sound + AS.silent(duration=(2000-len(kombi_sound)),frame_rate=16000)
    kombi_sound.export(out, format="wav")

pfad_corpus = "/home/noah/Schreibtisch/Bachelorarbeit/speechcommandCorpus/"
pfad_random_noise = "/home/noah/Schreibtisch/Bachelorarbeit/speechcommandCorpus/random_noise/"
worte = ["bed/","bird/","cat/","dog/","down/","eight/","five/","four/","happy/","house/","left/","nine/","no/","off/","on/","one/","right/","seven/"]
corpus_liste = []
for wort in worte:
    wort_liste = listdir(pfad_corpus+wort)
    corpus_liste.append(wort_liste)
for i in range(0,1800):
    wort_0_index = randint(0,17)
    sample_0_index = randint(0,len(corpus_liste[wort_0_index])-1)
    wort_1_index = randint(0,17)
    sample_1_index = randint(0,len(corpus_liste[wort_1_index])-1)
    wort_0 = pfad_corpus + worte[wort_0_index] + corpus_liste[wort_0_index][sample_0_index]
    wort_1 = pfad_corpus + worte[wort_1_index] + corpus_liste[wort_1_index][sample_1_index]
    out_pfad = pfad_random_noise + "noise" + str(i) + ".wav"
    fuse(wort_0,wort_1,out_pfad)