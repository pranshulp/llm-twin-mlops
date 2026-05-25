from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from config.settings import settings

class KnowledgeBase:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

    def sync_single_chunk(self, text_content: str):
        """Helper for parallel workers to push a single chunk to Qdrant."""
        doc = Document(page_content=text_content)
        QdrantVectorStore.from_documents(
            [doc],
            self.embeddings,
            path=str(settings.DB_PATH),
            collection_name=settings.COLLECTION_NAME,
        )

    def run_sync(self):
        """Standard batch ingestion (non-parallel)."""
        loader = DirectoryLoader(
            str(settings.DATA_DIR),
            glob="**/*.*",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        
        docs = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE, 
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        chunks = splitter.split_documents(docs)

        QdrantVectorStore.from_documents(
            chunks,
            self.embeddings,
            path=str(settings.DB_PATH),
            collection_name=settings.COLLECTION_NAME,
        )
        print(f"Batch index updated: {len(chunks)} chunks.")