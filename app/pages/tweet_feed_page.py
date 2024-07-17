import streamlit as st
from datetime import datetime
import requests
from .create_tweet_page import show as show_create_tweet

TWEET_FEED_URL = 'http://localhost:8000/api/tweets/'

def fetch_feed():
    response = requests.get(TWEET_FEED_URL)
    return response.json() if response.status_code == 200 else []

def show():
    show_create_tweet()  # Show the create tweet section

    st.subheader('Feed')
    feed = fetch_feed()
    for tweet in feed:
        st.markdown(
            f"""
            <div style="border: 1px solid #ccc; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                <p>{tweet['content']}</p>
                <small>Postado por {tweet['user']['username']} em {datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y %H:%M:%S')}</small>
            </div>
            """,
            unsafe_allow_html=True
        )
