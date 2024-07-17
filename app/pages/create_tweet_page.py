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

    if 'tweet_content_temp' not in st.session_state:
        st.session_state.tweet_content_temp = ''

    if 'tweet_created' in st.session_state:
        if st.session_state.tweet_created:
            st.success('Tweet created successfully!')
            st.session_state.tweet_content_temp = ''
            st.session_state.tweet_created = False
            st.experimental_rerun()

    new_tweet = st.text_area('Tweet Content', value=st.session_state.tweet_content_temp, key='tweet_content')

    if st.button('Create Tweet'):
        response = create_tweet(new_tweet, st.session_state.username, st.session_state.password)
        if response.status_code == 201:
            st.session_state.tweet_created = True
        else:
            st.error(f'Failed to create tweet. Error: {response.status_code} - {response.text}')
