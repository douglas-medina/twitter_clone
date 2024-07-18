import streamlit as st
import requests
from datetime import datetime

USER_URL = 'http://localhost:8000/api/users/{username}/tweets/'
FOLLOW_URL = 'http://localhost:8000/api/follow/{pk}/'

def show_profile(username, access_token):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header(f"Profile: {username}")

    # Fetch user details
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

            user_id = tweets[0]['user']['id']
            is_following = any(st.session_state.user_id in tweet['user']['followers'] for tweet in tweets)
            follow_status = "Unfollow" if is_following else "Follow"
            
        else:
            st.write("No tweets yet.")
            
        with col2:
            if st.button(follow_status):
                headers = {
                    'Authorization': f'Bearer {access_token}'
                }
                follow_response = requests.post(FOLLOW_URL.format(pk=user_id), headers=headers)
                if follow_response.status_code == 200:
                    st.success(f"{follow_status} successful!")
                    st.session_state[f"follow_status_{user_id}"] = "Unfollow" if follow_status == "Follow" else "Follow"
                else:
                    st.error(f"Failed to {follow_status.lower()}. Error: {follow_response.status_code} - {follow_response.text}")
    else:
        st.error(f'Failed to fetch user profile. Status code: {response.status_code}')

if __name__ == "__main__":
    pass
