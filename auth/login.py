import streamlit as st
import bcrypt
# Import necessary functions from your database module
from database import get_user 

def hash_password(password):
    """Placeholder function (actual hashing is handled by bcrypt.checkpw)."""
    return password.encode('utf-8') 

def login_user(email, password):
    
    # 1. Database Lookup (using Supabase)
    user_data = get_user(email)

    # Check if the user was found and data is valid
    if user_data and user_data.get('password_hash'):
        
        # 2. Password Verification (using bcrypt)
        # Stored hash must be bytes, so we encode the stored string hash
        stored_hash = user_data["password_hash"].encode('utf-8')
        password_bytes = password.encode('utf-8')

        try:
            # Check the password against the stored hash
            if bcrypt.checkpw(password_bytes, stored_hash):
                # Login successful
                st.session_state['logged_in'] = True
                st.session_state['email'] = email
                
                # Store user data for easy access on the home page
                st.session_state['users'] = {email: user_data} 
                
                return True, "Login successful!"
            else:
                return False, "Invalid email or password."
        except Exception:
            # Catches errors during the bcrypt check (e.g., if the stored hash is invalid)
            return False, "Login failed. Error during password verification."
    else:
        # Handles user not found or database error (error message handled in database.py)
        return False, "Invalid email or password."


def login_form():
    
    # --- CSS Styles remain unchanged ---
    st.markdown(
        """
        <style>
        /* Whole App */
        .stApp {
            background: radial-gradient(circle at top left,rgb(117, 210, 202),rgba(95, 113, 111, 0.85),rgb(76, 95, 100));
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        
        /* Glassmorphic Container */
        .main .block-container {
            background: rgba(245, 240, 240, 0.92); /* Transparent silver */
            backdrop-filter: blur(12px); /* Frosted glass */
            border: 1px solid rgba(225, 16, 1, 0.4);
            border-radius: 20px;
            padding: 50px 40px;
            box-shadow: 0 0 30px rgba(217, 228, 217, 0.3);
            max-width: 420px;
            margin: auto;
            animation: floatCard 6s ease-in-out infinite;
        }

        @keyframes floatCard {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            color: #bfffc8;
            text-shadow: 0px 0px 8px rgba(144, 238, 144, 0.8);
            text-align: center;
        }

        /* Inputs */
        .stTextInput > div > div > input {
            border: 2px solid rgba(144, 238, 144, 0.6) !important;
            border-radius: 10px;
            padding: 12px;
            background: rgba(42, 42, 42, 0.8) !important;
            color: #f1f1f1 !important;
            font-weight: 500;
            transition: all 0.3s ease-in-out;
        }
        .stTextInput > div > div > input:focus {
            border-color: #90ee90 !important;
            box-shadow: 0px 0px 15px #90ee90;
            outline: none !important;
        }

        /* Labels */
        label {
            color: #a8ffb0 !important;
            font-weight: bold;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #90ee90, #5cd65c);
            color: #0a0a0a !important;
            border-radius: 10px;
            padding: 12px 25px;
            font-weight: bold;
            font-size: 16px;
            border: none;
            box-shadow: 0 0 20px rgba(144, 238, 144, 0.5);
            transition: all 0.3s ease-in-out;
            width: 100%;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #a8ffb0, #77dd77);
            box-shadow: 0 0 25px #90ee90, 0 0 40px rgba(144, 238, 144, 0.8);
            transform: scale(1.05);
        }

        /* Alerts */
        .stAlert.success {
            background: rgba(144, 238, 144, 0.1);
            border-left: 5px solid #90ee90;
            color: #bfffc8;
            border-radius: 10px;
            backdrop-filter: blur(6px);
        }
        .stAlert.error {
            background: rgba(255, 100, 100, 0.1);
            border-left: 5px solid #ff4d4d;
            color: #ffcccc;
            border-radius: 10px;
            backdrop-filter: blur(6px);
        }

        /* Logo */
        .logo-container {
            text-align: center;
            margin-bottom: 25px;
        }
        .logo-container img {
            max-width: 160px;
            border-radius: 50%;
            border: 2px solidrgb(27, 31, 27);
            box-shadow: 0 0 20px rgba(144, 238, 144, 0.6);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # --- Logo at the top ---
    st.markdown(
        """
<div class="logo-container">
    <img src="https://iili.io/KkSVSFn.md.jpg" alt="LAX EV Station Logo">
</div>

        """,
        unsafe_allow_html=True
    )

    st.subheader("Login")
    
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email_form")
        password = st.text_input("Password", type="password", key="login_password_form")
        
        submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            success, msg = login_user(email, password)
            
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)