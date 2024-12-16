import streamlit as st
import sqlite3
import hashlib
import time

# Database setup
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 username TEXT PRIMARY KEY, 
                 password TEXT)''')
    conn.commit()
    conn.close()

# Hashing function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Add a new user to the database
def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
    conn.commit()
    conn.close()

# Authenticate user login
def authenticate(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result and hash_password(password) == result[0]:
        return True
    return False

# Main function
def main():
    st.title("Power BI Dashboard")

    # Initialize the database
    init_db()

    # Session state for login
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = ""

    # Login or Sign-Up selection
    page = st.sidebar.selectbox("Select Action", ["Login", "Sign Up"])

    if page == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            with st.spinner("Authenticating..."):
                time.sleep(1)  # Simulate authentication delay
                if authenticate(username, password):
                    st.success("Login successful!")
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                else:
                    st.error("Invalid username or password. Please try again.")

    elif page == "Sign Up":
        st.subheader("Sign Up")
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):
            if new_password != confirm_password:
                st.error("Passwords do not match!")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                try:
                    add_user(new_username, new_password)
                    st.success("Account created successfully! Please go to the Login page to log in.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please choose a different one.")

    # Dashboard page
    if st.session_state["logged_in"]:
        st.subheader(f"Welcome, {st.session_state['username']}!")
        st.subheader("Power BI Dashboard")
        POWERBI_EMBED_URL = "https://app.powerbi.com/reportEmbed?reportId=616b6d4f-da33-44c7-82a6-6c68a1b025fb&autoAuth=true&ctid=4398c2fc-05c1-4a0b-a312-c86b714cbc9a"  # Replace with your Power BI URL
        st.markdown(
            f'<iframe width="100%" height="600" src="{POWERBI_EMBED_URL}" frameborder="0" allowFullScreen="true"></iframe>',
            unsafe_allow_html=True
        )
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.experimental_rerun()

if __name__ == "__main__":
    main()
