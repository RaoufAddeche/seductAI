from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    llm = ChatGroq(api_key=os.getenv("GROQ_APIKEY"), model="llama-3.3-70b-versatile")
    return llm