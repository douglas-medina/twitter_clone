import streamlit as st
import requests
from app.pages import login_page, tweet_feed_page, profile_page, register_page, search_user_page

LOGIN_URL = 'http://localhost:8000/api/token/'

def login(username, password):
    data = {'username': username, 'password': password}
    response = requests.post(LOGIN_URL, data=data)
    return response

def main():
    st.title('Twitter Clone - EBAC')

    # Initialize session state variables if not already initialized
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
        st.session_state.refresh_token = None
        st.session_state.username = None
        st.session_state.password = None
        st.session_state.submitted = False
        st.session_state.user_id = None

    # Display logged in user info if access_token exists
    if st.session_state.access_token:
        st.sidebar.markdown(f"Logged in as: **{st.session_state.username}**")

    # Sidebar options based on login state
    if st.session_state.access_token:
        sidebar_options = ['Create Tweet & View Feed', 'Profile', 'Search']
        st.sidebar.markdown("---")
        if st.sidebar.button('Logout'):
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            st.session_state.username = None
            st.session_state.password = None
            st.session_state.submitted = False
            st.session_state.user_id = None
            st.success('Logged out successfully.')
            st.experimental_rerun()
    else:
        sidebar_options = ['Login', 'Register', 'Search']

    # Main content based on sidebar choice
    choice = st.sidebar.selectbox('Navigation', sidebar_options)

    if choice == 'Login':
        login_page.show()

        # Handle login form submission
        if 'submitted' in st.session_state and st.session_state.submitted:
            username = st.session_state.username
            password = st.session_state.password
            response = login(username, password)
            
            if response.status_code == 200:
                tokens = response.json()
                st.session_state.access_token = tokens['access']
                st.session_state.refresh_token = tokens['refresh']
                st.session_state.user_id = tokens['user_id']
                st.experimental_rerun()
            else:
                st.error('Login failed. Please check your credentials.')
                st.session_state.submitted = False

    elif choice == 'Register':
        register_page.show()

    elif choice == 'Create Tweet & View Feed':
        tweet_feed_page.show()

    elif choice == 'Profile':
        if st.session_state.access_token:
            profile_page.show_profile(st.session_state.username, st.session_state.access_token)
        else:
            st.warning('Please login to view your profile.')

    elif choice == 'Search':
        search_user_page.show(st.session_state.username, st.session_state.access_token)

if __name__ == '__main__':
    main()
