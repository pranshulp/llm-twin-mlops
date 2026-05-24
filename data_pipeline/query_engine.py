from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

class TwinQueryEngine:
    def __init__(self, collection_name: str = "senior_dev_twin"):
        root_dir = Path(__file__).resolve().parent.parent
        self.db_path = root_dir / "local_db"
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        client = QdrantClient(path=str(self.db_path))
        self.vector_db = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=self.embedding_model,
        )

    def query(self, question: str, k: int = 3):
        return self.vector_db.similarity_search(question, k=k)

if __name__ == "__main__":
    engine = TwinQueryEngine()
    
    user_query = "How do I handle authentication in Angular?"
    context_chunks = engine.query(user_query)
    
    print(f"\n--- Results for: {user_query} ---")
    for i, doc in enumerate(context_chunks):
        source_file = Path(doc.metadata.get('source', 'unknown')).name
        print(f"\n[Chunk {i+1} from {source_file}]:")
        print(doc.page_content[:200] + "...")