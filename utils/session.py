import streamlit as st

def init_session():
    if "users" not in st.session_state:
        st.session_state.users = {}
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None

def logout_user():
    st.session_state.logged_in = False
    st.session_state.current_user = None
