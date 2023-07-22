import streamlit as st
import pickle
import requests
import pandas as pd

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend_movies(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

st.title("Movie Recommender System")
st.text("Instead of watching random movies.. use this!!")

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend_movies(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
    for i in recommended_movie_names:
        st.write(i)
    


# if st.button('Recommend'):
#     # Get the index of the selected movie
#     index = movies[movies['title'] == selected_movie_name].index[0]
#     # Get the list of tuples containing the index and similarity score of all the movies
#     # in the dataset with the selected movie
#     similar_movies = list(enumerate(movies['similarity'][index]))
#     # Sort the list of tuples in descending order based on the similarity score
#     sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]
#     # Get the top 5 similar movies
#     top_5_similar_movies = []
#     for i in range(5):
#         top_5_similar_movies.append(movies.iloc[sorted_similar_movies[i][0]]['title'])
#     # Display the top 5 similar movies
#     st.write("Top 5 similar movies are:")
#     for i in range(5):
#         st.write(f"{i+1}. {top_5_similar_movies[i]}")

