from sentence_transformers import SentenceTransformer
import fastapi
import qdrant_client

print(f"✅ FastAPI version: {fastapi.__version__}")

print("Loading embedding model (this may take a minute the first time)...")
# This is a small, fast model from HuggingFace
model = SentenceTransformer('all-MiniLM-L6-v2')

test_text = "I am a senior Angular developer."
vector = model.encode(test_text)

print(f"✅ Success! Generated a vector with {len(vector)} dimensions.")
print("Your MLOps environment is fully functional.")