import pickle
import streamlit as st

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recommended_movie_names = []

        for i in distances[1:6]:
            movie_title = movies.iloc[i[0]]['title']
            recommended_movie_names.append(movie_title)
        
        return recommended_movie_names
    except Exception as e:
        st.write(f"Error in recommend function: {e}")
        return []

# Load movies and similarity matrices
try:
    with open('movie_list.pkl', 'rb') as file:
        movies = pickle.load(file)
    with open('similarity.pkl', 'rb') as file:
        similarity = pickle.load(file)
except Exception as e:
    st.write(f"Error loading files: {e}")

st.header('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)

    if not recommended_movie_names:
        st.write("No recommendations found.")
    else:
        st.write("Recommended Movies:")
        for name in recommended_movie_names:
            st.text(name)
