import pandas as pd
import requests
import os

movies = pd.read_csv("movieData/final_movies_data.csv")


def get_movie_details(movie):
    apikey = os.environ.get("tmdb-api-key")
    movie_id = movies.loc[movies["title"].str.lower() ==
                          movie.lower()][:1].id.squeeze()
    if movie:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={apikey}"
        movie_details = requests.get(url)
        data = movie_details.json()
        return data
    else:
        return False
