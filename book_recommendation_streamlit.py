import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Data
books = pd.read_csv("books.csv")
ratings = pd.read_csv("ratings.csv")  # Add your ratings.csv here

# --- Content-Based Preprocessing ---
books['features'] = books['Title'] + " " + books['Author'] + " " + books['Genre']
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(books['features'])
content_similarity = cosine_similarity(tfidf_matrix)

# --- Collaborative Filtering Preprocessing ---
user_item_matrix = ratings.pivot_table(index='User_ID', columns='Book_ID', values='Rating').fillna(0)
user_similarity = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

# --- UI ---
st.title("📚 Book Recommender System")
tab1, tab2, tab3 = st.tabs(["Content-Based", "Collaborative", "Hybrid"])

# ------------------------- Tab 1: Content-Based -------------------------
with tab1:
    st.header("🔍 Content-Based Recommendations")
    book_titles = books['Title'].tolist()
    selected = st.selectbox("Choose a Book", book_titles, key="cb_book")

    if st.button("Recommend", key="cb_recommend"):
        index = books[books['Title'] == selected].index[0]
        similar_books = content_similarity[index].argsort()[::-1][1:4]
        st.write("### Recommended Books:")
        for i in similar_books:
            st.write("- " + books.iloc[i]['Title'])

# ------------------------- Tab 2: Collaborative Filtering -------------------------
with tab2:
    st.header("👤 Collaborative Filtering (User-Based)")
    user_ids = user_item_matrix.index.tolist()
    selected_user = st.selectbox("Choose a User ID", user_ids)

    if st.button("Recommend", key="cf_recommend"):
        # Get ratings from similar users
        sim_users = user_similarity_df.loc[selected_user].sort_values(ascending=False)[1:4].index
        sim_ratings = user_item_matrix.loc[sim_users].mean().sort_values(ascending=False)

        # Recommend unrated books
        user_rated_books = user_item_matrix.loc[selected_user][user_item_matrix.loc[selected_user] > 0].index
        recommendations = sim_ratings.drop(user_rated_books).head(3)

        st.write("### Recommended Books:")
        for book_id in recommendations.index:
            title = books[books['Book_ID'] == book_id]['Title'].values[0]
            st.write("- " + title)

# ------------------------- Tab 3: Hybrid -------------------------
with tab3:
    st.header("🧠 Hybrid Recommendations")
    selected_user_h = st.selectbox("Choose User ID", user_ids, key="hy_user")
    selected_book = st.selectbox("Choose a Book", books['Title'].tolist(), key="hy_book")

    if st.button("Recommend", key="hy_recommend"):
        book_id = books[books['Title'] == selected_book]['Book_ID'].values[0]
        book_index = books[books['Book_ID'] == book_id].index[0]

        content_scores = content_similarity[book_index]
        user_ratings = user_item_matrix.loc[selected_user_h]
        aligned_ratings = user_ratings.reindex(books['Book_ID']).fillna(0).values

        hybrid_score = 0.6 * content_scores + 0.4 * aligned_ratings
        top_indices = np.argsort(hybrid_score)[::-1]
        recommended_indices = [i for i in top_indices if i != book_index][:3]

        st.write("### Recommended Books:")
        for i in recommended_indices:
            st.write("- " + books.iloc[i]['Title'])