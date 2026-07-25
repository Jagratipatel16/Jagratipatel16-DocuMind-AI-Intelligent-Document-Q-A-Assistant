import streamlit as st

from rag.loader import save_uploaded_file, load_pdf
from rag.splitter import split_documents
from rag.vector_store import create_vector_store
from rag.retriever import retrieve_documents
from rag.llm import generate_answer

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

        with st.expander("🔧 Advanced: File Processing Details"):

            # ----------------------------
            # File Information
            # ----------------------------

            st.subheader("📄 File Information")

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

            # ----------------------------
            # Metadata
            # ----------------------------

            st.subheader("📑 PDF Metadata")
            st.json(documents[0].metadata)

            # ----------------------------
            # Chunks
            # ----------------------------

            st.subheader("✂️ Chunk Information")

            st.metric(
                "Total Chunks",
                len(chunks)
            )

            st.caption(f"Showing first 5 of {len(chunks)} chunks")

            for i, chunk in enumerate(chunks[:5]):

                st.markdown(f"**Chunk {i+1}** — Page {chunk.metadata['page'] + 1}, {len(chunk.page_content)} characters")
                st.text(chunk.page_content[:300] + ("..." if len(chunk.page_content) > 300 else ""))

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

        # ----------------------------
        # AI Answer
        # ----------------------------

        st.header("🤖 AI Answer")

        st.write(answer)

        # Show the page(s) the answer most likely came from
        if results:
            top_doc, top_score = min(results, key=lambda r: r[1])
            top_page = top_doc.metadata["page"] + 1

            other_pages = sorted(set(
                doc.metadata["page"] + 1
                for doc, score in results
                if (doc.metadata["page"] + 1) != top_page
            ))

            if other_pages:
                st.caption(
                    f"📄 Source: Page {top_page}  •  Related: Page(s) {', '.join(map(str, other_pages))}"
                )
            else:
                st.caption(f"📄 Source: Page {top_page}")

        st.divider()

        # ----------------------------
        # Sources (optional, collapsed)
        # ----------------------------

        with st.expander(f"📚 View {len(results)} source(s) from your document"):

            for i, (doc, score) in enumerate(results):

                st.markdown(f"**Source {i+1} — Page {doc.metadata['page'] + 1}**")

                excerpt = doc.page_content[:250]
                st.caption(excerpt + ("..." if len(doc.page_content) > 250 else ""))

                st.divider()