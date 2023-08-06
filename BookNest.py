import streamlit as st
import pandas as pd
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="BookNest",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)




def page1():
    pop_books = pd.read_csv('final_popular_books.csv')
    st.title("BookNest")
    st.title(":red[Popular Books]")
    st.write("")
    st.write("")

    num_rows = 10
    num_images_per_row = 5

    for row in range(num_rows):
        # Create a new row for each iteration
        cols = st.columns(num_images_per_row)

        # Iterate over each column in the current row
        for col in range(num_images_per_row):
            index = row * num_images_per_row + col
            with cols[col]:
                st.image(
                    pop_books['Image-URL-L'].head(50)[index],
                    caption=pop_books['Book-Title'].head(50)[index] + " (by " + pop_books['Book-Author'].head(50)[
                        index] + ") " + " (" + str(
                        pop_books['Year-Of-Publication'].head(50)[index]) + ") " + " (Avg.rating = " + str(
                        round(pop_books['Avg-Rating'].head(50)[index], 2)) + ")",
                    use_column_width=True
                )

def page2():
    books = pd.read_csv('BOOKS_FINAL.csv')
    ratings = pd.read_csv('RATINGS_FINAL.csv')
    new_ratings = ratings.merge(books, on="ISBN")
    x = new_ratings.groupby('User-ID').count()['Book-Rating'] > 200
    educated_users = x[x].index
    filtered_ratings = new_ratings[new_ratings['User-ID'].isin(educated_users)]
    y = filtered_ratings.groupby('Book-Title').count()['Book-Rating'] >= 50
    rated_books = y[y].index
    final_ratings = filtered_ratings[filtered_ratings['Book-Title'].isin(rated_books)]

    final_table = final_ratings.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
    final_table.fillna(0, inplace=True)
    new_final = final_ratings.drop_duplicates(subset='Book-Title').copy()

    similarity_score = cosine_similarity(final_table)
    st.title("BookNest")
    st.title(":red[Books Recommender]")

    optios = new_final['Book-Title']
    selected_option = st.selectbox("Select a Book title",optios)

    recommend_button = st.button(label="Recommend")

    if recommend_button:
        def recommend(book_name):
            index=np.where(final_table.index==book_name)[0][0]
            similar_books = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]
            data=[]
            for i in similar_books:
                item=[]
                temp_df = books[books['Book-Title']==final_table.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
                data.append(item)
            return data



        final_recommend=recommend(selected_option)
        # print(final_recommend)
        col1,col2,col3,col4,col5 = st.columns(5)
        with col1:
            st.image(final_recommend[0][2],caption=final_recommend[0][0]+" ( by "+final_recommend[0][1]+" )")
        with col2:
            st.image(final_recommend[1][2],caption=final_recommend[1][0]+" ( by "+final_recommend[1][1]+" )")
        with col3:
            st.image(final_recommend[2][2],caption=final_recommend[2][0]+" ( by "+final_recommend[2][1]+" )")
        with col4:
            st.image(final_recommend[3][2],caption=final_recommend[3][0]+" ( by "+final_recommend[3][1]+" )")
        with col5:
            st.image(final_recommend[4][2],caption=final_recommend[4][0]+" ( by "+final_recommend[4][1]+" )")


def main():
    selected_page = st.sidebar.radio("BookNest", ("Popular Books","Books Recommender"))
    if selected_page == "Popular Books":
        page1()
    elif selected_page == "Books Recommender":
        page2()

if __name__ == "__main__":
    main()