import streamlit as st

from database.database import SessionLocal
from database.models import User
from database.conversation_service import get_conversations
from database.history_service import get_user_history
from session_utils import require_login


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="DocuMind AI - Profile",
    page_icon="👤",
    layout="wide"
)


# -----------------------------------
# Login Check
# -----------------------------------

require_login()

st.title("👤 Profile")


# -----------------------------------
# User Info
# -----------------------------------

db = SessionLocal()
user = db.query(User).filter(User.id == st.session_state.user_id).first()
db.close()

if user:
    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Name", value=user.name, disabled=True)
        st.text_input("Email", value=user.email, disabled=True)

    with col2:
        st.text_input(
            "Member Since",
            value=user.created_at.strftime("%d %b %Y"),
            disabled=True
        )

st.divider()

conversations = get_conversations(st.session_state.user_id)
history = get_user_history(st.session_state.user_id)

col1, col2 = st.columns(2)
with col1:
    st.metric("💬 Total Conversations", len(conversations))
with col2:
    st.metric("❓ Total Questions Asked", len(history))