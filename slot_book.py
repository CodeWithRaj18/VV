import streamlit as st
from datetime import date, timedelta

# This data should be accessible in this file
CABLE_DETAILS = {
    "Type 1": {"time": 60, "price": 150},
    "Type 2": {"time": 75, "price": 200},
    "CCS": {"time": 45, "price": 250},
    "CHAdeMO": {"time": 50, "price": 220}
}

def get_slot_data():
    # Using sample data for demonstration
  today_slots = [
    {"time": "08:00 - 09:00 AM", "total": 5, "booked": 2},
    {"time": "09:00 - 10:00 AM", "total": 5, "booked": 5},
    {"time": "10:00 - 11:00 AM", "total": 5, "booked": 1},
    {"time": "11:00 - 12:00 PM", "total": 5, "booked": 0},
    {"time": "12:00 - 01:00 PM", "total": 5, "booked": 3},
    {"time": "01:00 - 02:00 PM", "total": 5, "booked": 4},
    {"time": "02:00 - 03:00 PM", "total": 5, "booked": 5},
    {"time": "03:00 - 04:00 PM", "total": 5, "booked": 2},
    {"time": "04:00 - 05:00 PM", "total": 5, "booked": 1}
    ]

  tomorrow_slots = [
    {"time": "08:00 - 09:00 AM", "total": 5, "booked": 0},
    {"time": "09:00 - 10:00 AM", "total": 5, "booked": 1},
    {"time": "10:00 - 11:00 AM", "total": 5, "booked": 0},
    {"time": "11:00 - 12:00 PM", "total": 5, "booked": 2},
    {"time": "12:00 - 01:00 PM", "total": 5, "booked": 4},
    {"time": "01:00 - 02:00 PM", "total": 5, "booked": 1},
    {"time": "02:00 - 03:00 PM", "total": 5, "booked": 3},
    {"time": "03:00 - 04:00 PM", "total": 5, "booked": 0},
    {"time": "04:00 - 05:00 PM", "total": 5, "booked": 2}
    ]

  return {"Today": today_slots, "Tomorrow": tomorrow_slots}


