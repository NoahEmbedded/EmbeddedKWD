import csv
import time
import tensorflow as tf
import tensorflow.keras.models
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from numpy import expand_dims
from os import listdir

def ladeBild(pfad):
    bild = load_img(path = pfad,color_mode = 'grayscale')
    array = img_to_array(bild)
    array = expand_dims(array,axis = 0)
    return array

#Pfade Spektrogramme
pfadMarvin = "D:\Bachelorarbeit\Spektrogramme_MarvinGo"
pfadNoise = "D:\Bachelorarbeit\Spektrogramme_Noise"
pfadStille = "D:\Bachelorarbeit\Spektrogramme_Stille"

#dateilisten
listeDatenMarvin = listdir(pfadMarvin)[-300:]
listeDatenNoise = listdir(pfadNoise)[-300:]
listeDatenStille = listdir(pfadStille)[-300:]


#Tabellenkopfzeilen
headerNoise = ["Input = Sprache","Sprache in %","Marvin Go in %","Stille in %","Inferenzdauer in ms"]
headerMarvinGo = ["Input = Marvin Go","Sprache in %","Marvin Go in %","Stille in %","Inferenzdauer in ms"]
headerStille = ["Input = Stille","Sprache in %","Marvin Go in %","Stille in %","Inferenzdauer in ms"]
#Optimalwerte
ZielZeileNoise = ["Zielwert",100,0,0,"N/A"]
ZielZeileMarvin = ["Zielwert",0,100,0,"N/A"]
ZielZeileStille = ["Zielwert",0,0,100,"N/A"]

datenNoise = []#Input = Noise
datenMarvin = []#Input = Marvin
datenStille = []#Input = Stille
#############################################################
#                   Berechnung Tensorflow                   #
#############################################################
print("Starte Tensorflowinferenz\n")
model = tensorflow.keras.models.load_model("model.h5")
#input = Noise
i = 0
for noise in listeDatenNoise:
    pruefling = ladeBild(pfadNoise+"/"+noise)
    start = time.time()
    ergebnis = model.predict(pruefling)
    zeit = time.time()-start
    tempNoise = round(ergebnis[0][0]*100,2)
    tempMarvin = round(ergebnis[0][1]*100,2)
    tempStille = round(ergebnis[0][2]*100,2)
    datenNoise.append(["Sample{}".format(i),tempNoise,tempMarvin,tempStille,zeit*1000])
    i+=1
#input = Marvin
i = 0
for marvin in listeDatenMarvin:
    pruefling = ladeBild(pfadMarvin+"/"+marvin)
    start = time.time()
    ergebnis = model.predict(pruefling)
    zeit = time.time()-start
    tempNoise = round(ergebnis[0][0]*100,2)
    tempMarvin = round(ergebnis[0][1]*100,2)
    tempStille = round(ergebnis[0][2]*100,2)
    datenMarvin.append(["Sample{}".format(i),tempNoise,tempMarvin,tempStille,zeit*1000])
    i+=1
#input = Stille
i = 0
for stille in listeDatenStille:
    pruefling = ladeBild(pfadStille+"/"+stille)
    start = time.time()
    ergebnis = model.predict(pruefling)
    zeit = time.time()-start
    tempNoise = round(ergebnis[0][0]*100,2)
    tempMarvin = round(ergebnis[0][1]*100,2)
    tempStille = round(ergebnis[0][2]*100,2)
    datenStille.append(["Sample{}".format(i),tempNoise,tempMarvin,tempStille,zeit*1000])
    i+=1
print("Tensorflow Inferenz abgeschlossen\n")

#############################################################
#                      CSV Tensorflow                       #
#############################################################
with open('tf.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = "\n")
    #Input = Sprache
    print("Sprache\n")
    writer.writerow(headerNoise)
    writer.writerow(ZielZeileNoise)
    writer.writerows(datenNoise)
    writer.writerow("")
    #Input = Marvin Go
    print("Marvin\n")
    writer.writerow(headerMarvinGo)
    writer.writerow(ZielZeileMarvin)
    writer.writerows(datenMarvin)
    writer.writerow("")
    #Input = Stille
    print("Stille\n")
    writer.writerow(headerStille)
    writer.writerow(ZielZeileStille)
    writer.writerows(datenStille)
    writer.writerow("")
file.close()

datenNoise = []#Input = Noise
datenMarvin = []#Input = Marvin
datenStille = []#Input = Stille

#############################################################
#                Berechnung Tensorflow Lite                 #
#############################################################
print("Starte Tensorflow Lite Inferenz\n")
# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

i = 0
for noise in listeDatenNoise:
    pruefling = ladeBild(pfadNoise+"/"+noise)
    start = time.time()
    interpreter.set_tensor(input_details[0]['index'], pruefling)
    interpreter.invoke()
    ergebnis = interpreter.get_tensor(output_details[0]['index'])
    zeit = time.time() - start
    tempNoise = round(ergebnis[0][0]*100,2)
    tempMarvin = round(ergebnis[0][1]*100,2)
    tempStille = round(ergebnis[0][2]*100,2)
    datenNoise.append(["Sample{}".format(i),tempNoise,tempMarvin,tempStille,zeit*1000])
    i+=1
i = 0
for marvin in listeDatenMarvin:
    pruefling = ladeBild(pfadMarvin+"/"+marvin)
    start = time.time()
    interpreter.set_tensor(input_details[0]['index'], pruefling)
    interpreter.invoke()
    ergebnis = interpreter.get_tensor(output_details[0]['index'])
    zeit = time.time() - start
    tempNoise = round(ergebnis[0][0]*100,2)
    tempMarvin = round(ergebnis[0][1]*100,2)
    tempStille = round(ergebnis[0][2]*100,2)
    datenMarvin.append(["Sample{}".format(i),tempNoise,tempMarvin,tempStille,zeit*1000])
    i+=1
i = 0
for stille in listeDatenStille:
    start = time.time()
    interpreter.set_tensor(input_details[0]['index'], pruefling)
    interpreter.invoke()
    ergebnis = interpreter.get_tensor(output_details[0]['index'])
    zeit = time.time() - start
    tempNoise = round(ergebnis[0][0]*100,2)
    tempMarvin = round(ergebnis[0][1]*100,2)
    tempStille = round(ergebnis[0][2]*100,2)
    datenStille.append(["Sample{}".format(i),tempNoise,tempMarvin,tempStille,zeit*1000])
    i+=1
print("Tensorflow Lite Inferenz abgeschlossen\n")
#############################################################
#                    CSV Tensorflow Lite                    #
#############################################################
with open('tfLite.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = "\n")
    #Input = Sprache
    print("Sprache\n")
    writer.writerow(headerNoise)
    writer.writerow(ZielZeileNoise)
    writer.writerows(datenNoise)
    writer.writerow("")
    #Input = Marvin Go
    print("Marvin\n")
    writer.writerow(headerMarvinGo)
    writer.writerow(ZielZeileMarvin)
    writer.writerows(datenMarvin)
    writer.writerow("")
    #Input = Stille
    print("Stille\n")
    writer.writerow(headerStille)
    writer.writerow(ZielZeileStille)
    writer.writerows(datenStille)
    writer.writerow("")
file.close()
print("CSV erstellen Abgeschlossen\n")