import streamlit as st
import requests
from datetime import datetime


USER_TWEETS_URL = 'http://localhost:8000/api/users/{username}/tweets/'

def show(username):
    st.header(f"Profile: {username}")

    # Fetch user tweets
    response = requests.get(USER_TWEETS_URL.format(username=username))
    
    if response.status_code == 200:
        tweets = response.json()
        
        if tweets:
            for tweet in tweets:
                st.write(f"""
                    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin: 10px 0;">
                        <p>{tweet['content']}</p>
                        <small>Postado por {tweet['user']['username']} em {datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y %H:%M:%S')}</small>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No tweets found.")
    else:
        st.error('Failed to fetch tweets.')

# Teste o perfil diretamente ao executar este script
if __name__ == "__main__":
    show('medina')
