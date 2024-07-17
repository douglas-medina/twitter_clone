import streamlit as st
import requests

LOGIN_URL = 'http://localhost:8000/api/token/'

def login(username, password):
    data = {'username': username, 'password': password}
    response = requests.post(LOGIN_URL, data=data)
    return response

def show():
    st.subheader('Login')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        response = login(username, password)
        if response.status_code == 200:
            tokens = response.json()
            st.session_state.access_token = tokens['access']
            st.session_state.refresh_token = tokens['refresh']
            st.session_state.username = username
            st.session_state.password = password
            st.experimental_rerun()  # Redirecionar para a página de feed após login
        else:
            st.error('Login failed. Please check your credentials.')
