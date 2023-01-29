import sqlite3
from flask import Flask, render_template, request, jsonify
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import pandas as pd
from io import BytesIO
import base64
import os


app = Flask(__name__)
# connexion à la bdd
def get_db_connection():
    conn = sqlite3.connect('database.db')
   # conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['post'])
def login():
    mail=request.form['mail']
    mdp=request.form['mdp']
    conn = get_db_connection()
    user = conn.execute(f"SELECT * FROM user where adressemail='{mail}' and mdp='{mdp}'").fetchone()
    conn.close()
    if user:
        img = create_figure()
        plot_url = base64.b64encode(img.getvalue())

        print(plot_url)

        return render_template('home.html', plot_url=plot_url.decode())
    else:
       return render_template('index.html')


def create_figure():
    # Charger l'image
    img = cv2.imread("dress.jpg")

    # Convertir l'image en espace de couleurs HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Définir les limites de couleurs à détecter (en utilisant les valeurs HSV)
    lower_blue = (110, 50, 50)
    upper_blue = (130, 255, 255)

    lower_red = (0, 50, 50)
    upper_red = (10, 255, 255)

    lower_green = (50, 100, 100)
    upper_green = (70, 255, 255)

    lower_orange = (10, 50, 50)
    upper_orange = (20, 255, 255)

    lower_yellow = (20, 50, 50)
    upper_yellow = (30, 255, 255)

    lower_teal = (70, 100, 100)
    upper_teal = (90, 255, 255)

    lower_purple = (130, 50, 50)
    upper_purple = (140, 255, 255)

    lower_pink = (140, 50, 50)
    upper_pink = (160, 255, 255)

    lower_brown = (20, 100, 100)
    upper_brown = (30, 255, 255)

    lower_gray = (0, 0, 50)
    upper_gray = (179, 50, 220)

    lower_black = (0, 0, 0)
    upper_black = (179, 255, 30)

    lower_white = (0, 0, 221)
    upper_white = (179, 30, 255)

    # Appliquer la détection de couleurs
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    res_red1 = cv2.bitwise_and(img, img, mask=mask_red)

    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    res_orange = cv2.bitwise_and(img, img, mask=mask_orange)

    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res_yellow = cv2.bitwise_and(img, img, mask=mask_yellow)

    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    res_green = cv2.bitwise_and(img, img, mask=mask_green)

    mask_teal = cv2.inRange(hsv, lower_teal, upper_teal)
    res_teal = cv2.bitwise_and(img, img, mask=mask_teal)

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    res_blue = cv2.bitwise_and(img, img, mask=mask_blue)

    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
    res_purple = cv2.bitwise_and(img, img, mask=mask_purple)

    mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)
    res_pink = cv2.bitwise_and(img, img, mask=mask_pink)

    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    res_brown = cv2.bitwise_and(img, img, mask=mask_brown)

    mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
    res_gray = cv2.bitwise_and(img, img, mask=mask_gray)

    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    res_black = cv2.bitwise_and(img, img, mask=mask_black)

    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    res_white = cv2.bitwise_and(img, img, mask=mask_white)

    # Compter les pixels de chaque couleur dans l'image
    red_pixels = cv2.countNonZero(mask_red)
    orange_pixels = cv2.countNonZero(mask_orange)
    yellow_pixels = cv2.countNonZero(mask_yellow)
    green_pixels = cv2.countNonZero(mask_green)
    teal_pixels = cv2.countNonZero(mask_teal)
    blue_pixels = cv2.countNonZero(mask_blue)
    purple_pixels = cv2.countNonZero(mask_purple)
    pink_pixels = cv2.countNonZero(mask_pink)
    brown_pixels = cv2.countNonZero(mask_brown)
    gray_pixels = cv2.countNonZero(mask_gray)
    black_pixels = cv2.countNonZero(mask_black)
    white_pixels = cv2.countNonZero(mask_white)

    # Créer un dataframe avec les données de couleur
    data = {'color': ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'brown', 'gray', 'black',
                      'white'],
            'pixels': [red_pixels, orange_pixels, yellow_pixels, green_pixels, teal_pixels, blue_pixels, purple_pixels,
                       pink_pixels, brown_pixels, gray_pixels, black_pixels, white_pixels]}
    df = pd.DataFrame(data)

    img = BytesIO()

    # Créer un graphique à barres avec Seaborn de détection de couleur
    sns.barplot(x='color', y='pixels', data=df)

    # nuage de point
    #sns.relplot(data=df, x='color', y='pixels', kind='scatter', col='color')
    #sns.pairplot(df, hue='color')

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return img


@app.route('/upload', methods=['POST'])
def upload():
    # Récupération de l'image téléchargée
    image = request.files['image']
    # Enregistrement de l'image dans un dossier local
    image.save(os.path.join('uploads', image.filename))
    # connexion à la bdd
    conn = get_db_connection()
    # Insertion des informations de l'image dans la table
    conn.execute("INSERT INTO images (nom_image, path) VALUES (?,?)", (image.filename, os.path.join('uploads', image.filename)))
    # Enregistrement des modifications et fermeture de la connexion
    conn.commit()
    conn.close()
    return jsonify({'message': 'Image uploaded successfully'})


if __name__ == '__main__':
    app.run()
