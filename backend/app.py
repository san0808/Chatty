import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.llms import OpenAI

app = FastAPI()

# Model for request body
class Query(BaseModel):
    question: str

# Initialize and load your components
def init_components():
    os.environ["OPENAI_API_KEY"] = "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"

    # Load data from URLs
    urls = [
        'https://www.reuters.com/sports/soccer/france-annihilate-10-man-gibraltar-14-0-record-win-2023-11-18/',
        'https://www.goal.com/en-us/lists/france-player-ratings-gibraltar-kylian-mbappe-hat-trick-didier-deschamps-record-historic-14-0-victory-largest-ever-european-scoreline/blta605e262b2867c93', 
        'https://www.bbc.com/sport/football/67388343'
    ]
    loaders = UnstructuredURLLoader(urls=urls)
    data = loaders.load()

    # Text Splitter
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(data)

    # Initialize embeddings and FAISS vector store
    embeddings = OpenAIEmbeddings()
    vectorStore_openAI = FAISS.from_documents(docs, embeddings)

    # Serialize the FAISS index to bytes and deserialize
    serialized_bytes = vectorStore_openAI.serialize_to_bytes()
    vectorStore_openAI = FAISS.deserialize_from_bytes(serialized=serialized_bytes, embeddings=embeddings)

    # Initialize the LLM with desired settings
    llm = OpenAI(temperature=0, model_name='text-davinci-003')
    retriever = vectorStore_openAI.as_retriever()

    # Initialize the RetrievalQAWithSourcesChain with the LLM and the retriever
    chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=retriever)
    return chain

chain = init_components()

@app.post("/ask")
async def ask(query: Query):
    try:
        response = chain({"question": query.question}, return_only_outputs=True)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



