import streamlit as st

from database.database import SessionLocal
from database.crud import login_user


st.set_page_config(
    page_title="Login",
    page_icon="🔐"
)

st.title("🔐 Login")

st.write("Welcome back to DocuMind AI")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)


if st.button("Login"):

    db = SessionLocal()

    user = login_user(
        db,
        email,
        password
    )

    db.close()

    if user:

        st.session_state.logged_in = True
        st.session_state.user_id = user.id
        st.session_state.username = user.name

        st.success(f"Welcome {user.name}!")

        st.switch_page("app.py")

    else:

        st.error("Invalid Email or Password")