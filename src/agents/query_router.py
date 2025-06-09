import sys
import os
from src.retrievers.hybrid_retriever import get_relecant_documents
from src.models.model_selector import call_llm
from typing import List


def route_query(query: str, prompt_template: str = None, provider: str = None, model: str = None) -> str:

    documents = get_relecant_documents(query)

    context = "\n\n".join([doc.page_content for doc in documents])
    if prompt_template:
        prompt = prompt_template.format(query=query, context=context)

    else:
        prompt = f"""
        You are an expert assistant. Based on the following documents, answer the user's question.
    
        === USER QUESTION ===
        {query}
    
        === CONTEXT DOCUMENTS ===
        {context}
    
        Answer:"""
    
    answer = call_llm(prompt)

    return answer
