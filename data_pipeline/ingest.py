import sys
from pathlib import Path
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

class KnowledgeBase:
    def __init__(self, collection_name: str = "senior_dev_twin"):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.data_dir = self.root_dir / "my_knowledge"
        self.db_path = self.root_dir / "local_db"
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def run_sync(self):
        if not self.data_dir.exists():
            print(f"Directory not found: {self.data_dir}")
            return

        loader = DirectoryLoader(
            str(self.data_dir),
            glob="**/*.*",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        QdrantVectorStore.from_documents(
            chunks,
            self.embeddings,
            path=str(self.db_path),
            collection_name=self.collection_name,
        )
        
        print(f"Indexed {len(chunks)} chunks into {self.db_path}")

if __name__ == "__main__":
    kb = KnowledgeBase()
    kb.run_sync()