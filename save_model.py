import tensorflow as tf
from tensorflow.keras.applications import ResNet50
import bentoml
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

model = ResNet50(weights="imagenet")
img_path = 'fish.png'

img = image.load_img(img_path, target_size=(224, 224))

x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

preds = model.predict(x)
print('Keras Predicted:', decode_predictions(preds, top=3)[0])

bentoml.keras.save_model("keras_resnet50", model)
