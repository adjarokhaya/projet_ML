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
    st.markdown(
        "Design-Picker data-visualisation"
    )
    # histograme pour la distance
    plt.figure(figsize=(10, 5))
    sns.histplot(distances[0], kde=False)
    plt.xlabel("Distance")
    plt.ylabel("Nombre de vêtements")
    plt.title("Histogramme des distances des vêtements les plus proches")
    st.pyplot()

    # plus proches des voisin
    plt.figure(figsize=(10, 5))
    sns.barplot(x=np.arange(5), y=distances[0][1:], palette="deep")
    plt.xlabel("Index des vêtements les plus proches")
    plt.ylabel("Distance")
    plt.title("Barplot des distances des 5 vêtements les plus proches")
    st.pyplot()

    np.random.seed(0)
    data = np.random.normal(size=(20, 6)) + np.arange(6) / 2

    st.markdown(
        "Nuage de point representant l'ensemble des images de mon fichier plk afin visaliser ou se trouve mes images sur le graph"
    )
    # seaborn pour le graph kes valeur les plus proche
    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(feature_list)
    plt.scatter(reduced_features[:, 0], reduced_features[:, 1])
    for i in indices[0][1:]:
        plt.scatter(reduced_features[i, 0], reduced_features[i, 1], color='red')
    st.pyplot()
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


