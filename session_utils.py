import streamlit as st


def apply_theme():
    """
    Global CSS applied on every page (logged-in or not).
    Colors secondary buttons too (Streamlit only colors 'primary'
    buttons via theme.toml by default; secondary stays plain white).
    Call this once near the top of every page, right after
    st.set_page_config().
    """

    st.markdown(
        """
        <style>
        /* Secondary buttons — light teal tint instead of plain white */
        button[kind="secondary"] {
            background-color: #F0FDFA !important;
            border: 2px solid #0EA5A5 !important;
            color: #0F766E !important;
            font-weight: 600 !important;
        }
        button[kind="secondary"]:hover {
            background-color: #CCFBF1 !important;
            border-color: #0F766E !important;
            color: #0F766E !important;
        }

        /* Primary buttons — a bit bolder text + consistent radius */
        button[kind="primary"] {
            font-weight: 700 !important;
        }

        button[kind="primary"], button[kind="secondary"] {
            border-radius: 10px !important;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background: #F0FDFA;
            border: 1px solid #99F6E4;
            border-radius: 12px;
            padding: 14px 16px;
        }

        /* Sidebar background tint */
        section[data-testid="stSidebar"] {
            background-color: #F8FAFC;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def show_hero(subtitle="Intelligent Document Q&A Assistant"):
    """
    Renders the same branded gradient banner used on the landing
    screen. Call this near the top of any page (after apply_theme())
    to keep branding consistent across the whole app.
    """

    st.markdown(
        f"""
        <style>
        .documind-hero {{
            background: linear-gradient(135deg, #0F172A 0%, #0EA5A5 100%);
            padding: 28px 36px;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.2);
        }}
        .documind-hero h1 {{
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.9rem !important;
            margin-bottom: 4px !important;
            letter-spacing: 0.3px;
        }}
        .documind-hero p {{
            color: #CCFBF1 !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            margin: 0 !important;
        }}
        </style>

        <div class="documind-hero">
            <h1>📄 DocuMind AI</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
def require_login():
    """
    Call this at the top of every page that needs a logged-in user.
    - Blocks the page (with a branded login/register prompt) if
      nobody is logged in.
    - Hides "Login" and "Register" from the sidebar nav once logged in.
    - Adds a working "Logout" button to the sidebar.
    """

    apply_theme()

    if "logged_in" not in st.session_state or not st.session_state.get("logged_in"):

        show_hero()

        st.markdown(
            """
            <style>
            .documind-guide {
                background: #F1F5F9;
                border-left: 6px solid #0EA5A5;
                padding: 16px 20px;
                border-radius: 10px;
                font-size: 1.02rem;
                margin-bottom: 20px;
                color: #1E293B;
            }
            .documind-guide b {
                color: #0F766E;
            }
            .documind-guide div {
                margin-bottom: 4px;
            }
            </style>

            <div class="documind-guide">
                <div>🔑 <b>Already have an account?</b> Click <b>Login</b> below.</div>
                <div>✨ <b>New here?</b> Click <b>Register</b> to create a free account first.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔐  Login", use_container_width=True, type="primary"):
                st.switch_page("pages/Login.py")

        with col2:
            if st.button("📝  Register", use_container_width=True, type="primary"):
                st.switch_page("pages/Register.py")

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
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            for key in ["logged_in", "user_id", "username", "conversation_id"]:
                st.session_state.pop(key, None)
            st.switch_page("pages/Login.py")