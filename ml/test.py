import pickle
import tensorflow
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
import cv2

features = pickle.load(open("embeddings.pkl", "rb"))
filenames = pickle.load(open("filenames.pkl", "rb"))

# utilisation des modèle ResNet50 et GobalMaxPooling2D
resnet50 = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
resnet50.trainable = False
model = tensorflow.keras.Sequential([resnet50, GlobalMaxPooling2D()])

#tensorflow
img = image.load_img("sample/ballon.jpg", target_size=(224, 224))
img_array = image.img_to_array(img)
expanded_img_array = np.expand_dims(img_array, axis=0)
preprocessed_img = preprocess_input(expanded_img_array)
result = model.predict(preprocessed_img).flatten()

# Normalisation pour poizat
normalized_result = result / np.linalg.norm(result)

# fonction de fit pour trouver les voisins les plus proches et enfin trouver les images
neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
neighbors.fit(features)
_, indices = neighbors.kneighbors([normalized_result])

for file_index in indices[0][1:]:
    temp_img = cv2.imread(filenames[file_index])
    cv2.imshow("Output", cv2.resize(temp_img, (512, 512)))
    cv2.waitKey(0)