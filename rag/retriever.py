from langchain_chroma import Chroma
from rag.embeddings import embeddings
from rag.vector_store import get_collection_name

DB_DIRECTORY = "chroma_db"


def retrieve_documents(query, user_id):
    """
    Search only inside the requesting user's own collection.
    """

    collection_name = get_collection_name(user_id)

    vector_store = Chroma(
        persist_directory=DB_DIRECTORY,
        embedding_function=embeddings,
        collection_name=collection_name
    )

    results = vector_store.similarity_search_with_score(
        query,
        k=5
    )

    return results