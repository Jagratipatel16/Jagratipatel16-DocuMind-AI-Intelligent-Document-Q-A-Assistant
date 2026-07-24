import streamlit as st

from rag.loader import save_uploaded_file, load_pdf
from rag.splitter import split_documents
from rag.vector_store import create_vector_store
from rag.retriever import retrieve_documents
from rag.llm import generate_answer

from database.chat_service import save_chat
from database.history_service import get_user_history
from database.conversation_service import create_conversation


# -----------------------------------
# Login Check
# -----------------------------------

if "logged_in" not in st.session_state:

    st.warning("🔐 Please Login First")
    st.stop()


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide"
)


# -----------------------------------
# Header
# -----------------------------------

st.title("📄 DocuMind AI")
st.subheader("Intelligent Document Q&A System")


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

    st.session_state.pop("selected_question", None)
    st.session_state.pop("selected_answer", None)
    st.session_state.pop("conversation_id", None)

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
        st.session_state.selected_question = chat.question
        st.session_state.selected_answer = chat.answer


# Logout

st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):

    st.session_state.clear()
    st.switch_page("pages/Login.py")


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
        create_vector_store(
            chunks,
            user_id=st.session_state.user_id,
            reset=(file_index == 0)
        )

        st.success("✅ Embeddings generated successfully!")
        st.success("✅ Stored in ChromaDB")
        st.success(f"✅ {uploaded_file.name} uploaded successfully!")

        st.divider()

        # ----------------------------
        # File Information
        # ----------------------------

        st.header("📄 File Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "File Name",
                uploaded_file.name
            )

        with col2:
            st.metric(
                "Total Pages",
                len(documents)
            )

        st.divider()

        # ----------------------------
        # Metadata
        # ----------------------------

        st.header("📑 PDF Metadata")

        with st.expander("View Metadata"):
            st.json(documents[0].metadata)

        st.divider()

        # ----------------------------
        # Chunks
        # ----------------------------

        st.header("✂️ Chunk Information")

        st.metric(
            "Total Chunks",
            len(chunks)
        )

        st.divider()

        st.header("📚 Chunk Preview")

        for i, chunk in enumerate(chunks[:5]):

            st.subheader(f"Chunk {i+1}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"**Page Number:** {chunk.metadata['page'] + 1}"
                )

            with col2:
                st.write(
                    f"**Characters:** {len(chunk.page_content)}"
                )

            st.write(chunk.page_content)

            with st.expander("View Chunk Metadata"):
                st.json(chunk.metadata)

            st.divider()


# -----------------------------------
# Previous Chat
# -----------------------------------

if "selected_answer" in st.session_state:

    st.header("💬 Previous Chat")

    st.write("### Question")

    st.info(
        st.session_state.selected_question
    )

    st.write("### Answer")

    st.success(
        st.session_state.selected_answer
    )

    st.divider()


# -----------------------------------
# Ask Questions
# -----------------------------------

if uploaded_files:

    st.header("💬 Ask Questions")

    query = st.text_input(
        "Ask something about the uploaded PDF"
    )

    if query:

        results = retrieve_documents(query, user_id=st.session_state.user_id)

        docs = []

        for doc, score in results:
            docs.append(doc)

        answer = generate_answer(
            query,
            docs
        )

        # -----------------------------------
        # Get or Create Conversation
        # -----------------------------------

        if "conversation_id" not in st.session_state:

            title = query[:50]

            st.session_state.conversation_id = create_conversation(
                st.session_state.user_id,
                title
            )

        # Save Chat

        save_chat(
            st.session_state.conversation_id,
            query,
            answer
        )

        st.success(
            f"Found {len(results)} relevant chunks"
        )

        # ----------------------------
        # AI Answer
        # ----------------------------

        st.header("🤖 AI Answer")

        st.write(answer)

        st.divider()

        # ----------------------------
        # Sources
        # ----------------------------

        st.header("📚 Sources")

        for i, (doc, score) in enumerate(results):

            st.subheader(f"Source {i+1}")

            st.write(
                f"**Page:** {doc.metadata['page'] + 1}"
            )

            st.caption(
                f"Distance Score: {score:.4f}"
            )

            st.write(doc.page_content)

            with st.expander("View Metadata"):
                st.json(doc.metadata)

            st.divider()