from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from fuzzywuzzy import fuzz

app = Flask(__name__)

# Load Data
culinary_ds = os.path.join("culinary_dataset.csv")
rating_ds = os.path.join("culinary_rating.csv")
user_ds = os.path.join("user.csv")

place = pd.read_csv(culinary_ds)
rating = pd.read_csv(rating_ds)
user = pd.read_csv(user_ds)

# Implementasi TF-IDF pada fitur 'Category'
tf = TfidfVectorizer()
tfidf_matrix = tf.fit_transform(place['Category'])

# Calculate cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim, index=place['Place_Name'], columns=place['Place_Name'])

# Implementasi Sistem Rekomendasi
def resto_recommendations(place_name, similarity_data=cosine_sim_df, items=place[
    ['Place_Id', 
     'Place_Name', 
     'Category', 
     'Culinary_Ratings', 
     'Address',
     'Description',
     'Coordinate',
     'Lat',
     'Long',
     'Gmaps_Address',
     'Image_Address'
     ]], k=10):
    index = similarity_data.loc[:, place_name].to_numpy().argpartition(range(-1, -k, -1))
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    closest = closest.drop(place_name, errors='ignore')
    return pd.DataFrame(closest).merge(items).head(k)



# API endpoint untuk mendapatkan rekomendasi restoran
@app.route('/recommendations/<place_name>', methods=['GET'])
def get_recommendations(place_name):
    try:
# Pemeriksaan nama tempat
        if place_name not in place['Place_Name'].values:
            # Pencarian berbasis kesamaan nama
            similar_places = [name for name in place['Place_Name'] if fuzz.ratio(place_name, name) > 80]
            
            if not similar_places:
                return jsonify({'status': 'ERROR', 'message': 'Nama Restoran Tidak Ditemukan'}), 404
            
            # Rekomendasi berdasarkan tempat yang mirip
            recommendations = resto_recommendations(similar_places[0])
        else:
            # Rekomendasi berdasarkan nama tempat yang sesuai
            recommendations = resto_recommendations(place_name)
        
        response = {
            'status': 'SUCCESS',
            'message': 'Rekomendasi Tempat',
            'recommended_places': recommendations.to_dict(orient='records')
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'status': 'ERROR', 'message': str(e)}), 500

# API endpoint untuk mendapatkan restoran dengan rating tertinggi
@app.route('/top-rated', methods=['GET'])
def get_top_rated_places():
    try:
        top_rated_places = place.sort_values(by='Culinary_Ratings', ascending=False).head(10)
        response = {
            'status': 'SUCCESS',
            'message': 'Restoran dengan Rating Tertinggi',
            'top_rated_places': top_rated_places.to_dict(orient='records')
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'status': 'ERROR', 'message': str(e)}), 500

# Route API
@app.route('/', methods=['GET'])
def index():
    return {"status": "SUCCESS", "message": "Service is Up"}, 200

if __name__ == '__main__':
    app.run(debug=True)
