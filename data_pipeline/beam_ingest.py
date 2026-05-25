import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from data_pipeline.ingest import KnowledgeBase
from config.settings import settings
import os

class ProcessDocument(beam.DoFn):
    def process(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE, 
                chunk_overlap=settings.CHUNK_OVERLAP
            )
            chunks = splitter.split_text(content)
            
            for chunk in chunks:
                yield chunk
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

def run_pipeline():
    options = PipelineOptions()
    kb = KnowledgeBase() 
    
    input_dir = settings.DATA_DIR
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    with beam.Pipeline(options=options) as p:
        (
            p 
            | "CreateFilePaths" >> beam.Create(files)
            | "ParallelTransform" >> beam.ParDo(ProcessDocument())
            | "BatchToVectorDB" >> beam.Map(lambda chunk: kb.sync_single_chunk(chunk))
        )
    print("Parallel Ingestion Complete.")

if __name__ == "__main__":
    run_pipeline()