from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
def ladeBild(pfad):
    bild = load_img(pfad,grayscale=True)
    array = img_to_array(bild)
    return array
