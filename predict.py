# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from keras.preprocessing.image import ImageDataGenerator
from keras.models import model_from_json
import numpy as np
import config
import csv
keys = ['1', '10', '11', '12', '13', '2', '3', '4', '5', '6', '7', '8', '9']
testGen = ImageDataGenerator().flow_from_directory(
    "data/Test",
    class_mode=None,
    target_size=(224, 224),
    color_mode="rgb",
    shuffle=False,
    batch_size=config.BATCH_SIZE)

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")
print(len(testGen.filenames))
print(config.BATCH_SIZE)
predIdxs = loaded_model.predict_generator(testGen, steps=(len(testGen.filenames)//config.BATCH_SIZE) + 1)
print(predIdxs.shape)
predIdxs = np.argmax(predIdxs, axis=1)
print(predIdxs.shape)
 
with open('example.csv', 'w', newline='') as file:  
    writer = csv.writer(file)
    writer.writerow(['Id','Expected'])
    for i in range(len(testGen.filenames)):
        id = testGen.filenames[i].split('\\')[-1].split('.')[0]
        writer.writerow([id, keys[predIdxs[i]]])