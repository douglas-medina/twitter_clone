# app/pages/register_page.py

import streamlit as st
import requests

REGISTER_URL = 'http://localhost:8000/api/register/'

def show():
    st.header("Register")

    with st.form(key='register_form'):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")

    if submitted:
        if password != password_confirm:
            st.error("Passwords do not match!")
        else:
            data = {
                'username': username,
                'email': email,
                'password': password
            }
            response = requests.post(REGISTER_URL, data=data)
            if response.status_code == 201:
                st.success("User registered successfully! Please login.")
                st.session_state.show_register = False
                st.experimental_rerun()
            else:
                st.error(f"Registration failed: {response.text}")