import tensorflow.keras.models
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from numpy import array,expand_dims,mean,median
from os import listdir
def ladeBild(pfad):
    bild = load_img(path = pfad,color_mode = 'grayscale')
    array = img_to_array(bild)
    array = expand_dims(array,axis = 0)
    return array
model = tensorflow.keras.models.load_model("model.h5")
pfad_marvin = "D:\Bachelorarbeit\Spektrogramme_MarvinGo"
pfad_noise = "D:\Bachelorarbeit\Spektrogramme_Noise"
pfad_ruhe = "D:\Bachelorarbeit\Spektrogramme_Stille"

liste_daten_marvin = listdir(pfad_marvin)[-300:]
liste_daten_noise = listdir(pfad_noise)[-300:]
liste_daten_ruhe = listdir(pfad_ruhe)[-300:]


#Teste Noise
print("\n\ninput = Noise")
marvin50 = 0
marvin70 = 0
marvin90 = 0
noise50 = 0
noise70 = 0
noise90 = 0
ruhe50 = 0
ruhe70 = 0
ruhe90 = 0
#0 noise 1 marvin 2 ruhe
for noise in liste_daten_noise:
    pruefling = ladeBild(pfad_noise+"/"+noise)
    ergebnis = model.predict(pruefling)
    if(ergebnis[0][0]>=0.5):
        noise50+=1
    if(ergebnis[0][0]>=0.7):
        noise70+=1
    if(ergebnis[0][0]>=0.9):
        noise90+=1

    if(ergebnis[0][1]>=0.5):
        marvin50+=1
    if(ergebnis[0][1]>=0.7):
        marvin70+=1
    if(ergebnis[0][1]>=0.9):
        marvin90+=1
    
    if(ergebnis[0][2]>=0.5):
        ruhe50+=1
    if(ergebnis[0][2]>=0.7):
        ruhe70+=1
    if(ergebnis[0][2]>=0.9):
        ruhe90+=1

print("marvin erkannt(50%,70%,90%):",marvin50,marvin70,marvin90)
print("noise erkannt(50%,70%,90%):",noise50,noise70,noise90)
print("ruhe erkannt(50%,70%,90%):",ruhe50,ruhe70,ruhe90)
#Teste Marvin
print("\n\ninput = marvin")
marvin50 = 0
marvin70 = 0
marvin90 = 0
noise50 = 0
noise70 = 0
noise90 = 0
ruhe50 = 0
ruhe70 = 0
ruhe90 = 0
#0 noise 1 marvin 2 ruhe
for marvin in liste_daten_marvin:
    pruefling = ladeBild(pfad_marvin+"/"+marvin)
    ergebnis = model.predict(pruefling)
    if(ergebnis[0][0]>=0.5):
        noise50+=1
    if(ergebnis[0][0]>=0.7):
        noise70+=1
    if(ergebnis[0][0]>=0.9):
        noise90+=1

    if(ergebnis[0][1]>=0.5):
        marvin50+=1
    if(ergebnis[0][1]>=0.7):
        marvin70+=1
    if(ergebnis[0][1]>=0.9):
        marvin90+=1
    
    if(ergebnis[0][2]>=0.5):
        ruhe50+=1
    if(ergebnis[0][2]>=0.7):
        ruhe70+=1
    if(ergebnis[0][2]>=0.9):
        ruhe90+=1
print("Marvin erkannt(50%,70%,90%):",marvin50,marvin70,marvin90)
print("noise erkannt(50%,70%,90%):",noise50,noise70,noise90)
print("ruhe erkannt(50%,70%,90%):",ruhe50,ruhe70,ruhe90)
#Teste Ruhe
print("\n\ninput = ruhe")
marvin50 = 0
marvin70 = 0
marvin90 = 0
noise50 = 0
noise70 = 0
noise90 = 0
ruhe50 = 0
ruhe70 = 0
ruhe90 = 0
#0 noise 1 marvin 2 ruhe
for ruhe in liste_daten_ruhe:
    pruefling = ladeBild(pfad_ruhe+"/"+ruhe)
    ergebnis = model.predict(pruefling)
    if(ergebnis[0][0]>=0.5):
        noise50+=1
    if(ergebnis[0][0]>=0.7):
        noise70+=1
    if(ergebnis[0][0]>=0.9):
        noise90+=1

    if(ergebnis[0][1]>=0.5):
        marvin50+=1
    if(ergebnis[0][1]>=0.7):
        marvin70+=1
    if(ergebnis[0][1]>=0.9):
        marvin90+=1
    
    if(ergebnis[0][2]>=0.5):
        ruhe50+=1
    if(ergebnis[0][2]>=0.7):
        ruhe70+=1
    if(ergebnis[0][2]>=0.9):
        ruhe90+=1
print("Marvin erkannt(50%,70%,90%):",marvin50,marvin70,marvin90)
print("noise erkannt(50%,70%,90%):",noise50,noise70,noise90)
print("ruhe erkannt(50%,70%,90%):",ruhe50,ruhe70,ruhe90)

