# import the necessary packages
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.applications.resnet50 import decode_predictions
from PIL import Image
import numpy as np
import settings
import helper_utilities
import flask
import redis
import uuid
import time
import json
import io
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions

# initialize our Flask application and Redis server
app = flask.Flask(__name__)
db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, db=settings.REDIS_DB)

print("* Loading model...")
model = ResNet50(weights="imagenet")
print("* Model loaded")

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


@app.route("/")
def homepage():
	return "Welcome to the DISML project"
@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}
	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		if flask.request.files.get("image"):
			# read the image in PIL format and prepare it for
			# classification
			image = flask.request.files["image"].read()
			image = Image.open(io.BytesIO(image))
			# prepare image should be on model server after gpu is involved since even preprocessing can be done on batches rather
			# than a single image.
			image = prepare_image(image,
				(settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT))
			preds = model.predict(image)
			results = decode_predictions(preds)

			# initialize the list of output predictions
			output = []

			for resultSet in results:
				# loop over the results and add them to the list of
				# output predictions
				print(resultSet)
				for (imagenetID, label, prob) in resultSet:
					r = {"label": label, "probability": float(prob)}
					output.append(r)

			data["predictions"] = output
			data["success"] = True
	return flask.jsonify(data)
# for debugging purposes, it's helpful to start the Flask testing
# server (don't use this for production
if __name__ == "__main__":
	print("* Starting web service...")
	app.run(host="0.0.0.0", port=8000)
