import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

TWEET_CREATE_URL = 'http://localhost:8000/api/tweets/'

def create_tweet(content, username, password):
    auth = HTTPBasicAuth(username, password)
    data = {'content': content}
    response = requests.post(TWEET_CREATE_URL, auth=auth, data=data)
    return response

def show():
    st.subheader('Create Tweet')
    new_tweet = st.text_area('Tweet Content', key='tweet_content')

    if st.button('Create Tweet'):
        response = create_tweet(new_tweet, st.session_state.username, st.session_state.password)
        if response.status_code == 201:
            st.success('Tweet created successfully!')
            st.session_state['tweet_content'] = ''  # Clear the text area
            st.experimental_rerun()  # Refresh the page to update the feed
        else:
            st.error(f'Failed to create tweet. Error: {response.status_code} - {response.text}')
