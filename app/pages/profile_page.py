import streamlit as st
import requests
from datetime import datetime

USER_URL = 'http://localhost:8000/api/users/{username}/tweets/'
FOLLOW_URL = 'http://localhost:8000/api/follow/{pk}/'

def show_profile(username, access_token):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header(f"Profile: {username}")

    response = requests.get(USER_URL.format(username=username), headers={'Authorization': f'Bearer {access_token}'})
    
    if response.status_code == 200:
        tweets = response.json()
        
        if tweets:
            for tweet in tweets:
                st.write(f"""
                    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin: 10px 0;">
                        <p>{tweet['content']}</p>
                        <small>Posted by {tweet['user']['username']} on {datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y %H:%M:%S')}</small>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No tweets found.")

        user_id = tweets[0]['user']['id']
        
        if f"follow_status_{user_id}" not in st.session_state:
            follow_status = "Follow"
            for tweet in tweets:
                if st.session_state.user_id in tweet['user']['followers']:
                    follow_status = "Unfollow"
                    break
            st.session_state[f"follow_status_{user_id}"] = follow_status

        follow_status = st.session_state[f"follow_status_{user_id}"]

        with col2:
            if st.button(follow_status):
                follow_response = requests.post(FOLLOW_URL.format(pk=user_id), headers={'Authorization': f'Bearer {access_token}'})
                st.write(f"Sending follow/unfollow request to {FOLLOW_URL.format(pk=user_id)}")
                if follow_response.status_code == 200:
                    st.success(f"{follow_status} successful!")
                    st.session_state[f"follow_status_{user_id}"] = "Unfollow" if follow_status == "Follow" else "Follow"
                    st.experimental_rerun()
                else:
                    st.error(f"Failed to {follow_status.lower()}. Error: {follow_response.status_code} - {follow_response.text}")
                    st.write(f"Error details: {follow_response.json()}")
    else:
        st.error(f'Failed to fetch user profile. Status code: {response.status_code}')

if __name__ == "__main__":
    pass
