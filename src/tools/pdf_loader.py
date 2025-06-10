from langchain_community.document_loaders import PyMuPDFLoader
from pathlib import Path
import fitz  # PyMuPDF


def load_pdf_with_metada(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def load_all_pdfs_from_folder(folder_path):
    all_docs = []
    folder = Path(folder_path)
    for pdf_file in folder.glob("*.pdf"):
        docs = load_pdf_with_metada(pdf_file)
        all_docs.extend(docs)
    return all_docs

