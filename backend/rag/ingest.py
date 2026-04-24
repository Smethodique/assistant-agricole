from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.document_loaders import TextLoader
import os
import glob

DOCS_DIR = "data/agriculture_docs"
PERSIST_DIR = "data/embeddings"

if __name__ == "__main__":
    filepaths = glob.glob(os.path.join(DOCS_DIR, "*.txt"))
    docs = []
    for path in filepaths:
        loader = TextLoader(path)
        docs.extend(loader.load())
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(docs, embeddings, persist_directory=PERSIST_DIR)
    db.persist()
    print(f"Ingested {len(docs)} documents into ChromaDB.")
