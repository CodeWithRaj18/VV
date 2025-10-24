# LAX_EV_Station: A Streamlit Booking Platform

*An interactive web application built with Streamlit for finding, booking, and managing electric vehicle charging slots.*

---
## About The Project

As the adoption of electric vehicles grows, the need for a seamless and efficient charging infrastructure becomes critical. EV Charge-Hub is a web-based platform designed to simplify the process of locating and reserving charging stations. Users can register, add their vehicles, and browse an interactive map to find nearby stations. The entire booking and confirmation process is handled within the app, providing a smooth experience from discovery to payment.

This project demonstrates a modern, multi-page application structure within Streamlit, integrating user authentication, interactive maps, and a stateful navigation system.

---
## Key Features ✨

* **Secure User Authentication**: A complete login and registration system that securely stores user data. Passwords are **hashed** using `passlib` for enhanced security.
* **Interactive Map Dashboard**: A dynamic dashboard powered by **Folium** that displays charging stations on a map. It uses **marker clustering** to keep the view clean in dense areas.
* **Click-to-Book**: Users can click directly on a station's marker on the map to initiate the booking process.
* **Vehicle Management**: Users can register their vehicles, which are loaded from a central `user.json` file.
* **End-to-End Booking Workflow**:
    1.  **Slot Selection**: A dedicated page to choose a date and time slot for charging.
    2.  **In-App Confirmation**: A pop-up view appears on the booking page to confirm details like price and time before proceeding.
    3.  **UPI Payment Integration**: A payment page that generates a unique UPI link and QR code for the transaction.
    4.  **Digital QR Code Ticket**: A final confirmation page that displays all booking details and a scannable QR code that acts as a digital ticket.
* **Custom Theming**: A modern, custom-styled UI applied across all pages for a consistent and professional look.

---
## Built With

This project is built with Python and several powerful libraries:

* **Framework**: [Streamlit](https://streamlit.io/)
* **Mapping**: [Folium](https://python-visualization.github.io/folium/) & [streamlit-folium](https://github.com/randyzwitch/streamlit-folium)
* **Password Hashing**: [passlib](https://passlib.readthedocs.io/en/stable/)
* **QR Code Generation**: [qrcode](https://github.com/lincolnloop/python-qrcode)
* **Frontend Interaction**: [streamlit_js_eval](https://github.com/aghasemi/streamlit_js_eval) for browser geolocation.

---
## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Make sure you have Python 3.8+ and pip installed on your system.

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    Create a file named `requirements.txt` and paste the following lines into it.
    ```txt
    streamlit
    folium
    streamlit-folium
    streamlit_js_eval
    passlib
    qrcode
    Pillow
    ```
    Then, run the installation command:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your data file:**
    * Create a folder named `data`.
    * Inside it, create an empty `user.json` file. The app will populate this file when you register a new user.
    ```json
    {}
    ```

5.  **Run the application:**
    ```sh
    streamlit run app.py
    ```
    Open your browser and navigate to the local URL provided by Streamlit.

---
