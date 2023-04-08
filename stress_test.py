from threading import Thread
import requests
import time
from time import sleep, perf_counter
from concurrent.futures import ThreadPoolExecutor, as_completed
 
# initialize the Keras REST API endpoint URL along with the input
# image path
AZURE_VM_IP = "20.25.160.84"

KERAS_REST_API_URL = "http://" + AZURE_VM_IP + "/predict"
IMAGE_PATH = "fish.png"
# initialize the number of requests for the stress test along with
# the sleep amount between requests
NUM_REQUESTS = 500
SLEEP_COUNT = 0.05
image = open(IMAGE_PATH, "rb").read()
def call_predict_endpoint(n):
	# load the input image and construct the payload for the request
	payload = {"image": image}
	# submit the request
	r = requests.post(KERAS_REST_API_URL, files=payload).json()
	# ensure the request was sucessful
	sleep(SLEEP_COUNT)
	if r["success"]:
		return "[INFO] thread {} OK".format(n)
	# otherwise, the request failed
	else:
		return "[INFO] thread {} FAILED".format(n)
	
# loop over the number of threads

thread_results = []
start_time = perf_counter()

with ThreadPoolExecutor() as executor:
	for i in range(0, NUM_REQUESTS):
		thread_results.append(executor.submit(call_predict_endpoint, i))
	
	for res in as_completed(thread_results):
		print(res.result())

end_time = perf_counter()

print("It took total time " end_time-start_time)