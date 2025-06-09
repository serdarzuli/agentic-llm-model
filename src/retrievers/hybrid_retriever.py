from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import os
from dotenv import load_dotenv
import cohere

load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")  # OpenAI Embeddings model

co = cohere.Client(cohere_api_key)  # Coh

def load_vector_db(persist_dir="./data/embeddings/"):
    """
    Cohere API anahtarını kullanarak vektör veritabanını yükler.
    """
    if not cohere_api_key:
        raise ValueError("Cohere API anahtarı sağlanmadı.")
    
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )

def rerank_with_cohere(query, documents, top_n=5):
    """
    Cohere API kullanarak belgeleri yeniden sıralar.
    
    query: Sorgu metni
    documents: Belgeler listesi (Document nesneleri)
    top_n: En iyi N belgeyi döndür
    """
    if not cohere_api_key:
        raise ValueError("Cohere API anahtarı sağlanmadı.")
    
    # Belgelerin metinlerini al
    texts = [doc.page_content for doc in documents]
    
    # Cohere ile yeniden sıralama yap
    response = co.rerank(
        model="rerank-english-v2.0",
        query=query,
        documents=texts,
        top_n=top_n
    )
    
    # Sonuçları Document nesnelerine dönüştür
    reranked_docs = []
    for idx in response.reranked_documents:
        reranked_docs.append(documents[idx.index])  #indexe gore siralama yap

    return reranked_docs

def keyword_fallback(query, db, k=3):
    """
    Embedding sonucu boş dönerse, keyword arama fallback'i.
    """
    results = []
    for collection in db._collection.get()["documents"]:
        for i, doc in enumerate(collection):
            if query.lower() in doc.lower():  # Case-insensitive eşleşme
                results.append(Document(page_content=doc))
                if len(results) >= k:
                    return results
    return results


def get_relecant_documents(query, k=10, filters=None, rerank=True):
    """
    Verilen sorguya göre ilgili belgeleri döndürür.
    
    query: Sorgu metni
    k: Döndürülecek belge sayısı
    filters: Opsiyonel filtreler (örneğin tarih, tür vs.)
    rerank: Yeniden sıralama yapılıp yapılmayacağı
    """
    vector_db = load_vector_db()
    
    # Belgeleri al
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