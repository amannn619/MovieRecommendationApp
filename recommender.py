import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

movies = pd.read_csv("movieData/final_movies_data.csv")
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(movies['tags']).toarray()
similarity = cosine_similarity(vector)


def get_movie(movie):
    apikey = "67563d5737e9fd5ced1250495eaae39b"
    url = f"https://api.themoviedb.org/3/search/movie?api_key={apikey}&query={movie}&page=1"
    response = requests.get(url)
    data = response.json()
    res = []
    for i in data["results"]:
        res.append(i["title"].lower())
    return res


def get_index(movie):
    try:
        index = movies[movies['title'].str.lower() == movie.lower()].index[0]
        return index
    except:
        return -1


def recommender(movie):
    recommendations = []
    searched_movie = movie
    index = get_index(movie)
    if index == -1:
        movie_titles = get_movie(movie)
    while index == -1 and len(movie_titles) > 0:
        movie = movie_titles.pop(0)
        index = get_index(movie)
    if index == -1:
        return "no movie", searched_movie
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:11]:
        recommendations.append(movies.iloc[i[0]].title)
    return recommendations, movie
