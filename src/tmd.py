import requests
from firebase import *
from datetime import datetime, timedelta

API_KEY = '70becdd84007025667ef72b01400f64e'
BASE_URL = 'https://api.themoviedb.org/3'

def get_movies(api_key, num_movies=500):
    """Fetch movies with a broader selection criteria."""
    movies = []
    page = 1
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)  # Broadened to last year
    
    while len(movies) < num_movies:
        response = requests.get(f"{BASE_URL}/discover/movie",
                                params={'api_key': api_key, 'sort_by': 'popularity.desc', 'primary_release_date.gte': one_year_ago.strftime('%Y-%m-%d'), 'page': page})
        data = response.json()
        movies.extend(data["results"])
        if page >= data['total_pages'] or len(movies) >= num_movies:
            break
        page += 1
    
    return [{"id": movie["id"], "title": movie["original_title"]} for movie in movies[:num_movies]]

def get_recent_reviews(movie_id, api_key, max_reviews_per_movie=20):
    """Fetch up to a maximum number of recent reviews for a given movie."""
    endpoint = f"{BASE_URL}/movie/{movie_id}/reviews"
    params = {'api_key': api_key, 'language': 'en-US', 'page': 1}
    reviews = []
    
    while len(reviews) < max_reviews_per_movie:
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            reviews_data = response.json()
            reviews.extend(reviews_data.get('results', []))
            if not reviews_data['results'] or params['page'] >= reviews_data['total_pages']:
                break
            params['page'] += 1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching reviews for movie ID {movie_id}: {e}")
            break
    
    return reviews[:max_reviews_per_movie]

def collect_reviews(api_key, movies, target_reviews=500):
    """Collect up to the target number of recent reviews from a broader selection of movies."""
    num = 1
    for movie in movies:
        if num >= target_reviews:
            break
        movie_reviews = get_recent_reviews(movie['id'], api_key)
        if len(movie_reviews) == 0:
            continue
        for reviews in movie_reviews:
            tmd = TMD(movie["id"], movie["title"], reviews["content"])
            inser_movie_review(tmd, num)
            num +=1
        if num >= target_reviews:
            break

if __name__ == "__main__":
    permission()
    #movies = get_movies(API_KEY, 500)  # Adjust the number of movies to fetch as needed
    #reviews = collect_reviews(API_KEY, movies, 500)
    print(get_review_data(406))
