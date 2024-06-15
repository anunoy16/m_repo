import pandas as pd
import streamlit as st 
import pickle 
import lzma

# Load the pickled data
movies = pickle.load(open('movies_df.pkl', 'rb'))
with lzma.open('data.pkl.xz','rb') as f:
    similarity=pickle.load(f)

# Convert movies to a DataFrame
movies_df = pd.DataFrame(movies)

def recommend(movie):
    movie_index = movies_df[movies_df["title"] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]

    rec_movies = []
    rec_id=[]
    rec_paths = []
    for i in movies_list:
        rec_movies.append(movies_df.iloc[i[0]]['title'])
        rec_paths.append("https://image.tmdb.org/t/p/w500" + movies_df.iloc[i[0]]["backdrop_path"])
        rec_id.append(movies_df.iloc[i[0]]['id'])
    
    return rec_movies,rec_id,rec_paths


st.title("Movie Recommendation System")

select_movie = st.selectbox(
    "Choose a movie",
    movies_df["title"].values
)

if st.button("Recommend"):
    name,mid,path = recommend(select_movie)
    for i,j,k in zip(name,mid,path):
        st.write(i)
        st.write(j)
        st.image(k)
