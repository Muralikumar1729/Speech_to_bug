import whisper
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI

def load_whisper_model():
    return whisper.load_model("small")

def load_semantic_similarity_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def load_llm_model():
    API_KEY = 'AIzaSyAeY-JZQUTeI8kCgVt1Ey_'  # Replace with your actual API key
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.5,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        google_api_key=API_KEY,
    )
