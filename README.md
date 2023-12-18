## Culinarix Content-Based Recommendations Flask-based API Documentation

This Flask-based API provides functionalities to search for restaurants, fetch recommendations based on user experience similarity, and retrieve top-rated places. A machine learning model can provide recommendation based on User Input Restaurant Name which have tried before. 

**Deployment:**

* **Base URL:** [https://culinarix-content-based-fix-6lmjk4zvdq-as.a.run.app](https://culinarix-content-based-fix-6lmjk4zvdq-as.a.run.app)

**API Routes:**

**1. Search:**
*Get restaurant details with search feature*

* `/search`: Search for restaurants by name (case-insensitive).
* **Parameters:**
    * `query`: (optional) String query to search restaurants by name.
* **Response:**
    * `status`: `SUCCESS` if restaurants are found, `ERROR` otherwise.
    * `message`: Descriptive message about the search results.
    * `matching_restaurants`: Array of dictionaries containing information about the matching restaurants (if `status` is `SUCCESS`):
        * `Place_Id`: Restaurant ID.
        * `Place_Name`: Restaurant name.
        * `Category`: Restaurant category.
        * `Culinary_Ratings`: Restaurant culinary rating.
        * `Address`: Restaurant address.
        * `Description`: Restaurant description.
        * `Coordinate`: Restaurant coordinates (latitude and longitude).
        * `Lat`: Restaurant latitude.
        * `Long`: Restaurant longitude.
        * `Gmaps_Address`: Restaurant address on Google Maps.
        * `Image_Address`: Restaurant image URL.
    ```json
      {
            "Address": "Astanaanyar, Kota Bandung",
            "Category": "Chinese",
            "Coordinate": "{'lat':-6.916279099486068, 'lng':107.59973743179438}",
            "Culinary_Ratings": 4.5,
            "Description": "Restoran yang memiliki ruangan yang luas dan cocok untuk berbagai acara, menawarkan beragam                   menu hidangan China, termasuk pork hong.",
            "Gmaps_Address": "https://maps.app.goo.gl/z3wwKvUVjJ2Qx6zF7",
            "Image_Address": "https://lh5.googleusercontent.com/p/AF1QipPRHbJIucHceFJTu_FMQGyP9ts6HG0F5CpVg1XD=w122-h92-k-               no",
            "Lat": -6.916279099,
            "Long": 107.5997374,
            "Place_Id": 94,
            "Place_Name": "Hongkong Restaurant"
       },
    ```
##

**2. Recommendations:**
*Discover restaurant recommendations based on the unique characteristics of each dining establishment.*

* `/recommendations/<place_name>`: Get recommendations for restaurants similar to the specified place.
* **Parameters:**
    * `<place_name>`: Name of the restaurant for which recommendations are requested.
* **Response:**
    * `status`: `SUCCESS` if recommendations are found, `ERROR` otherwise.
    * `message`: Descriptive message about the recommendations.
    * `recommended_places`: Array of dictionaries containing information about the recommended restaurants (if `status` is `SUCCESS`):
    ```json
   {
    "message": "Rekomendasi Tempat",
    "recommended_places": [
        {
            "Address": "Astanaanyar, Kota Bandung",
            "Category": "Chinese",
            "Coordinate": "{'lat':-6.916279099486068, 'lng':107.59973743179438}",
            "Culinary_Ratings": 4.5,
            "Description": "Restoran yang memiliki ruangan yang luas dan cocok untuk berbagai acara, menawarkan beragam                   menu hidangan China, termasuk pork hong.",
            "Gmaps_Address": "https://maps.app.goo.gl/z3wwKvUVjJ2Qx6zF7",
            "Image_Address": "https://lh5.googleusercontent.com/p/AF1QipPRHbJIucHceFJTu_FMQGyP9ts6HG0F5CpVg1XD=w122-h92-k-               no",
            "Lat": -6.916279099,
            "Long": 107.5997374,
            "Place_Id": 94,
            "Place_Name": "Hongkong Restaurant"
        },
          *other 9 restaurant Recommendation..*
        "status": "SUCCESS"
    ```
        
##

**3. Top-Rated:**
*Get top-rated restaurants*

* `/top-rated`: Get the top 10 highest-rated restaurants.
* **Response:**
    * `status`: `SUCCESS`.
    * `message`: `Restoran dengan Rating Tertinggi`
    * `top_rated_places`: Array of dictionaries containing information about the top-rated restaurants:
        * Same as "Matching Restaurants" in the `/search` response.
    ```json
   {
    "message": "Restoran dengan Rating Tertinggi",
    "status": "SUCCESS"
    "top_rated_place": [
        {
            "Address": "Bandung Wetan, Kota Bandung",
            "Category": "Western",
            "Coordinate": "{'lat':-6.891593210184938, 'lng':107.62333924190962}",
            "Culinary_Ratings": 5.0,
            "Description": "Nikmati pilihan menu internasional dan lokal kami yang beragam dengan variasi ala carte. Menu ini mengutamakan bahan-bahan organik lokal dan mendukung keberlanjutan, sambil mempertahankan keaslian warisan lokal. Semua hidangan disajikan dengan sentuhan teknik memasak klasik, menawarkan pengalaman rasa terbaik dari masakan Indonesia-Sunda yang segar. Temukan juga ragam minuman pilihan yang disiapkan dengan antusiasme oleh bartender kami.",
            "Gmaps_Address": "https://maps.app.goo.gl/dEw9YqfuKYk8Tuks9",
            "Image_Address": "https://lh5.googleusercontent.com/p/AF1QipMidZxzG5xcO94yNPt_uWX4ivA90bdbPS6Lp36Y=w122-h92-k-no",
            "Lat": -6.89159321,
            "Long": 107.6233392,
            "Place_Id": 29,
            "Place_Name": "Sadrasa Kitchen & Bar"
        },
          *other 9 restaurant Recommendation..*
    ```
##

**4. Root API:**

* `/`: Get a confirmation message that the service is running.
* **Response:**
    * `status`: `SUCCESS`.
    * `message`: `Service is Up`.
##
**Notes:**

* Recommendations are based on similarity in user experience (cosine similarity of TF-IDF vectors of restaurant categories).
* If the exact `<place_name>` is not found, fuzzy matching with a threshold of 80% is applied.
* The API is deployed on Google Cloud Run and accessible at the provided URL.

**Additional Information:**

* This API is a basic example and can be further enhanced.
* The response format may be adjusted to accommodate specific needs.

## Technologies Used

- Python
- Flask
- Pickle
- sklearn
- numpy
- pandas
- fuzzywuzzy

**Please feel free to explore the API and provide feedback!**
