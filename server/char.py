import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import LabelEncoder

json_file = open('weights/character_recognition.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("weights/weight.h5")
print("[INFO] Model loaded successfully...")
labels = LabelEncoder()
labels.classes_ = np.load('weights/license_character_classes.npy')
print("[INFO] Labels loaded successfully...")

def detect(image):
    image = cv2.resize(image,(80,80))
    image = np.stack((image,)*3, axis=-1)
    prediction = labels.inverse_transform([np.argmax(model.predict(image[np.newaxis,:]))])
    return prediction 