def slot_book():
    # --- Corrected Glassmorphic Theme CSS ---
    st.markdown(
        """
        <style>
        /* Whole App */
        .stApp {
            background: radial-gradient(circle at top left, rgb(117, 210, 202), rgba(95, 113, 111, 0.85), rgb(76, 95, 100));
        }
        /* Main Content Area Styling */
        .main .block-container {
            background: rgba(40, 40, 40, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(144, 238, 144, 0.4);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 0 30px rgba(144, 238, 144, 0.3); /* Glow for the container */
        }
        h1, h2, h3, h4, h5, h6, .stSubheader {
            color: #bfffc8;
            text-shadow: 0px 0px 8px rgba(144, 238, 144, 0.8); /* Glow for text */
        }
        .stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div {
            border: 2px solid rgba(144, 238, 144, 0.6) !important;
            border-radius: 10px;
            background: rgba(42, 42, 42, 0.8) !important;
            color: #f1f1f1 !important;
        }
        .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus, .stSelectbox > div > div:focus-within {
            border-color: #90ee90 !important;
            box-shadow: 0px 0px 15px #90ee90; /* ADDED: Glow effect for focused inputs */
            outline: none !important;
        }
        label { color: #a8ffb0 !important; font-weight: bold; }
        .stButton > button {
            background: linear-gradient(135deg, #90ee90, #5cd65c);
            color: #0a0a0a !important;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
            border: none;
            box-shadow: 0 0 20px rgba(144, 238, 144, 0.5); /* ADDED: Glow effect for buttons */
            transition: all 0.3s ease-in-out;
        }
        .stButton > button:hover {
             box-shadow: 0 0 25px #90ee90, 0 0 40px rgba(144, 238, 144, 0.8); /* ADDED: Enhanced glow on hover */
             transform: scale(1.02);
        }
        .stAlert { border-radius: 10px; }
        .stAlert.st-success { background: rgba(144, 238, 144, 0.1); border-left: 5px solid #90ee90; color: #bfffc8;}
        .stAlert.st-info { background: rgba(100, 149, 237, 0.1); border-left: 5px solid #6495ED; color: #b0c4de;}
        .stAlert.st-warning { background: rgba(255, 165, 0, 0.1); border-left: 5px solid #ffa500; color: #ffdead;}
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- The rest of your Python code is unchanged ---
    if 'confirming_booking' in st.session_state:
        slot_info = st.session_state['confirming_booking']
        cable_info = CABLE_DETAILS[slot_info["cable_type"]]
        with st.container(border=True):
            st.subheader("Confirm Your Booking")
            # ... (confirmation details)
            st.markdown(f"**Time Slot:** {slot_info['time_slot']}")
            st.markdown(f"**Cable Type:** {slot_info['cable_type']}")
            st.info(f"**Expected Charging Time:** {cable_info['time']} minutes")
            st.success(f"**Price:** ₹{cable_info['price']}")
            st.warning("Do you want to proceed to the payment page?")
            col1, col2 = st.columns(2)
            if col1.button("Confirm and Proceed to Payment", use_container_width=True, type="primary"):
                st.session_state['payment_params'] = st.session_state['confirming_booking']
                del st.session_state['confirming_booking']
                st.session_state['page'] = 'payment'
                st.rerun()
            if col2.button("Cancel", use_container_width=True):
                del st.session_state['confirming_booking']
                st.rerun()
        st.stop()

    # --- The main booking page UI starts here ---
    st.title("Book EV Charging Slot")

    if st.button("⬅️ Back to Map"):
        st.session_state['page'] = 'home'
        st.rerun()

    if 'selected_day' not in st.session_state:
        st.session_state.selected_day = "Today"

    slot_data = get_slot_data()
    cable_options = list(CABLE_DETAILS.keys())

    cols = st.columns(2)
    with cols[0]:
        if st.button("Today", use_container_width=True, type="primary" if st.session_state.selected_day == "Today" else "secondary"):
            st.session_state.selected_day = "Today"
            st.rerun()
    with cols[1]:
        if st.button("Tomorrow", use_container_width=True, type="primary" if st.session_state.selected_day == "Tomorrow" else "secondary"):
            st.session_state.selected_day = "Tomorrow"
            st.rerun()
            
    st.header(f"Available Slots for {st.session_state.selected_day}", divider="gray")

    header_cols = st.columns([2, 2, 2, 1])
    header_cols[0].markdown("**Time Slot**")
    header_cols[1].markdown("**Availability**")
    header_cols[2].markdown("**Cable Type**")
    header_cols[3].markdown("**Actions**")
    st.divider()

    active_slots = slot_data[st.session_state.selected_day]
    for slot in active_slots:
        free_slots = slot["total"] - slot["booked"]
        row_cols = st.columns([2, 2, 2, 1])
        row_cols[0].write(slot["time"])
        if free_slots == 0:
            row_cols[1].markdown(":red[**Fully Booked**]")
        else:
            row_cols[1].write(f"{free_slots} Free / {slot['booked']} Booked")

        if free_slots > 0:
            unique_key = f"{st.session_state.selected_day}_{slot['time']}"
            selected_cable = row_cols[2].selectbox(
                "Select Cable", options=cable_options, key=f"cable_{unique_key}",
                label_visibility="collapsed"
            )
            
            if row_cols[3].button("Book", key=f"book_{unique_key}"):
                booking_date = date.today() if st.session_state.selected_day == "Today" else date.today() + timedelta(days=1)
                cable_info = CABLE_DETAILS[selected_cable]
                st.session_state['confirming_booking'] = {
                    "date": booking_date.strftime("%Y-%m-%d"),
                    "time_slot": slot["time"],
                    "cable_type": selected_cable,
                    "charging_time": cable_info["time"],
                    "price": cable_info["price"]
                }
                st.rerun()
        else:
            row_cols[2].write("-")
            row_cols[3].write("-")