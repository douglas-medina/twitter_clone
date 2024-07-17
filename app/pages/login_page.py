import streamlit as st
import requests

LOGIN_URL = 'http://localhost:8000/api/token/'

def show():
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        st.session_state.submitted = True
        st.session_state.username = username
        st.session_state.password = password

def login(username, password):
    data = {'username': username, 'password': password}
    response = requests.post(LOGIN_URL, data=data)
    return response.json()
