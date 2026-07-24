import os
from langchain_community.document_loaders import PyPDFLoader

UPLOAD_FOLDER = "data/uploads"


def save_uploaded_file(uploaded_file):
    """
    Save uploaded PDF to data/uploads
    """

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def load_pdf(file_path):
    """
    Read PDF using PyPDFLoader
    """

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    return documents