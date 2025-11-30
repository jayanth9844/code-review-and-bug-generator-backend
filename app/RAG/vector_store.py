"""
Vector Store module for RAG system.
Handles initialization of Chroma vector store and code indexing.
"""

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document
import os


def initialize_vector_store_and_embeddings():
    """
    Initializes a Chroma vector store and a SentenceTransformer embedding model.

    Returns:
        tuple: A tuple containing the embedding model and the Chroma vector store.
    """
    # Create an instance of SentenceTransformerEmbeddings
    # Using 'all-MiniLM-L6-v2' as the model name as specified.
    embedding_model = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')

    # Create an in-memory instance of Chroma using the embedding model
    vector_store = Chroma(embedding_function=embedding_model)

    return embedding_model, vector_store


def load_and_index_code(code_input, embedding_model, vector_store):
    """
    Loads code from a directory or a list of snippets, splits them into chunks,
    embeds them, and adds them to the Chroma vector store.

    Args:
        code_input (str or list): A directory path (string) or a list of code snippets (list of strings).
        embedding_model: The SentenceTransformerEmbeddings model.
        vector_store: The Chroma vector store instance.

    Returns:
        str: A confirmation message indicating success.
        
    Raises:
        ValueError: If code_input is neither a directory path nor a list.
    """
    documents = []

    if isinstance(code_input, str) and os.path.isdir(code_input):
        # Load from directory if code_input is a directory path
        loader = DirectoryLoader(code_input, glob="**/*.py")
        loaded_docs = loader.load()
        for doc in loaded_docs:
            documents.append(Document(page_content=doc.page_content, metadata=doc.metadata))
    elif isinstance(code_input, list):
        # Create documents from a list of code snippets
        for snippet in code_input:
            documents.append(Document(page_content=snippet))
    else:
        raise ValueError("code_input must be a directory path (string) or a list of code snippets (list).")

    # Initialize RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Split documents into chunks
    code_chunks = text_splitter.split_documents(documents)

    # Add code chunks to the vector store
    vector_store.add_documents(code_chunks)

    return "Code loaded, chunked, embedded, and added to the vector store successfully."
