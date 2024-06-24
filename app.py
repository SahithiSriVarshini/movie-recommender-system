import streamlit as st
import pickle
import requests
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = '/Users/apple/Desktop/MovieRecommendation/bg.jpg'
img_base64 = get_base64_of_bin_file(img_path)

bg_img = f"""
<style>
.stApp {{
    background: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
}}
</style>
"""

st.markdown(bg_img, unsafe_allow_html=True)

def fetch_poster(movie_id):
#    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=47d861b044b9c0e3033734150686571a&language=en-US'.format(movie_id))
#    data = response.json()
#    return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    # url = "https://api.themoviedb.org/3/movie/{movie_id}?api_key=47d861b044b9c0e3033734150686571a&language=en-US"
    # response = requests.get(url)

    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0N2Q4NjFiMDQ0YjljMGUzMDMzNzM0MTUwNjg2NTcxYSIsIm5iZiI6MTcxOTE1ODQ4Mi44OTU0ODQsInN1YiI6IjY2Nzg0MmYwYTJhZjI4M2NlZGYyNTIzYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.yzTdi1j0kqTi9hlZY3-_ee1luUoKp-kvprj6LjtLAQc"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x : x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append((movies.iloc[i[0]].title))
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies = pickle.load(open('movies.pkl','rb'))
movieNames = movies['title'].values
similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Select a movie you like',movieNames)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])