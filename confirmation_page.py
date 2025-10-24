import streamlit as st
import qrcode
import json
from io import BytesIO

def confirmation_page():
    # --- Glassmorphic Theme CSS ---
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
            border: 2px solid rgb(27, 31, 27);
            box-shadow: 0 0 20px rgba(144, 238, 144, 0.6);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("✅ Booking Confirmed!")
    st.balloons()

    if 'payment_params' not in st.session_state:
        st.error("Booking details not found. Please return to the home page.")
        if st.button("Go Home"):
            st.session_state['page'] = 'home'
            st.rerun()
        return

    booking_details = st.session_state['payment_params']
    
    # Add the user's email to the booking details for the QR code
    booking_details['user_email'] = st.session_state.get('email', 'N/A')

    # --- Display Booking Summary ---
    st.subheader("Here is your booking summary and QR code:")
    with st.container(border=True):
        st.markdown(f"**Date:** {booking_details['date']}")
        st.markdown(f"**Time Slot:** {booking_details['time_slot']}")
        st.markdown(f"**Cable Type:** {booking_details['cable_type']}")
        st.markdown(f"**Price Paid:** ₹{booking_details['price']}")

    st.divider()

    # --- Generate and Display QR Code ---
    st.subheader("Scan this QR Code at the charging station:")

    qr_data = json.dumps(booking_details, indent=4)
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = BytesIO()
    img.save(buf)
    st.image(buf)

    st.info("This QR code contains all your booking information.")
    
    if st.button("Return to Home Page", use_container_width=True):
        del st.session_state['payment_params']
        st.session_state['page'] = 'home'
        st.rerun()
