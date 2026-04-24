from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
import os

class Retriever:
    def __init__(self, persist_directory="data/embeddings"):
        self.persist_directory = persist_directory
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def similarity_search(self, query, k=3):
        return self.vectorstore.similarity_search(query, k=k)

