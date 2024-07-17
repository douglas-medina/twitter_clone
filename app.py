import streamlit as st
import requests
from app.pages import login_page, tweet_page, feed_page

LOGIN_URL = 'http://localhost:8000/api/token/'

def login(username, password):
    data = {'username': username, 'password': password}
    response = requests.post(LOGIN_URL, data=data)
    return response

def main():
    st.title('Twitter Clone - Streamlit Frontend')

    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
        st.session_state.refresh_token = None
        st.session_state.username = None
        st.session_state.password = None
        st.session_state.submitted = False

    if st.session_state.access_token:
        st.sidebar.markdown(f"Logged in as: **{st.session_state.username}**")

    if st.session_state.access_token:
        sidebar_options = ['Create Tweet', 'View Feed']
        st.sidebar.markdown("---")
        if st.sidebar.button('Logout'):
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            st.session_state.username = None
            st.session_state.password = None
            st.session_state.submitted = False
            st.success('Logged out successfully.')
            st.experimental_rerun()  # Redireciona para a página de login após logout
    else:
        sidebar_options = ['Login']

    choice = st.sidebar.selectbox('Navigation', sidebar_options)

    if choice == 'Login':
        login_page.show()

        if 'submitted' in st.session_state and st.session_state.submitted:
            username = st.session_state.username
            password = st.session_state.password

            response = login(username, password)
            if response.status_code == 200:
                tokens = response.json()
                st.session_state.access_token = tokens['access']
                st.session_state.refresh_token = tokens['refresh']
                st.experimental_rerun()  # Redirecionar para a página de feed após login
            else:
                st.error('Login failed. Please check your credentials.')
                st.session_state.submitted = False

    #TODO: melhorar o contato com o backend do post de tweets.
    elif choice == 'Create Tweet':
        tweet_page.show(st.session_state.access_token)

    elif choice == 'View Feed':
        feed_page.show(st.session_state.access_token)

if __name__ == '__main__':
    main()
