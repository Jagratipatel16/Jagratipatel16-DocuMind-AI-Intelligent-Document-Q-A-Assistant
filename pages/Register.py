import streamlit as st

from database.database import SessionLocal
from database.crud import create_user
from session_utils import apply_theme, show_hero

st.set_page_config(
    page_title="Register - DocuMind AI",
    page_icon="📝"
)

apply_theme()
show_hero()

st.header("📝 Register")
st.write("New here? Create a new DocuMind AI account.")

name = st.text_input("Full Name")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

confirm_password = st.text_input(
    "Confirm Password",
    type="password"
)


if st.button("Register", use_container_width=True, type="primary"):

    if not name or not email or not password or not confirm_password:

        st.error("Please fill all fields.")

    elif password != confirm_password:

        st.error("Passwords do not match.")

    else:

        db = SessionLocal()

        user = create_user(
            db=db,
            name=name,
            email=email,
            password=password
        )

        db.close()

        if user:

            st.success("Registration Successful! Please login now.")

        else:

            st.error("Email already exists.")

st.divider()
st.caption("Already have an account?")
if st.button("🔐 Login instead", use_container_width=True, type="secondary"):
    st.switch_page("pages/Login.py")