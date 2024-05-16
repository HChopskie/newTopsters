import streamlit as st
from streamlit_dnd import st_dnd
import requests
from PIL import Image
from io import BytesIO

# Google Custom Search API settings
API_KEY = 'your_google_api_key'
CSE_ID = 'your_cse_id'

def fetch_album_images(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={CSE_ID}&key={API_KEY}&searchType=image&num=5"
    response = requests.get(url)
    results = response.json()
    return [item['link'] for item in results.get('items', [])]

def main():
    st.title("Topsters Creator")

    with st.sidebar:
        st.header("Configuration")
        rows = st.number_input("Number of rows", min_value=1, value=3)
        cols = st.number_input("Number of columns", min_value=1, value=3)

        query = st.text_input("Search for an album")
        if query:
            album_images = fetch_album_images(query)
            for img_url in album_images:
                st.image(img_url, use_column_width=True)

    grid = [[None for _ in range(cols)] for _ in range(rows)]

    st.header("Create your Topster")
    container = st.container()
    for r in range(rows):
        cols_container = container.columns(cols)
        for c in range(cols):
            with cols_container[c]:
                if st_dnd.drag_and_drop(f"drop_area_{r}_{c}", key=f"drop_{r}_{c}"):
                    grid[r][c] = st.session_state[f"drop_{r}_{c}"]

    for r in range(rows):
        cols_container = st.columns(cols)
        for c in range(cols):
            with cols_container[c]:
                if grid[r][c]:
                    st.image(grid[r][c], use_column_width=True)

if __name__ == "__main__":
    main()