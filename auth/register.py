import streamlit as st
import hashlib

from database import add_user, create_connection 
from pathlib import Path

def hash_password(password):
    """Hash the password using SHA256. This is essential for security."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_form():
    st.subheader("Create a New Account")

    with st.form(key='register_form'):
        new_name = st.text_input("Full Name", key='reg_name')
        new_email = st.text_input("Email (Used for Login)", key='reg_email')
        new_password = st.text_input("Password", type='password', key='reg_password')
        new_vehicle = st.text_input("Enter your EV Model (e.g., Tesla Model 3)", key='reg_vehicle')
        
        register_button = st.form_submit_button("Register")
 
    if register_button:
        if new_name and new_email and new_password and new_vehicle:
            
            
            conn = create_connection()
            if not conn:
                st.error("❌ Database connection failed during registration. Cannot save user.")
                return
 

            hashed_password = hash_password(new_password)
            
            
            success = add_user(conn, new_email, new_name, hashed_password, new_vehicle)
            conn.close()

            if success:
                st.success("✅ Registration Successful! Please log in above.")
            else:
                st.warning("⚠️ This email is already registered. Please try logging in or use a different email.")
        else:
            st.warning("Please fill in all fields.")