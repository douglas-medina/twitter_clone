import streamlit as st
import requests
from datetime import datetime

USER_URL = 'http://localhost:8000/api/users/{username}/tweets/'
FOLLOW_URL = 'http://localhost:8000/api/follow/{pk}/'

def show_profile(username, access_token):
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
        else:
            st.write("No tweets found.")
        
        # Check if current user is following this user
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        
        if st.session_state.user_id:  # Ensure user_id is set in session state
            follow_status = "Follow"
            for tweet in tweets:
                if st.session_state.user_id in tweet['user']['followers']:
                    follow_status = "Unfollow"
                    break

            col1, col2 = st.columns([3, 1])  # Adjust column widths as needed

            with col1:
                st.write(f"Username: {tweets[0]['user']['username']}")
                st.write(f"Email: {tweets[0]['user']['email']}")
            
            with col2:
                if st.button(follow_status):
                    follow_response = requests.post(FOLLOW_URL.format(pk=tweets[0]['user']['id']), headers={'Authorization': f'Bearer {access_token}'})
                    if follow_response.status_code == 200:
                        st.success(f"{follow_status} successful!")
                    else:
                        st.error(f"Failed to {follow_status.lower()}. Error: {follow_response.status_code} - {follow_response.text}")

    else:
        st.error(f'Failed to fetch user profile. Status code: {response.status_code}')

# Test the profile directly when running this script
if __name__ == "__main__":
    access_token = 'seu_token_de_autenticacao'  # Replace with the token obtained after login
    st.session_state.user_id = 1  # Initialize user_id with the ID of the logged-in user
    
    show_profile('medina', access_token)
