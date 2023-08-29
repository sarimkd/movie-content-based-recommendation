import pickle
import streamlit as st
import requests
import pandas as pd

# Set page title
st.set_page_config(page_title="Movie Recommender")

# Developer Information
linkedin = "https://www.linkedin.com/in/sarimkhanskd"
github = "https://github.com/sarimkd"
st.sidebar.write("Developed by [Sarim Khan](%s)" % linkedin, "| [GitHub](%s)" % github)
st.sidebar.write("Email : sarimkhanskd@gmail.com")

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=cae0d088cff177d6b0838bee084f70e3&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

st.header('Movie Recommender System')
#movies = pickle.load(open('movie_list.pkl','rb'))
# Load the movie data from the pickle file
with open('model/movie_dict.pkl', 'rb') as f:
    movies = pickle.load(f)

movies = pd.DataFrame.from_dict(movies)
similarity = pickle.load(open('model/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
selected_movie_id = movies[movies['title'] == selected_movie].iloc[0].id
selected_movie_poster = fetch_poster(selected_movie_id)
column1, column2, column3 = st.columns(3)
with column1:
    st.write(' ')
with column2:
    st.image(selected_movie_poster, caption=selected_movie, width=200)
with column3:
    st.write(' ')

recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.image(recommended_movie_posters[0], caption=recommended_movie_names[0])
with col2:
    st.image(recommended_movie_posters[1], caption=recommended_movie_names[1])
with col3:
    st.image(recommended_movie_posters[2], caption=recommended_movie_names[2])
with col4:
    st.image(recommended_movie_posters[3], caption=recommended_movie_names[3])
with col5:
    st.image(recommended_movie_posters[4], caption=recommended_movie_names[4])