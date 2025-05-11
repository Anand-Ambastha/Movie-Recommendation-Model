import streamlit as st
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Set page config
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 4px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #00FF9D;
    }
    .stTextInput>div>div>input {
        background-color: #1E1E1E;
        color: #E0E0E0;
        border: 1px solid #333;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 1px #4CAF50;
    }
    .movie-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }
    .movie-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        border-color: #4CAF50;
    }
    .movie-title {
        color: #00FF9D;
        font-size: 1.2em;
        margin-bottom: 5px;
    }
    .movie-genre {
        color: #B0B0B0;
        font-size: 0.9em;
    }
    .stMarkdown {
        color: #E0E0E0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🎬 Movie Recommendation System")
st.markdown("""
    <div style='color: #E0E0E0;'>
    This app recommends movies based on your favorite movie. 
    Simply enter a movie name and get 20 similar movie recommendations!
    </div>
""", unsafe_allow_html=True)

# Load and process data
@st.cache_data
def load_data():
    movies_data = pd.read_csv("movies.csv")
    return movies_data

# Process data and create similarity matrix
@st.cache_data
def create_similarity_matrix(movies_data):
    selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director', 'overview']
    
    # Replace null values with empty string
    for feature in selected_features:
        movies_data[feature] = movies_data[feature].fillna('')
    
    # Combine all selected features
    combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + \
                       movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + \
                       movies_data['director'] + ' ' + movies_data['overview']
    
    # Convert text to feature vectors
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    
    # Get similarity scores
    similarity = cosine_similarity(feature_vectors)
    
    return similarity

# Main function
def main():
    # Load data
    movies_data = load_data()
    similarity = create_similarity_matrix(movies_data)
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Enter Movie Name")
        movie_name = st.text_input("", placeholder="Type a movie name...")
        
        if st.button("Get Recommendations"):
            if movie_name:
                # Find close match
                list_of_movies = movies_data['title'].tolist()
                find_close_match = difflib.get_close_matches(movie_name, list_of_movies)
                
                if find_close_match:
                    close_match = find_close_match[0]
                    index_of_movie = movies_data[movies_data.title == close_match]['index'].values[0]
                    
                    # Get similarity scores
                    similarity_score = list(enumerate(similarity[index_of_movie]))
                    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
                    
                    # Display recommendations
                    st.subheader(f"Recommendations based on '{close_match}'")
                    
                    # Create a container for recommendations
                    with st.container():
                        for i, movie in enumerate(sorted_similar_movies[:20], 1):
                            index = movie[0]
                            title = movies_data[movies_data.index == index]['title'].values[0]
                            genres = movies_data[movies_data.index == index]['genres'].values[0]
                            
                            # Create a card-like display for each movie with new styling
                            st.markdown(f"""
                                <div class='movie-card'>
                                    <div class='movie-title'>{i}. {title}</div>
                                    <div class='movie-genre'>{genres}</div>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.error("No close match found. Please try another movie name.")
            else:
                st.warning("Please enter a movie name.")

if __name__ == "__main__":
    main() 