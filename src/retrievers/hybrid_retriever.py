from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import os
from dotenv import load_dotenv
import cohere

load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")

# NOTE: For ingestion and embedding, use ingest.py. This module is only for retrieval and reranking.

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
co = cohere.Client(cohere_api_key)

def load_vector_db(persist_dir="./data/embeddings/"):
    """
    Load the vector database using the Cohere API key.
    """
    if not cohere_api_key:
        raise ValueError("Cohere API key not provided.")
    
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )

def rerank_with_cohere(query, documents, top_n=5):
    """
    Rerank documents using the Cohere API.
    
    query: Query text
    documents: List of documents (Document objects)
    top_n: Return top N documents
    """
    if not cohere_api_key:
        raise ValueError("Cohere API key not provided.")
    
    # Extract the text from the documents
    texts = [doc.page_content for doc in documents]
    
    # Rerank using Cohere
    response = co.rerank(
        model="rerank-english-v2.0",
        query=query,
        documents=texts,
        top_n=top_n
    )
    
    # Convert the results back to Document objects
    reranked_docs = []
    for idx in response.reranked_documents:
        reranked_docs.append(documents[idx.index])

    return reranked_docs

def keyword_fallback(query, db, k=3):
    """
    Fallback to keyword search if embedding result is empty.
    """
    results = []
    for collection in db._collection.get()["documents"]:
        for i, doc in enumerate(collection):
            if query.lower() in doc.lower():  # Case-insensitive match
                results.append(Document(page_content=doc))
                if len(results) >= k:
                    return results
    return results


def get_relecant_documents(query, k=10, filters=None, rerank=True):
    """
    Retrieve relevant documents based on the given query.
    
    query: Query text
    k: Number of documents to return
    filters: Optional filters (e.g., date, type, etc.)
    rerank: Whether to rerank the documents
    """
    vector_db = load_vector_db()
    
    # Retrieve documents
    retriever = vector_db.as_retriever(search_kwargs={
        "k": k,
        "filters": filters or {}
        }
    )

    results = retriever.get_relevant_documents(query)

    if not results:
        results = keyword_fallback(query, vector_db, k=3)


    if rerank and results:
        results = rerank_with_cohere(query, results, top_n=5)

    return results