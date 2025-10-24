import streamlit as st
from pathlib import Path

def payment_option():
    st.title("Complete Your Payment")

    if 'payment_params' not in st.session_state:
        st.error("No booking info found!")
        return

    params = st.session_state['payment_params']
    payee_upi_id = "raj5530000@okicici"  # Your UPI ID

    st.subheader("Booking Summary")
    st.markdown(f"**Date:** {params['date']}")
    st.markdown(f"**Time Slot:** {params['time_slot']}")
    st.markdown(f"**Cable Type:** {params['cable_type']}")
    st.markdown(f"#### Price to Pay: ₹{params['price']}")
    st.divider()

    payment_method = st.radio("Choose Payment Method:", ["UPI", "Cash"])

    if payment_method == "UPI":
        st.subheader("Pay via UPI")
        qr_path = Path(__file__).parent / "my_upi_qr.jpg"
        if qr_path.exists():
            st.image(str(qr_path), caption="Scan to Pay", use_container_width=False)
        st.markdown(f"**UPI ID:** `{payee_upi_id}`")
        st.info("After completing the payment, upload the payment screenshot for verification:")

        uploaded_file = st.file_uploader("Upload Screenshot (JPG/PNG)", type=["png", "jpg", "jpeg"])
        
        if uploaded_file:
            # Optional: simple filename check
            if payee_upi_id.split("@")[0] in uploaded_file.name:
                st.success("Screenshot uploaded & verified! You can now proceed.")
                st.session_state['payment_done'] = True
            else:
                st.error("UPI ID in screenshot does not match! Payment cannot be verified.")

    else:  # Cash payment
        st.subheader("Pay by Cash")
        st.info(f"Please pay ₹{params['price']} at the station.")
        if st.checkbox("I will pay by cash at station"):
            st.session_state['payment_done'] = True
            st.success("Cash payment selected! You can now proceed.")

    st.divider()

    if st.session_state.get('payment_done', False):
        if st.button("Proceed to Confirmation"):
            st.session_state['page'] = 'confirmation'
            st.rerun()
    else:
        st.info("Complete your payment first to proceed.")
