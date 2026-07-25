import streamlit as st
import plotly.graph_objects as go
from datetime import date, timedelta

from database.conversation_service import get_conversations
from database.history_service import get_user_history
from session_utils import require_login, show_hero


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

show_hero("Your activity at a glance")
st.subheader("📊 Dashboard")
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

st.header("📈 Activity — Last 7 Days")

if history:

    today = date.today()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    counts_by_date = {}
    for h in history:
        d = h.created_at.date()
        counts_by_date[d] = counts_by_date.get(d, 0) + 1

    labels = [d.strftime("%a") for d in last_7_days]
    values = [counts_by_date.get(d, 0) for d in last_7_days]
    colors = ["#5EEAD4" if d == today else "#0EA5A5" for d in last_7_days]

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker=dict(color=colors),
                text=[str(v) if v else "" for v in values],
                textposition="outside",
                hovertemplate="%{x}: %{y} question(s)<extra></extra>",
            )
        ]
    )

    try:
        fig.update_traces(marker_cornerradius=10)
    except Exception:
        pass

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=320,
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E2E8F0",
            zeroline=False,
            title=None,
            dtick=1
        ),
        xaxis=dict(showgrid=False, title=None),
        bargap=0.4,
        font=dict(color="#1E293B", size=13)
    )

    st.plotly_chart(fig, use_container_width=True)

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

            if st.button("Open in Chat →", key=f"open_{conv.id}", type="primary"):
                st.session_state.conversation_id = conv.id
                st.switch_page("pages/Chat.py")