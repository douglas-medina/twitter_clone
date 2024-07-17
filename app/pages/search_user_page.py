# app/pages/search_page.py

import streamlit as st
from app.pages.profile_page import show_profile

def show():
    st.title('Search User')

    search_username = st.text_input('Enter username:')
    if st.button('Search'):
        show_profile(search_username, st.session_state.access_token)
