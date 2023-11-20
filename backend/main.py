from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pytrends.request import TrendReq
import openai
import os
from langchain.llms import OpenAI
llm = OpenAI(openai_api_key="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")

app = FastAPI()

# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key ="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"

class TopicRequest(BaseModel):
    topic: str

class ChatRequest(BaseModel):
    message: str
    session_id: str
    
class ChatSession:
    def __init__(self):
        self.sessions = {}

    def get_session_context(self, session_id):
        return self.sessions.get(session_id, "")

    def update_session_context(self, session_id, user_input, bot_response):
        context = self.sessions.get(session_id, "")
        updated_context = f"{context}\nUser: {user_input}\nAI: {bot_response}"
        self.sessions[session_id] = updated_context

# Initialize Pytrends
pytrends = TrendReq(hl='en-US', tz=360)

def get_top_three_trends():
    trends = pytrends.trending_searches(pn='india').head(3)
    return trends[0].tolist()

def get_interest_data(keyword):
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='IN', gprop='')
    interest_over_time = pytrends.interest_over_time()
    interest_over_time.index = interest_over_time.index.strftime('%Y-%m-%d')  # Format the dates
    interest_by_region = pytrends.interest_by_region()
    return interest_over_time.to_dict(), interest_by_region.to_dict()


# Endpoint for fetching top 3 topics
@app.get("/get_top_topics")
async def get_top_topics():
    topics = get_top_three_trends()  
    return {"topics": topics}


# Instance of ChatSession to manage conversation contexts
chat_sessions = ChatSession()

@app.post("/chat/")
async def chat(chat_request: ChatRequest):
    try:
        # Retrieve the current context for this session
        context = chat_sessions.get_session_context(chat_request.session_id)
        
        # Craft the prompt with context, user input, and a directive for the AI
        prompt = f"{context}\nUser: {chat_request.message}\nAI:"
        
        # Add a directive for witty and engaging responses
        prompt += "\n[Respond in a witty and engaging manner, providing a thoughtful and intelligent contrary opinion.]"

        # Send the prompt to the LLM and get a response
        # response = llm.generate([prompt], {"session_id": chat_request.session_id})
        response = llm.generate([prompt])

        # Update the context with the new exchange
        chat_sessions.update_session_context(chat_request.session_id, chat_request.message, response)

        # Return the response
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

