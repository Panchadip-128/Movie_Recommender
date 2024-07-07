import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    print("API Response for movie ID {}: {}".format(movie_id, data))  # Print API response for debugging
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        # Handle the case when 'poster_path' is not found
        print("Poster path not found for movie ID:", movie_id)  # Print error message for debugging
        return "Placeholder_for_missing_poster"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_title = movies.iloc[i[0]]['title']  # Fetch the movie title
        print("Fetching poster for movie:", movie_title)  # Print movie title for debugging
        # Use the movie title to fetch the movie ID from the API
        movie_id = fetch_movie_id(movie_title)
        if movie_id:
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movie_title)  # Append movie title instead of 'title' column from DataFrame

    return recommended_movie_names, recommended_movie_posters

# Function to fetch movie ID based on the title (modify this according to your API)
def fetch_movie_id(movie_title):
    # Implement the logic to fetch movie ID using the movie title
    # For demonstration, I'm assuming a simple dictionary mapping of titles to IDs
    movie_id_mapping = {
        "Movie Title 1": "id1",
        "Movie Title 2": "id2",
        # Add more mappings as needed
    }
    return movie_id_mapping.get(movie_title, None)

st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity1.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    if not recommended_movie_names:
        st.write("No recommendations found.")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        for name, poster in zip(recommended_movie_names, recommended_movie_posters):
            with col1:
                st.text(name)
                st.image(poster)
