import streamlit as st
import json
from pathlib import Path

# ------------------- JSON file -------------------
DATA_FILE = Path("data/user.json")

# ------------------- Load users -------------------
if "users" not in st.session_state:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            st.session_state.users = json.load(f)
    else:
        st.session_state.users = {}

# ------------------- Dummy current user -------------------
# In real login, set st.session_state.current_user dynamically
if "current_user_email" not in st.session_state:
    st.session_state.current_user_email = "test@example.com"

current_email = st.session_state.current_user_email
if current_email not in st.session_state.users:
    # Create a blank profile if user does not exist
    st.session_state.users[current_email] = {
        "name": "",
        "age": "",
        "vehicle": "",
        "station_id": ""
    }

user_data = st.session_state.users[current_email]

st.title("User Profile")

# ------------------- Editable Fields -------------------
with st.form("profile_form"):
    name = st.text_input("Name", value=user_data.get("name", ""))
    age = st.text_input("Age", value=user_data.get("age", ""))
    vehicle = st.text_input("Vehicle Type", value=user_data.get("vehicle", ""))
    station_id = st.text_input("Station ID", value=user_data.get("station_id", ""))

    submitted = st.form_submit_button("Save Profile")
    if submitted:
        # Update JSON
        st.session_state.users[current_email]["name"] = name
        st.session_state.users[current_email]["age"] = age
        st.session_state.users[current_email]["vehicle"] = vehicle
        st.session_state.users[current_email]["station_id"] = station_id

        with open(DATA_FILE, "w") as f:
            json.dump(st.session_state.users, f, indent=4)

        st.success("Profile updated successfully!")

# ------------------- Show Current Data -------------------
st.subheader("Current Profile Data")
st.json(st.session_state.users[current_email])
