import tensorflow as tf
from tensorflow.keras.models import load_model
model = load_model("model.h5")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tfmodel = converter.convert() 
open ("model.tflite" , "wb") .write(tfmodel)
print("\n Fertig \n")
