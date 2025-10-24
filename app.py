import streamlit as st
from auth.login import login_form
from auth.register import register_form
from utils.session import init_session, logout_user
from home import home_page
from slot_book import slot_book
from payment import payment_option
from confirmation_page import confirmation_page


def main():
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}   /* hamburger menu */
            footer {visibility: hidden;}      /* footer */
            header {visibility: hidden;}      /* top header */
            </style>
            <style>
            .block-container {
            padding-top: 1rem;   /* reduce from ~6rem default */
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
            }
            </style>


            """ 
    st.markdown(hide_st_style, unsafe_allow_html=True)
    



    st.set_page_config(page_title="Streamlit Modular App", layout="centered")
    init_session()

    if not st.session_state.logged_in:

          

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            login_form()

        with tab2:
            register_form()

    else:
        page = st.session_state.get("page", "home")

        if page == "home":
            if page == "home":
            # Get the current user's email (or username) from the session state
                current_user = st.session_state.get('email') 
                
                if current_user:
                    # Pass the user's info to the function
                    home_page(current_user)
                else:
                    st.error("Could not find user information. Please log in again.")
        elif page == "book":
            slot_book()
        elif page == "payment":
            payment_option()
        elif page == "confirmation": # <-- 2. ADD THIS NEW ROUTE
            confirmation_page()
        
        

if __name__ == "__main__":
    main()
