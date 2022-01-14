#-------------------------------------------------------------------------------------------------#
#Trainingsdaten reinladen
#-------------------------------------------------------------------------------------------------#
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from tensorflow.keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint
from numpy import array
from os import listdir
#ladeBilde(pfad) lädt das Bild vom angegebenen Pfad und wandelt die daten in ein numpy-array um
def ladeBild(pfad):
    bild = load_img(path = pfad,color_mode = 'grayscale')
    array = img_to_array(bild)
    return array
trainingsdaten = []
trainingslabel = []
pfadNoiseBilder = "D:\Bachelorarbeit\Spektrogramme_Noise"
pfadMarvinGoBilder = "D:\Bachelorarbeit\Spektrogramme_MarvinGo"
pfadStilleBilder = "D:\Bachelorarbeit\Spektrogramme_Stille"
AnzahlSamplesProArt = 1800
dateienListeNoise = listdir(pfadNoiseBilder)
dateienListeMarvinGo = listdir(pfadMarvinGoBilder)
dateienListeStille = listdir(pfadStilleBilder)

for zaehler in range(AnzahlSamplesProArt):
    tempDaten = ladeBild(pfadNoiseBilder + "/" + dateienListeNoise[zaehler])
    trainingsdaten.append(tempDaten)
    trainingslabel.append(0)
    tempDaten = ladeBild(pfadMarvinGoBilder + "/" + dateienListeMarvinGo[zaehler])
    trainingsdaten.append(tempDaten)
    trainingslabel.append(1)
    tempDaten = ladeBild(pfadStilleBilder + "/" + dateienListeStille[zaehler])
    trainingsdaten.append(tempDaten)
    trainingslabel.append(2)
trainingslabel = to_categorical(trainingslabel)#liste zu one-hot-matrix
trainingsdaten = array(trainingsdaten)

#-------------------------------------------------------------------------------------------------#
#----------------------------------------Modellbeschreibung---------------------------------------#
#-------------------------------------------------------------------------------------------------#
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, AveragePooling2D
#Faltungsschichten und Pooling
layer0 = Conv2D(filters = 20,kernel_size = (3,6),input_shape = (62, 256, 1),activation = 'relu')
layer1 = MaxPooling2D(pool_size = (4,4))
layer2 = Conv2D(filters = 15,kernel_size = (3,6),activation = 'relu')
layer3 = MaxPooling2D(pool_size = (5,5))
layer4 = Flatten()
layer5 = Dense(30,activation = 'relu')
layer6 = Dense(60,activation = 'relu')
layer7 = Dense(3,activation = 'softmax')
 
#Zusammenbauen
model = Sequential()
model.add(layer0) 
model.add(layer1)
model.add(layer2)
model.add(layer3)
model.add(layer4)
model.add(layer5)
model.add(layer6)
model.add(layer7)

#Zusammenfassung anzeigen
model.summary()
#Modell kompilieren
from tensorflow.keras.optimizers import Adam
optimierer = Adam(lr=0.00001)
model.compile(
    loss='categorical_crossentropy',
    optimizer=optimierer,
    metrics=['accuracy']
)
filepath = "model.h5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

#-------------------------------------------------------------------------------------------------#
#------------------------------------------Modelltraining-----------------------------------------#
#-------------------------------------------------------------------------------------------------#
model.fit(trainingsdaten,trainingslabel,batch_size=1800,epochs=2500,callbacks=callbacks_list)
model.save('./model.h5')
