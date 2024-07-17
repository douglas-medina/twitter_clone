import streamlit as st
import requests

LOGIN_URL = 'http://localhost:8000/api/token/'
REGISTER_URL = 'http://localhost:8000/api/register/'
TWEET_CREATE_URL = 'http://localhost:8000/api/tweets/'
FEED_URL = 'http://localhost:8000/api/feed/'

def login(username, password):
    data = {'username': username, 'password': password}
    response = requests.post(LOGIN_URL, data=data)
    return response.json()

def create_tweet(content, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'content': content}
    response = requests.post(TWEET_CREATE_URL, headers=headers, data=data)
    return response.json()

def main():
    st.title('Twitter Clone - Streamlit Frontend')

    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        result = login(username, password)
        if 'access' in result:
            st.success('Logged in successfully!')
            access_token = result['access']

            st.subheader('Create Tweet')
            new_tweet = st.text_area('Tweet Content')
            if st.button('Create Tweet'):
                create_result = create_tweet(new_tweet, access_token)
                st.write(create_result)
        else:
            st.error('Failed to log in. Please check your credentials.')

if __name__ == '__main__':
    main()
