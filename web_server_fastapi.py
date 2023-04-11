from fastapi import FastAPI
from typing import Annotated
from PIL import Image
from fastapi import FastAPI, File, UploadFile
import io
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import settings
import uuid
import json
import helper_utilities
import redis
import time

app = FastAPI()
db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, db=settings.REDIS_DB)

@app.get("/")
def homepage():
	return "Welcome to the DISML project"


@app.post("/predict")
def predict(image: Annotated[bytes, File()]):
    data = {"success": False}
    image = Image.open(io.BytesIO(image))
    image = prepare_image(image, (settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT))
    image = image.copy(order="C")
    k = str(uuid.uuid4())
    image = helper_utilities.base64_encode_image(image)
    d = {"id": k, "image": image}
    db.rpush(settings.IMAGE_QUEUE, json.dumps(d))
    # keep looping until our model server returns the output
    # predictions
    while True:
        # attempt to grab the output predictions
        output = db.get(k)
        # check to see if our model has classified the input
        # image
        if output is not None:
            # add the output predictions to our data
            # dictionary so we can return it to the client
            output = output.decode("utf-8")
            data["predictions"] = json.loads(output)
            # delete the result from the database and break
            # from the polling loop
            db.delete(k)
            break
        # sleep for a small amount to give the model a chance
        # to classify the input image
        time.sleep(settings.CLIENT_SLEEP)
    # indicate that the request was a success
    data["success"] = True
	# return the data dictionary as a JSON response
    return data


def prepare_image(image, target):
	# if the image mode is not RGB, convert it
	if image.mode != "RGB":
		image = image.convert("RGB")
	# resize the input image and preprocess it
	image = image.resize(target)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = preprocess_input(image)
	# return the processed image
	return image