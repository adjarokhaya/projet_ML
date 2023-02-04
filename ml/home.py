import streamlit as st
import os
from PIL import Image
import numpy as np
import pickle
import tensorflow
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
from numpy.linalg import norm
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA


feature_list = np.array(pickle.load(open('embeddings.pkl', 'rb')))
filenames = pickle.load(open('filenames.pkl', 'rb'))

model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model.trainable = False

model = tensorflow.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])


st.title('Design picker')
st.markdown(
    "Design-Picker une application Web qui permet aux utilisateurs de trouver des vêtements similaires à partir d'une photo/image qu'ils ont téléchargée. L'utilisateur peut prendre une photo d'un vêtement qu'il voit dans la rue, la télécharger sur le site web, et l'application renverra une liste de vêtements similaires à partir de notre base de données."
            )
def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('uploads',uploaded_file.name),"wb") as f:
            f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0

def feature_extraction(img_path,model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)

    return normalized_result

def recommend(features, feature_list):
    neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
    neighbors.fit(feature_list)
    distances, indices = neighbors.kneighbors([features])

    st.set_option('deprecation.showPyplotGlobalUse', False)
    return indices


uploaded_file = st.file_uploader("Choisir une image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    if save_uploaded_file(uploaded_file):
        display_image = Image.open(uploaded_file)
        st.image(display_image, caption="Image sélectionnée", use_column_width=True)

        features = feature_extraction(os.path.join("uploads", uploaded_file.name), model)

        indices = recommend(features, feature_list)

        st.header("Les 5 images les plus proches :")

        for index in indices[0]:
            st.image(filenames[index], use_column_width=True)
    else:
        st.header("Il y a eu une erreur")


