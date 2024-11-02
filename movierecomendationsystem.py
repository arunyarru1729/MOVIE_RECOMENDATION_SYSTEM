import streamlit as st
import pickle
import pandas as pd
import requests
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=4de3882e8a7b565374263a13a9839f5c'
        )
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return f"http://image.tmdb.org/t/p/w500{data['poster_path']}"
        else:
            st.write(f"Poster not found for movie ID: {movie_id}")
            return "https://via.placeholder.com/500?text=Poster+Not+Available" 
    except requests.exceptions.RequestException:
        st.write(f"Failed to fetch poster for movie ID: {movie_id}")
        return "https://via.placeholder.com/500?text=Error+Fetching+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('C:/Users/Yarru Arun/Desktop/Movie_recomendation_system/movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('C:/Users/Yarru Arun/Desktop/Movie_recomendation_system/similarity.pkl', 'rb'))

st.title('Movie Recommendation System')
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)
