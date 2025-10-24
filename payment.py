import streamlit as st
import qrcode
from io import BytesIO

def payment_option():
   
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at top left, rgb(117, 210, 202), rgba(95, 113, 111, 0.85), rgb(76, 95, 100));
        }
        .main .block-container {
            background: rgba(40, 40, 40, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(144, 238, 144, 0.4);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 0 30px rgba(144, 238, 144, 0.3);
        }
        h1, h2, h3, h4, h5, h6, .stSubheader {
            color: #bfffc8;
            text-shadow: 0px 0px 8px rgba(144, 238, 144, 0.8);
        }
        .stButton > button {
            background: linear-gradient(135deg, #90ee90, #5cd65c);
            color: #0a0a0a !important;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stAlert { border-radius: 10px; }
        .stAlert.st-error { background: rgba(255, 100, 100, 0.1); border-left: 5px solid #ff4d4d; color: #ffcccc; }
        .stAlert.st-warning { background: rgba(255, 165, 0, 0.1); border-left: 5px solid #ffa500; color: #ffdead; }
        div[data-testid="stImage"] { text-align: center; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Title ---
    st.title("Complete Your Payment via UPI")

    # --- Session Check ---
    if 'payment_params' not in st.session_state:
        st.error("No booking information found. Please return to the booking page.")
        return

    params = st.session_state['payment_params']

    # --- Payment Details ---
    payee_upi_id = "your upi id"
    payee_name = "EV Charging Corp"

    with st.container(border=True):
        st.subheader("Booking Summary")
        st.markdown(f"**Date:** {params['date']}")
        st.markdown(f"**Time Slot:** {params['time_slot']}")
        st.markdown(f"**Cable Type:** {params['cable_type']}")
        st.markdown(f"#### Price to Pay: ₹{params['price']}")

    st.divider()

    # --- UPI QR Code Generation ---
    transaction_notes = f"Payment for slot {params['time_slot']}"
    upi_payment_link = (
        f"upi://pay?pa={payee_upi_id}&pn={payee_name}"
        f"&am={params['price']}&cu=INR&tn={transaction_notes}"
    )

    st.subheader("Payment Method")
    st.write("Scan the QR Code below with your UPI App:")

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(upi_payment_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf)

    st.image(buf)

    st.divider()

    # --- Payment Confirmation ---
    st.warning("After completing the payment in your UPI app, please click the button below.")

    if st.button("I have completed the payment", type="primary", use_container_width=True):
        st.session_state['page'] = 'confirmation'
        st.rerun()
