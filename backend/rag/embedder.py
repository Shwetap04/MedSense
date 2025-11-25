import google.generativeai as genai
import os

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GENAI_API_KEY"))

def embed_text(text: str):
    """
    Generate embeddings using Gemini's text-embedding-004 model.
    """
    try:
        result = genai.embed_content(
            model="text-embedding-004",
            content=text
        )
        return result["embedding"]
    except Exception as e:
        print("Embedding error:", e)
        return [0.0] * 768
