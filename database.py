import streamlit as st
from supabase import create_client, Client
import bcrypt # Required for password verification logic
import uuid # Required for generating unique booking IDs
from datetime import datetime

# --- Supabase Initialization ---
# Supabase credentials MUST be set in your .streamlit/secrets.toml file under the [supabase] section.
try:
    SUPABASE_URL = st.secrets["supabase"]["URL"]
    SUPABASE_ANON_KEY = st.secrets["supabase"]["ANON_KEY"]
except KeyError:
    # This error handles cases where secrets are not set up correctly in Streamlit Cloud
    st.error("❌ SUPABASE SETUP ERROR: Please ensure URL and ANON_KEY are correctly defined in Streamlit Secrets under the [supabase] header.")
    st.stop()

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# --- Supabase Table Names ---
USERS_TABLE = "users"
BOOKINGS_TABLE = "bookings" 

# ----------------------------
# USER REGISTRATION AND LOGIN FUNCTIONS
# ----------------------------

def add_user(email, name, password_hash, vehicle_model):
    """Adds a new user record to the Supabase 'users' table."""
    try:
        # Check if user already exists
        user_record = supabase.table(USERS_TABLE).select("email").eq("email", email).execute()
        
        if len(user_record.data) > 0:
            return False # User already exists

        # Prepare data for insertion (keys must match Supabase table columns!)
        data = {
            "email": email,
            "name": name,
            "password_hash": password_hash,
            "vehicles": vehicle_model # Storing vehicle model as a string
        }

        # Insert the new user record
        supabase.table(USERS_TABLE).insert(data).execute()
        return True

    except Exception as e:
        st.error(f"❌ Database Error during registration: {e}")
        return False


def get_user(email):
    """Retrieves a user's details from the Supabase 'users' table by email."""
    try:
        # Query the users table
        response = supabase.table(USERS_TABLE).select("*").eq("email", email).execute()
        
        if response.data:
            user_data = response.data[0]
            # Convert the vehicles string back to a list (important for home.py)
            vehicles_list = [user_data.get('vehicles', '').strip()] if user_data.get('vehicles') else []
            
            # Return a dictionary compatible with the rest of the application
            return {
                "name": user_data['name'],
                "password_hash": user_data['password_hash'],
                "vehicles": vehicles_list
            }
        else:
            return None # User not found

    except Exception as e:
        # We catch the exception and return None, letting the calling function handle the error message
        # st.error(f"❌ Database Error: Failed to retrieve user. Details: {e}")
        return None

# ----------------------------
# BOOKING FUNCTIONS
# ----------------------------

def add_booking(booking_details):
    """Records a new successful booking into the Supabase 'bookings' table."""
    try:
        booking_id = f"EVB-{uuid.uuid4().hex[:8].upper()}"
        
        # Prepare data for insertion (keys must match Supabase table columns!)
        data = {
            "booking_id": booking_id,
            "user_email": booking_details.get('user_email', 'N/A'),
            "station_name": booking_details.get('station', 'N/A'),
            "vehicle_model": booking_details.get('vehicle', 'N/A'),
            "date_time": f"{booking_details['date']} {booking_details['time_slot'].split(' - ')[0]}", 
            "cable_type": booking_details.get('cable_type', 'N/A'),
            "cost": booking_details.get('price', 0),
            "status": "Confirmed"
        }
        
        supabase.table(BOOKINGS_TABLE).insert(data).execute()
        return True, booking_id

    except Exception as e:
        st.error(f"❌ Database Error during booking: {e}")
        return False, None
