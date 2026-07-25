import streamlit as st

from rag.retriever import retrieve_documents
from rag.llm import generate_answer

from database.conversation_service import (
    create_conversation,
    get_conversations,
    delete_conversation,
)
from database.chat_service import save_chat, get_messages
from session_utils import require_login


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="DocuMind AI - Chat",
    page_icon="💬",
    layout="wide"
)


# -----------------------------------
# Login Check
# -----------------------------------

require_login()

st.title("💬 Chat")


# -----------------------------------
# Sidebar — Conversation List
# -----------------------------------

st.sidebar.success(f"👤 {st.session_state.username}")
st.sidebar.divider()

if st.sidebar.button("➕ New Chat", use_container_width=True):
    st.session_state.pop("conversation_id", None)
    st.rerun()

st.sidebar.divider()
st.sidebar.header("Your Conversations")

conversations = get_conversations(st.session_state.user_id)

if not conversations:
    st.sidebar.caption("No conversations yet. Ask a question to start one!")

for conv in conversations:

    col1, col2 = st.sidebar.columns([4, 1])

    label = conv.title if len(conv.title) <= 30 else conv.title[:30] + "..."

    is_active = st.session_state.get("conversation_id") == conv.id

    with col1:
        if st.button(
            ("📌 " if is_active else "") + label,
            key=f"conv_{conv.id}",
            use_container_width=True
        ):
            st.session_state.conversation_id = conv.id
            st.rerun()

    with col2:
        if st.button("🗑️", key=f"del_{conv.id}"):
            delete_conversation(conv.id)
            if st.session_state.get("conversation_id") == conv.id:
                st.session_state.pop("conversation_id", None)
            st.rerun()


# -----------------------------------
# Main Chat Thread
# -----------------------------------

active_conversation_id = st.session_state.get("conversation_id")

if active_conversation_id:
    messages = get_messages(active_conversation_id)

    for msg in messages:
        with st.chat_message("user"):
            st.write(msg.question)
        with st.chat_message("assistant"):
            st.write(msg.answer)
else:
    st.info(
        "👋 This is a new chat. Ask a question below about your uploaded "
        "PDFs — upload documents first from the **Home** page if you "
        "haven't already."
    )


# -----------------------------------
# Chat Input
# -----------------------------------

query = st.chat_input("Ask something about your uploaded documents...")

if query:

    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            results = retrieve_documents(
                query,
                user_id=st.session_state.user_id
            )

            docs = [doc for doc, score in results]

            answer = generate_answer(query, docs)

            st.write(answer)

    # Create a conversation on the first message of a new chat
    if not active_conversation_id:
        active_conversation_id = create_conversation(
            st.session_state.user_id,
            title=query[:50]
        )
        st.session_state.conversation_id = active_conversation_id

    save_chat(active_conversation_id, query, answer)

    st.rerun()