from langchain_chroma import Chroma
from rag.embeddings import embeddings

DB_DIRECTORY = "chroma_db"


def get_collection_name(user_id):
    """
    Each user gets their own isolated ChromaDB collection,
    so one user's documents never leak into another user's answers.
    """
    return f"documind_user_{user_id}"


def create_vector_store(chunks, user_id, reset=True):
    """
    Store chunks in the collection belonging to `user_id`.

    reset=True  -> wipes this user's previous collection first
                   (use for the FIRST file in a fresh upload batch)
    reset=False -> adds to the existing collection
                   (use for additional files in the same batch/session)
    """

    collection_name = get_collection_name(user_id)

    if reset:
        try:
            old_db = Chroma(
                persist_directory=DB_DIRECTORY,
                embedding_function=embeddings,
                collection_name=collection_name
            )

            old_db.delete_collection()

        except Exception:
            pass

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=DB_DIRECTORY,
            collection_name=collection_name
        )

    else:
        vector_store = Chroma(
            persist_directory=DB_DIRECTORY,
            embedding_function=embeddings,
            collection_name=collection_name
        )

        vector_store.add_documents(chunks)

    print("Total Documents:", vector_store._collection.count())

    return vector_store