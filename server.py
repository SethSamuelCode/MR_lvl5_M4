from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel 
from dotenv import load_dotenv 
import os
from google import genai
from google.genai import types
from uuid_extensions import uuid7

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = API_KEY)

app = FastAPI()

corsOrigins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=corsOrigins,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserData(BaseModel):
    hello: str

@app.get("/")
def read_root():
    return "hello world"

@app.post("/postTest")
def sendback(userin: UserData):
    return userin

@app.get("/api/uuid")
def sendUUID():
    return {"uuid": uuid7()}

class Message(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(userin: Message):
    chat = client.aio.chats.create(model='gemini-2.0-flash')
    resp = await chat.send_message(userin.message)
    return resp.candidates[0].content.parts[0].text