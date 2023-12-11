from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from io import StringIO
import requests
import pickle

# Load Data from URLs
culinary_ds_url = "https://storage.googleapis.com/dataset-culinarix/culinary_dataset.csv"
rating_ds_url = "https://storage.googleapis.com/dataset-culinarix/culinary_rating.csv"

# Load data from URLs
def load_data_from_url(url):
    response = requests.get(url)
    data = StringIO(response.text)
    return pd.read_csv(data)

# Load place data from URLs
place = load_data_from_url(culinary_ds_url)

# Implementasi TF-IDF pada fitur 'Category'
tf = TfidfVectorizer()
tfidf_matrix = tf.fit_transform(place['Category'])

# Calculate cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim, index=place['Place_Name'], columns=place['Place_Name'])

# Function Definitions
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

# Save the cosine similarity matrix to a pickle file
with open('resto_recommendations.pkl', 'wb') as file:
    pickle.dump(cosine_sim_df, file)
    
app = Flask(__name__)

with open('resto_recommendations.pkl', 'rb') as file:
    cosine_sim_df = pickle.load(file)

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
            recommendations = resto_recommendations(similar_places[0], similarity_data=cosine_sim_df)
        else:
            # Rekomendasi berdasarkan nama tempat yang sesuai
            recommendations = resto_recommendations(place_name, similarity_data=cosine_sim_df)

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

# API endpoint untuk mencari dan menampilkan restoran berdasarkan query
@app.route('/search', methods=['GET'])
def search_restaurant():
    try:
        query = request.args.get('query', '')  # Mendapatkan query dari parameter URL
        
        # Pencarian restoran berdasarkan query pada nama tempat
        matching_restaurants = place[place['Place_Name'].str.contains(query, case=False)]

        if matching_restaurants.empty:
            return jsonify({'status': 'ERROR', 'message': 'Tidak ada restoran yang cocok dengan query'}), 404

        response = {
            'status': 'SUCCESS',
            'message': 'Hasil Pencarian',
            'matching_restaurants': matching_restaurants[
                ['Place_Id', 'Place_Name', 'Category', 'Culinary_Ratings', 'Address',
                 'Description', 'Coordinate', 'Lat', 'Long', 'Gmaps_Address', 'Image_Address']
            ].to_dict(orient='records')
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
