import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from numpy import array,expand_dims,mean,median
from os import listdir
def ladeBild(pfad):
    bild = load_img(path = pfad,color_mode = 'grayscale')
    array = img_to_array(bild)
    array = expand_dims(array,axis = 0)
    return array
pfad_marvin = "D:\Bachelorarbeit\Spektrogramme_MarvinGo"
pfad_noise = "D:\Bachelorarbeit\Spektrogramme_Noise"
pfad_ruhe = "D:\Bachelorarbeit\Spektrogramme_Stille"

liste_daten_marvin = listdir(pfad_marvin)[-300:]
liste_daten_noise = listdir(pfad_noise)[-300:]
liste_daten_ruhe = listdir(pfad_ruhe)[-300:]

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#Teste Noise
werte_marvin = []
werte_noise = []
werte_ruhe = []
#0 noise 1 marvin 2 ruhe
for noise in liste_daten_noise:
    pruefling = ladeBild(pfad_noise+"/"+noise)

    interpreter.set_tensor(input_details[0]['index'], pruefling)
    interpreter.invoke()
    ergebnis = interpreter.get_tensor(output_details[0]['index'])

    werte_noise.append(int(ergebnis[0][0]*100))
    werte_marvin.append(int(ergebnis[0][1]*100))
    werte_ruhe.append(int(ergebnis[0][2]*100))
print("\n\nTestdaten: Noise")
print("marvin durchschnitt:",mean(werte_marvin))
print("marvin median:",median(werte_marvin))    
# print("marvin maximum:",max(werte_marvin))
# print("marvin minimum:",min(werte_marvin))

print("\nnoise durchschnitt:",mean(werte_noise))
print("noise median:",median(werte_noise))    
# print("noise maximum:",max(werte_noise))
# print("noise minimum:",min(werte_noise))

print("\nruhe durchschnitt:",mean(werte_ruhe))
print("ruhe median:",median(werte_ruhe))    
# print("ruhe maximum:",max(werte_ruhe))
# print("ruhe minimum:",min(werte_ruhe))
#Teste Marvin
werte_marvin = []
werte_noise = []
werte_ruhe = []
#0 noise 1 marvin 2 ruhe
for marvin in liste_daten_marvin:
    pruefling = ladeBild(pfad_marvin+"/"+marvin)
    
    interpreter.set_tensor(input_details[0]['index'], pruefling)
    interpreter.invoke()
    ergebnis = interpreter.get_tensor(output_details[0]['index'])

    werte_noise.append(int(ergebnis[0][0]*100))
    werte_marvin.append(int(ergebnis[0][1]*100))
    werte_ruhe.append(int(ergebnis[0][2]*100))
print("\n\nTestdaten: Marvin")
print("\nmarvin durchschnitt:",mean(werte_marvin))
print("marvin median:",median(werte_marvin))    
# print("marvin maximum:",max(werte_marvin))
# print("marvin minimum:",min(werte_marvin))

print("\nnoise durchschnitt:",mean(werte_noise))
print("noise median:",median(werte_noise))    
# print("noise maximum:",max(werte_noise))
# print("noise minimum:",min(werte_noise))

print("\nruhe durchschnitt:",mean(werte_ruhe))
print("ruhe median:",median(werte_ruhe))    
# print("ruhe maximum:",max(werte_ruhe))
# print("ruhe minimum:",min(werte_ruhe))
#Teste Ruhe
werte_marvin = []
werte_noise = []
werte_ruhe = []
#0 noise 1 marvin 2 ruhe
for ruhe in liste_daten_ruhe:
    pruefling = ladeBild(pfad_ruhe+"/"+ruhe)
    
    interpreter.set_tensor(input_details[0]['index'], pruefling)
    interpreter.invoke()
    ergebnis = interpreter.get_tensor(output_details[0]['index'])

    werte_noise.append(int(ergebnis[0][0]*100))
    werte_marvin.append(int(ergebnis[0][1]*100))
    werte_ruhe.append(int(ergebnis[0][2]*100))
print("\n\nTestdaten: Ruhe")
print("\nmarvin durchschnitt:",mean(werte_marvin))
print("marvin median:",median(werte_marvin))    
# print("marvin maximum:",max(werte_marvin))
# print("marvin minimum:",min(werte_marvin))

print("\nnoise durchschnitt:",mean(werte_noise))
print("noise median:",median(werte_noise))    
# print("noise maximum:",max(werte_noise))
# print("noise minimum:",min(werte_noise))

print("\nruhe durchschnitt:",mean(werte_ruhe))
print("ruhe median:",median(werte_ruhe))    
# print("ruhe maximum:",max(werte_ruhe))
# print("ruhe minimum:",min(werte_ruhe))