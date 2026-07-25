import streamlit as st
import pandas as pd

from database.conversation_service import get_conversations
from database.history_service import get_user_history
from session_utils import require_login


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="DocuMind AI - Dashboard",
    page_icon="📊",
    layout="wide"
)


# -----------------------------------
# Login Check
# -----------------------------------

require_login()

st.title("📊 Dashboard")
st.caption(f"Welcome back, {st.session_state.username} 👋")


# -----------------------------------
# Fetch Data
# -----------------------------------

conversations = get_conversations(st.session_state.user_id)
history = get_user_history(st.session_state.user_id)


# -----------------------------------
# Summary Metrics
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💬 Total Conversations", len(conversations))

with col2:
    st.metric("❓ Total Questions Asked", len(history))

with col3:
    last_active = history[0].created_at.strftime("%d %b %Y") if history else "—"
    st.metric("🕒 Last Active", last_active)

st.divider()


# -----------------------------------
# Activity Over Time
# -----------------------------------

st.header("📈 Activity")

if history:
    df = pd.DataFrame(
        [{"date": h.created_at.date()} for h in history]
    )

    daily_counts = (
        df.groupby("date")
        .size()
        .reset_index(name="questions")
        .set_index("date")
    )

    st.bar_chart(daily_counts)
else:
    st.caption("No activity yet — start a chat to see your stats here.")

st.divider()


# -----------------------------------
# Recent Conversations
# -----------------------------------

st.header("🗂️ Your Conversations")

if not conversations:
    st.caption("You haven't started any conversations yet.")
else:
    for conv in conversations:

        msg_count = sum(
            1 for h in history
        )  # placeholder, refined below

        with st.expander(
            f"📌 {conv.title}  —  {conv.created_at.strftime('%d %b %Y, %I:%M %p')}"
        ):
            conv_messages = [h for h in history if h.conversation_id == conv.id]

            st.caption(f"{len(conv_messages)} message(s) in this conversation")

            if st.button("Open in Chat →", key=f"open_{conv.id}"):
                st.session_state.conversation_id = conv.id
                st.switch_page("pages/Chat.py")