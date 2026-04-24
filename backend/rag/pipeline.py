from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_groq import ChatGroq
import os
import logging
import time

class RAGPipeline:
    def __init__(self, persist_directory="data/embeddings"):
        self.persist_directory = persist_directory
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def retrieve(self, query, k=3):
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return docs
        except Exception as e:
            logging.error(f"Retrieval error: {e}")
            return []

    def generate(self, query, k=3, timeout=20, live_data=None):
        docs = self.retrieve(query, k)
        if not docs:
            context = "No relevant documents found in knowledge base."
        else:
            context = "\n".join([doc.page_content for doc in docs])
        
        # Build the prompt with Live Data context if available
        live_context = ""
        if live_data:
            live_context = f"\n--- LIVE DATA ---\n{live_data}\n------------------\n"

        prompt = f"""
You are a Precision Farming Assistant. Use the provided Knowledge Base and Live Data to answer the farmer's question.

KNOWLEDGE BASE:
{context}
{live_context}
QUESTION: {query}

Provide a practical, data-driven answer. If live data is available, relate it to the knowledge base guidelines.
ANSWER:"""
        try:
            start = time.time()
            response = self.llm.invoke(prompt)
            elapsed = time.time() - start
            if elapsed > timeout:
                raise TimeoutError("LLM call timed out.")
            return {"response": response.content, "context": context}
        except Exception as e:
            logging.error(f"LLM error: {e}")
            return {"response": f"Error generating answer: {e}", "context": context}
