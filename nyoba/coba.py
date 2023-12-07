import os
from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Lokasi file dataset
dataset_path = os.path.join("culinary_dataset.csv")

# Baca file dataset
dataset = pd.read_csv(dataset_path)

# Lokasi file matriks kemiripan cosine
cosine_sim_matrix = os.path.join("models", "resto_recommendations.pkl")

# Periksa keberadaan file
if not os.path.exists(cosine_sim_matrix):
    print("File tidak ada")
    exit()



# Fungsi untuk mendapatkan rekomendasi
def get_cosine_similarities():
    # Terima permintaan dari pengguna
    place_name = request.args.get("place_name")
    place_name = place_name.replace(" ", "")
    place_name = place_name.replace(".", "")
    place_name = place_name.replace(",", "")

    # Periksa format nama tempat
    if not place_name.isalpha():
        print("Format nama tempat tidak valid")
        exit()

    # Cari restoran berdasarkan nama
    place_data = dataset.loc[place_name]

    # Dapatkan kemiripan cosine untuk tempat yang diminta
    similarity_scores = cosine_sim_matrix.loc[place_name]

    # Mengurutkan tempat berdasarkan kemiripan cosine
    sorted_index = similarity_scores.argsort()[-10:][::-1]

    # Mengekstrak 10 tempat rekomendasi teratas
    recommended_places = [cosine_sim_matrix.columns[i] for i in sorted_index]

    # Kembalikan respon
    return jsonify({
        "status": "SUCCESS",
        "message": "Rekomendasi Restoran",
        "recommended_places": recommended_places,
        "place_details": place_data.to_dict()
    })

# Fungsi untuk mendapatkan detail tempat
def get_place_details(place_name):
    # Cari restoran berdasarkan nama
    place_data = dataset.loc[place_name]

    # Periksa apakah restoran ditemukan
    if place_data.empty:
        return jsonify({
            "status": "ERROR",
            "message": "Restoran tidak ditemukan"
        })

    # Kembalikan detail restoran
    return jsonify(place_data.to_dict())

# Route API
@app.route('/')
def index():
    return {"status": "SUCCESS",
            "message": "Service is Up"}, 200

@app.route("/recommendations/place_name", methods=["GET"])
def recommendations():
    return get_cosine_similarities()

@app.route("/places/<place_name>", methods=["GET"])
def place_details(place_name):
    return get_place_details(place_name)

if __name__ == "__main__":
    app.run(debug=True)
