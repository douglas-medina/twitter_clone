import streamlit as st
from app.pages import login_page, tweet_feed_page

def main():
    st.title('Twitter Clone - Streamlit Frontend')

    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
        st.session_state.refresh_token = None
        st.session_state.username = None
        st.session_state.password = None
        st.session_state.submitted = False

    if st.session_state.access_token:
        st.sidebar.markdown(f"Logged in as: **{st.session_state.username}**")

    if st.session_state.access_token:
        sidebar_options = ['Create Tweet & View Feed']
        st.sidebar.markdown("---")
        if st.sidebar.button('Logout'):
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            st.session_state.username = None
            st.session_state.password = None
            st.session_state.submitted = False
            st.success('Logged out successfully.')
            st.experimental_rerun()
    else:
        sidebar_options = ['Login']

    choice = st.sidebar.selectbox('Navigation', sidebar_options)

    if choice == 'Login':
        login_page.show()

    elif choice == 'Create Tweet & View Feed':
        tweet_feed_page.show()
        
    #TODO: Criar perfil e funcionalidade de seguir.

if __name__ == '__main__':
    main()
