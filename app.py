import streamlit as st

from rag.loader import save_uploaded_file, load_pdf
from rag.splitter import split_documents
from rag.vector_store import create_vector_store
from rag.retriever import retrieve_documents
from rag.llm import generate_answer, generate_summary

from database.chat_service import save_chat
from database.history_service import get_user_history
from database.conversation_service import create_conversation
from session_utils import require_login, show_hero


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide"
)


# -----------------------------------
# Login Check
# -----------------------------------

require_login()


# -----------------------------------
# Header
# -----------------------------------

show_hero("Intelligent Document Q&A System")


# -----------------------------------
# Sidebar
# -----------------------------------

st.sidebar.success(
    f"👤 {st.session_state.username}"
)

# ----------------------------
# New Chat Button
# ----------------------------

if st.sidebar.button("➕ New Chat"):

    st.session_state.pop("conversation_id", None)
    st.session_state.pop("home_messages", None)

    st.rerun()

st.sidebar.divider()

# ----------------------------
# Chat History
# ----------------------------

st.sidebar.header("💬 Chat History")

history = get_user_history(
    st.session_state.user_id
)

for chat in history:

    title = chat.question

    if len(title) > 35:
        title = title[:35] + "..."

    if st.sidebar.button(
        title,
        key=chat.id
    ):
        st.session_state.home_messages = [
            {"role": "user", "content": chat.question},
            {"role": "assistant", "content": chat.answer}
        ]
        st.session_state.conversation_id = chat.conversation_id
        st.rerun()


# -----------------------------------
# Upload PDF
# -----------------------------------

uploaded_files = st.file_uploader(
    "Upload PDF Files",
    type=["pdf"],
    accept_multiple_files=True
)

documents = []
chunks = []


# -----------------------------------
# Process PDFs
# -----------------------------------

if uploaded_files:

    all_chunks = []

    for file_index, uploaded_file in enumerate(uploaded_files):

        file_path = save_uploaded_file(uploaded_file)

        documents = load_pdf(file_path)

        chunks = split_documents(documents)

        all_chunks.extend(chunks)

        # Only wipe the user's collection on the FIRST file of this
        # upload batch — subsequent files get added, not overwritten.
        vector_store, added_count = create_vector_store(
            chunks,
            user_id=st.session_state.user_id,
            reset=(file_index == 0)
        )

        if added_count == 0:
            st.warning(
                f"⚠️ No extractable text found in **{uploaded_file.name}**. "
                "It looks like a scanned/image-based PDF (no text layer), "
                "so it was skipped. Try a text-based PDF, or an OCR tool first."
            )
            st.divider()
            continue

        st.success(f"✅ {uploaded_file.name} uploaded and processed successfully!")

        # ----------------------------
        # Summary (click to expand/collapse)
        # ----------------------------

        summary_key = f"summary_{uploaded_file.name}"

        with st.expander(f"📝 Summary of {uploaded_file.name}"):

            if summary_key not in st.session_state:

                if st.button("Generate Summary", key=f"gen_summary_{file_index}"):

                    with st.spinner("Generating summary..."):

                        full_text = "\n\n".join(doc.page_content for doc in documents)

                        st.session_state[summary_key] = generate_summary(full_text)

                    st.rerun()

            if summary_key in st.session_state:
                st.write(st.session_state[summary_key])

        st.divider()


# -----------------------------------
# Chat Interface
# -----------------------------------

if uploaded_files:

    if "home_messages" not in st.session_state:
        st.session_state.home_messages = []

    if len(uploaded_files) == 1:
        chat_title = f"💬 Chat with: {uploaded_files[0].name}"
    else:
        chat_title = "💬 Chat with your documents"

    st.header(chat_title)

    # Render the running conversation as chat bubbles
    for msg in st.session_state.home_messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

            if msg.get("source"):
                st.caption(msg["source"])

    query = st.chat_input("Ask anything about your document...")

    if query:

        with st.chat_message("user"):
            st.write(query)

        st.session_state.home_messages.append({
            "role": "user",
            "content": query
        })

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                results = retrieve_documents(query, user_id=st.session_state.user_id)

                docs = [doc for doc, score in results]

                answer = generate_answer(query, docs)

                st.write(answer)

                source_line = None

                if results:
                    top_doc, top_score = min(results, key=lambda r: r[1])
                    top_page = top_doc.metadata["page"] + 1

                    other_pages = sorted(set(
                        doc.metadata["page"] + 1
                        for doc, score in results
                        if (doc.metadata["page"] + 1) != top_page
                    ))

                    if other_pages:
                        source_line = f"📄 Source: Page {top_page}  •  Related: Page(s) {', '.join(map(str, other_pages))}"
                    else:
                        source_line = f"📄 Source: Page {top_page}"

                    st.caption(source_line)

        st.session_state.home_messages.append({
            "role": "assistant",
            "content": answer,
            "source": source_line
        })

        # -----------------------------------
        # Get or Create Conversation, then save
        # -----------------------------------

        if "conversation_id" not in st.session_state:

            title = query[:50]

            st.session_state.conversation_id = create_conversation(
                st.session_state.user_id,
                title
            )

        save_chat(
            st.session_state.conversation_id,
            query,
            answer
        )