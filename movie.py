import streamlit as st
import pickle
import requests

# Load data
movies = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies_list = movies['title'].values

# App title
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎬 Movie Recommender 🍿</h1>", unsafe_allow_html=True)
st.write("**Find your next favorite movie based on what you love!**")

# Movie selector
select_value = st.selectbox('📽️ **Select a Movie**', movies_list)

# Fetch poster from TMDB
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0e5953f9f143eb850eaf18082c5bc509'
    response = requests.get(url)
    
    if response.status_code != 200:
        return "https://via.placeholder.com/500x750?text=No+Image"

    data = response.json()
    poster_path = data.get("poster_path")
    
    if not poster_path:
        return "https://via.placeholder.com/500x750?text=No+Image"
    
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_list = []
    recommend_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_poster.append(fetch_poster(movie_id))
        recommend_list.append(movies.iloc[i[0]].title)
    return recommend_list, recommend_poster

# Show recommendations
if st.button("✨ Recommend"):
    movie_names, movie_posters = recommend(select_value)
    st.markdown("---")
    st.subheader(f"🎉 **Top 5 Recommendations for _{select_value}_**")

    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.image(movie_posters[idx], use_container_width=True)

            st.caption(f"**{movie_names[idx]}**")
