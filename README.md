## Culinary API Documentation

This API provides functionalities to search for restaurants, fetch recommendations based on user experience similarity, and retrieve top-rated places. A machine learning model can provide recommendation based on User Input Restaurant Name which have tried before. 

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
        * Same as "Matching Restaurants" in the `/search` response.
##

**3. Top-Rated:**
*Get top-rated restaurants*

* `/top-rated`: Get the top 10 highest-rated restaurants.
* **Response:**
    * `status`: `SUCCESS`.
    * `message`: Message indicating successful retrieval of top-rated places.
    * `top_rated_places`: Array of dictionaries containing information about the top-rated restaurants:
        * Same as "Matching Restaurants" in the `/search` response.
##

**4. Root API:**

* `/`: Get a confirmation message that the service is running.
* **Response:**
    * `status`: `SUCCESS`.
    * `message`: Message indicating service is up and running.
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
