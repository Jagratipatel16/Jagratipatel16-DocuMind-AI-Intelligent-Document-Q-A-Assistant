import streamlit as st


def require_login():
    """
    Call this at the top of every page that needs a logged-in user.
    - Blocks the page (with a warning) if nobody is logged in.
    - Hides "Login" and "Register" from the sidebar nav once logged in.
    - Adds a working "Logout" button to the sidebar.
    """

    if "logged_in" not in st.session_state or not st.session_state.get("logged_in"):
        st.warning("🔐 Please Login First")
        st.stop()

    # Hide Login / Register links from the sidebar nav for logged-in users
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] a[href*="Login"],
        [data-testid="stSidebarNav"] a[href*="Register"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            for key in ["logged_in", "user_id", "username", "conversation_id"]:
                st.session_state.pop(key, None)
            st.switch_page("pages/Login.py")