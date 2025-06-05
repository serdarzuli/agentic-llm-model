import sys
import os
from src.retrievers.hybrid_retriever import get_relecant_documents
from src.models.model_selector import call_llm
from typing import List

def route_query(query: str, prompt_template: str = None) -> str:
    """
    Verilen sorguyu uygun bir modele yönlendirir ve sonuçları döndürür.
    
    query: Sorgu metni
    """
    # İlgili belgeleri al
    documents = get_relecant_documents(query)

    context = "\n\n".join([doc.page_content for doc in documents])

    prompt = f"""
    You are an expert assistant. Based on the following documents, answer the user's question.

    === USER QUESTION ===
    {query}

    === CONTEXT DOCUMENTS ===
    {context}

    Answer:"""

    answer = call_llm(prompt)

    return answer
