import streamlit as st
from pathlib import Path

def payment_option():
    st.title("Complete Your Payment")

    if 'payment_params' not in st.session_state:
        st.error("No booking info found!")
        return

    params = st.session_state['payment_params']
    payee_upi_id = "raj5530000@okicici"

    st.subheader("Booking Summary")
    st.markdown(f"**Date:** {params['date']}")
    st.markdown(f"**Time Slot:** {params['time_slot']}")
    st.markdown(f"**Cable Type:** {params['cable_type']}")
    st.markdown(f"#### Price to Pay: ₹{params['price']}")
    st.divider()

    payment_method = st.radio("Choose Payment Method:", ["UPI", "Cash"])

    payment_done = False  # local flag

    if payment_method == "UPI":
        st.subheader("Pay via UPI")
        qr_path = Path(__file__).parent / "my_upi_qr.jpg"
        if qr_path.exists():
            st.image(str(qr_path), caption="Scan to Pay", use_container_width=False)
        st.markdown(f"**UPI ID:** `{payee_upi_id}`")
        st.info("After completing the payment, upload the screenshot:")

        uploaded_file = st.file_uploader("Upload Screenshot (JPG/PNG)", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            payment_done = True
            st.success("Screenshot uploaded! You can now proceed.")

    else:  # Cash payment
        st.subheader("Pay by Cash")
        st.info(f"Please pay ₹{params['price']} at the station.")
        if st.checkbox("I will pay by cash at station"):
            payment_done = True
            st.success("Cash payment selected! You can now proceed.")

    st.divider()

    # --- Show Proceed button ONLY if payment_done ---
    if payment_done:
        if st.button("Proceed to Confirmation"):
            st.session_state['payment_done'] = True
            st.session_state['page'] = 'confirmation'
            st.rerun()
    else:
        st.info("Complete your payment first to proceed.")
