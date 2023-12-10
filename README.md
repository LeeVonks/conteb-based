# Culinary Recommendation API

## Overview

This Flask-based API provides restaurant recommendations and information based on culinary preferences. It utilizes TF-IDF and cosine similarity for recommendation and includes an endpoint to retrieve top-rated restaurants.

## Endpoints

### Get Recommendations

#### Endpoint:

`GET /recommendations/<place_name>`

#### Description:

This endpoint provides restaurant recommendations based on the input place name. If the exact name is not found, it performs a fuzzy search to find similar restaurant names.

#### Request:

- Parameters:
  - `place_name` (string): The name of the restaurant.

#### Response:

- Status: 200 OK
- Content: JSON
  - `status` (string): "SUCCESS" or "ERROR"
  - `message` (string): A message describing the status
  - `recommended_places` (array of objects): An array of recommended places with details.

### Get Top-Rated Restaurants

#### Endpoint:

`GET /top-rated`

#### Description:

This endpoint retrieves the top-rated restaurants based on culinary ratings.

#### Response:

- Status: 200 OK
- Content: JSON
  - `status` (string): "SUCCESS" or "ERROR"
  - `message` (string): A message describing the status
  - `top_rated_places` (array of objects): An array of top-rated places with details.

## Technologies Used

- Python
- Flask
- pandas
- scikit-learn (TF-IDF and cosine similarity)
- fuzzywuzzy (for fuzzy string matching)

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/culinary-recommendation-api.git

   
2. Install dependencies:
   ```bash
pip install -r requirements.txt

3. Run the API:
   ```bash
python app.py
