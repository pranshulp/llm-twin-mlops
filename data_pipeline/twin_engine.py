from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from data_pipeline.query_engine import TwinQueryEngine

class LLMTwin:
    def __init__(self):
        self.query_engine = TwinQueryEngine()
        
        self.llm = ChatOllama(
            model="phi3",
            temperature=0,
        )
        
        self.system_identity = (
            "You are a Senior Angular Developer's AI Twin. "
            "Use the provided context to answer the user's technical questions. "
            "Maintain a professional, senior-level tone. If the information isn't "
            "in the context, leverage your internal expertise while staying in character."
            "\n\n"
            "Context:\n{context}"
        )

    def ask(self, question: str):
        docs = self.query_engine.query(question)
        context_text = "\n".join([doc.page_content for doc in docs])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_identity),
            ("human", "{question}")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({"context": context_text, "question": question})
            return response.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

if __name__ == "__main__":
    twin = LLMTwin()
    response = twin.ask("How should we handle Angular interceptors for auth?")
    print(f"\n--- Twin's Perspective (Local Model) ---\n{response}")