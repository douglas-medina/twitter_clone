import streamlit as st
import requests

REGISTER_URL = 'http://localhost:8000/api/register/'

def show():
    st.subheader('Register')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')
    email = st.text_input('Email')
    
    if st.button('Register'):
        if password == confirm_password:
            result = register(username, password, email)
            if 'id' in result:  # Exemplo: verificar se o registro foi bem-sucedido
                st.success('Registration successful!')
                st.session_state.username = username
                st.session_state.access_token = result['access_token']
            else:
                st.error('Registration failed. Please check your details.')
        else:
            st.warning('Passwords do not match. Please try again.')

def register(username, password, email):
    data = {'username': username, 'password': password, 'email': email}
    response = requests.post(REGISTER_URL, data=data)
    return response.json()
