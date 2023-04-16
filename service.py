import bentoml

import numpy as np
# from bentoml.io import Image
from PIL import Image
from bentoml.io import JSON
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from pydantic import BaseModel
from io import BytesIO
import base64
runner = bentoml.keras.get("keras_resnet50:latest").to_runner()

svc = bentoml.Service("keras_resnet50", runners=[runner])

class ImageRequest(BaseModel):
    b64: str

    class Config:
        extra: 'forbid'

input_spec = JSON(pydantic_model=ImageRequest)

@svc.api(input=input_spec, output=JSON())
async def predict(img):
    img = img.b64
    img = Image.open(BytesIO(base64.b64decode(img)))
    img = img.resize((224, 224))
    arr = np.array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)
    preds = await runner.async_run(arr)
    return decode_predictions(preds, top=1)[0]
    # print(img.b64)