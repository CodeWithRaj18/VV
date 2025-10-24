import streamlit as st
from pathlib import Path

def payment_option():
    # --- CSS Styling ---
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

    st.title("Complete Your Payment")

    # --- Session Check ---
    if 'payment_params' not in st.session_state:
        st.error("No booking information found. Please return to the booking page.")
        return

    params = st.session_state['payment_params']

    # --- Payment Details ---
    payee_upi_id = "raj5530000@okicici"  # Your UPI ID
    payee_name = "EV Charging Corp"

    # --- Booking Summary ---
    with st.container(border=True):
        st.subheader("Booking Summary")
        st.markdown(f"**Date:** {params['date']}")
        st.markdown(f"**Time Slot:** {params['time_slot']}")
        st.markdown(f"**Cable Type:** {params['cable_type']}")
        st.markdown(f"#### Price to Pay: ₹{params['price']}")

    st.divider()

    # --- Payment Method Selection ---
    payment_method = st.radio(
        "Choose Payment Method:",
        options=["UPI", "Cash"]
    )

    # --- UPI Payment ---
    if payment_method == "UPI":
        st.subheader("Pay via UPI")
        st.write("Scan this QR Code in your UPI app:")

        qr_path = Path(__file__).parent / "my_upi_qr.jpg"
        if not qr_path.exists():
            st.error("QR code image not found!")
            return

        st.image(str(qr_path), caption="Scan to Pay", use_container_width=False)
        st.markdown(f"**UPI ID:** `{payee_upi_id}`")
        st.warning("After completing the payment in your UPI app, please click the button below.")

        if st.button("I have completed the UPI payment"):
            st.session_state['payment_done'] = True
            st.success("UPI payment confirmed! You can now proceed.")

    # --- Cash Payment ---
    else:
        st.subheader("Pay by Cash")
        st.info(f"Please pay ₹{params['price']} at the station before charging begins.")

        if st.button("I will pay by cash at station"):
            st.session_state['payment_done'] = True
            st.success("Cash payment selected! You can now proceed.")

    st.divider()

    # --- Proceed to Confirmation ONLY if Payment Done ---
    if st.session_state.get('payment_done', False):
        if st.button("Proceed to Confirmation"):
            st.session_state['page'] = 'confirmation'
            st.rerun()
    else:
        st.info("Complete your payment first to proceed.")
