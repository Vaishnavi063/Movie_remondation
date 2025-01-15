import pickle
import streamlit as st
import requests

def fetch_poster(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return None
    else:
        st.error("Error fetching data from TMDB API.")
        return None

def recommend(movie):
    index = movies[movies['original_title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        # Ensure you have the correct column name for movie ID
        id = movies.iloc[i[0]].get('id')  # Use .get() to avoid errors if column doesn't exist
        poster = fetch_poster(id)
        if poster:  # Only append if the poster is fetched successfully
            recommended_movie_posters.append(poster)
            recommended_movie_names.append(movies.iloc[i[0]].original_title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')
movies = pickle.load(open('Movie_list.pkl', 'rb'))
similarity = pickle.load(open('Similarity.pkl', 'rb'))

movie_list = movies['original_title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)  # Updated method
    for i in range(len(recommended_movie_names)):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
