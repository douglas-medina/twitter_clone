import streamlit as st
from app.pages.profile_page import show_profile

def show():
    st.title('Search User')

    search_username = st.text_input('Enter username:')
    if st.button('Search'):
        st.session_state['search_username'] = search_username

    if 'search_username' in st.session_state:
        show_profile(st.session_state['search_username'], st.session_state.access_token)
