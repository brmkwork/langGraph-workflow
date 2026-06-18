from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.6)
validation_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")