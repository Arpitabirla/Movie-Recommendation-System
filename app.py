import streamlit as st
import pickle
import pandas as pd
import requests
import urllib.parse

# TMDB API Key
API_KEY = "702c37606c0f0ca30d954a70d4c0c286"


#  Fetching poster using movie name
def fetch_poster(movie_name):
    try:
        # Encodeing movie name
        query = urllib.parse.quote(movie_name)

        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"

        response = requests.get(url, timeout=5)

        # API failed
        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=API+Error"

        data = response.json()

        # No results found
        if len(data['results']) == 0:
            return "https://via.placeholder.com/500x750?text=No+Result"

        # Find first movie with valid poster
        for movie in data['results']:
            if movie.get('poster_path'):
                return "https://image.tmdb.org/t/p/w500/" + movie['poster_path']

        # No poster available
        return "https://via.placeholder.com/500x750?text=No+Poster"

    except Exception:
        return "https://via.placeholder.com/500x750?text=Error"


# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]]['title']

        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# UI
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

# Button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])