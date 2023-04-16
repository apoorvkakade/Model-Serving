import bentoml

model  = bentoml.keras.load_model("keras_resnet50:latest")

print(model)