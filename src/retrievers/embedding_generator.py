from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from pathlib import Path

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  

def prepare_documents(chunks):
    docs = []
    for item in chunks:
        doc = Document(
            page_content=item["text"],
            metadata={
                k: v for k, v in item.items() if k != "text"
            }
        )
        docs.append(doc)
    return docs

def save_to_chroma(documents, persist_dir=".data/embeddings/"):
    # save to db
    vector_db = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    vector_db.add_documents(documents)
    vector_db.persist()

    return vector_db
