import os
from langchain_google_genai import ChatGoogleGenerativeAI

if __name__ == "__main__":
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not found in environment.")
        exit(1)
    llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-pro")
    prompt = "What is the capital of France?"
    try:
        response = llm.invoke(prompt)
        print("LLM response:", response)
    except Exception as e:
        print("Error calling Gemini API:", e)
