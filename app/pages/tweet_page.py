import streamlit as st
import requests

TWEET_CREATE_URL = 'http://localhost:8000/api/tweets/'

def show(access_token):
    st.subheader('Create Tweet')
    new_tweet = st.text_area('Tweet Content')
    
    if st.button('Create Tweet'):
        result = create_tweet(new_tweet, access_token)
        if 'id' in result:
            st.success('Tweet created successfully!')
        else:
            st.error('Failed to create tweet.')

def create_tweet(content, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {'content': content}
    response = requests.post(TWEET_CREATE_URL, headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        st.error(f'Failed to create tweet. Status code: {response.status_code}')
        return {}
