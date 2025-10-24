import streamlit as st
import bcrypt
# Import necessary function from your database module
from database import add_user 
from pathlib import Path

# NOTE: bcrypt is used for secure password hashing
def hash_password(password):
    """Hashes the password using bcrypt for secure storage."""
    # Encode password to bytes, generate salt, hash it, and decode to string for storage
    password_bytes = password.encode('utf-8')
    password_hash_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return password_hash_bytes.decode('utf-8') # Return as string for storage

def register_form():
    st.subheader("Create a New Account")

    with st.form(key='register_form'):
        new_name = st.text_input("Full Name", key='reg_name')
        new_email = st.text_input("Email (Used for Login)", key='reg_email')
        new_password = st.text_input("Password", type='password', key='reg_password')
        # We assume new_vehicle is a single string input as per the database design
        new_vehicle = st.text_input("Enter your EV Model (e.g., Tesla Model 3)", key='reg_vehicle')
        
        register_button = st.form_submit_button("Register")
    
    # Process registration logic outside the form block
    if register_button:
        if new_name and new_email and new_password and new_vehicle:
            
            # --- DATABASE OPERATION (Supabase) ---
            
            # 1. Securely hash the password
            hashed_password = hash_password(new_password)
            
            # 2. Add user to the Supabase table
            # The add_user function handles the database connection and insertion.
            success = add_user(new_email, new_name, hashed_password, new_vehicle)

            if success:
                st.success("✅ Registration Successful! Please log in above.")
            else:
                # Failure indicates email collision (user already exists) or a DB connection error.
                st.warning("⚠️ Registration failed. This email may already be registered, or there was a database error.")
        else:
            st.warning("Please fill in all fields.")
