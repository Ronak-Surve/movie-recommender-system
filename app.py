import os
import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

movies = pd.read_pickle(open('movies.pkl', 'rb'))
movies_title = movies['title'].values

similarity = pd.read_pickle(open('similarity.pkl', 'rb'))

# fetch poster from API
def fetch_poster(movie_id):
        api_key = os.getenv("API_KEY")
        url = 'https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,api_key)
        response = requests.get(url)
        data = response.json()
        return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

def recommend(movie):
    # fetch the index
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # get the top 5 similar movies
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

st.title("Movie Recommender System")


selected_movie_name = st.selectbox(
    'Which movie is your favourite?',
    (movies_title))

import streamlit as st

if st.button('Recommend'):
    name,poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])




