import streamlit as st
import requests
from datetime import datetime

TWEET_LIST_URL = 'http://localhost:8000/api/tweets/'

def show(access_token):
    st.subheader('Feed do Twitter')

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(TWEET_LIST_URL, headers=headers)

    if response.status_code == 200:
        tweets = response.json()
        sorted_tweets = sorted(tweets, key=lambda x: datetime.strptime(x['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'), reverse=True)

        for tweet in sorted_tweets:
            st.markdown('---')
            st.write(f"Publicado por: {tweet['user']['username']}")
            st.write(f"**{tweet['content']}**")
            
            # Convertendo a data para o formato brasileiro
            created_at = datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            created_at_str = created_at.strftime('%d/%m/%Y %H:%M:%S')

            st.write(f"Criado em: {created_at_str}")

    else:
        st.error('Falha ao buscar os tweets.')

