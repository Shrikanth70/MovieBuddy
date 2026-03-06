import pickle
import pandas as pd
import os

# Load movies dataset and similarity matrix
# movies.pkl is now a tuple: (movies_df, similarity_matrix)
pkl_path = os.path.join(os.path.dirname(__file__), "movies.pkl")

try:
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)
        if isinstance(data, tuple) and len(data) == 2:
            movies = data[0]
            similarity = data[1]
        else:
            movies = data
            # Fallback recompute if similarity is not in pkl
            from sklearn.feature_extraction.text import CountVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            cv = CountVectorizer(max_features=5000, stop_words='english')
            vectors = cv.fit_transform(movies['tags']).toarray()
            similarity = cosine_similarity(vectors)
except Exception as e:
    print(f"Error loading recommendations: {e}")
    movies = pd.DataFrame()
    similarity = None

def recommend_by_id(movie_id):
    """Recommend movies based on a TMDB movie ID."""
    if movies.empty or similarity is None:
        return []
        
    try:
        # Check if the ID exists in our local dataset
        if movie_id not in movies['movie_id'].values:
            return []
            
        index = movies[movies['movie_id'] == movie_id].index[0]
        distances = similarity[index]
        
        movies_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:9] # Get top 8 recommendations

        recommended_ids = []
        for i in movies_list:
            recommended_ids.append(int(movies.iloc[i[0]].movie_id))

        return recommended_ids
    except Exception as e:
        print(f"Error in recommend_by_id: {e}")
        return []

def recommend(movie_title):
    """Legacy support for recommendation by title."""
    if movies.empty or similarity is None:
        return []
        
    try:
        if movie_title not in movies['title'].values:
            return []
            
        index = movies[movies['title'] == movie_title].index[0]
        distances = similarity[index]
        
        movies_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:7]

        recommended_titles = []
        for i in movies_list:
            recommended_titles.append(movies.iloc[i[0]].title)

        return recommended_titles
    except Exception as e:
        print(f"Error in recommend: {e}")
        return []