from pymupdf4llm import PyMuPDFLoader
from pathlib import Path


def load_pdf_with_metada(pdf_path):
    loader = PyMuPDFLoader(pdf_path)
    return loader.load()

def load_all_pdfs_from_folder(folder_path):
    all_docs = []
    folder = Path(folder_path)
    for pdf_file in folder.glob("*.pdf"):
        docs = load_pdf_with_metada(pdf_file)
        all_docs.extend(docs)
    return all_docs

