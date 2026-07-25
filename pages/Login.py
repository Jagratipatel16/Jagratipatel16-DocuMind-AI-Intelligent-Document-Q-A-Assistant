import streamlit as st

from database.database import SessionLocal
from database.crud import login_user
from session_utils import apply_theme, show_hero

st.set_page_config(
    page_title="Login - DocuMind AI",
    page_icon="🔐"
)

apply_theme()
show_hero()

st.header("🔐 Login")
st.write("Already have an account? Login below.")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)


if st.button("Login", use_container_width=True, type="primary"):

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

st.divider()
st.caption("Don't have an account?")
if st.button("📝 Create a new account", use_container_width=True, type="secondary"):
    st.switch_page("pages/Register.py")