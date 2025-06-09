# ------------------ SETUP AND INSTALL ----------------- #

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel 
from dotenv import load_dotenv 
import os
from google import genai
from google.genai import types
from uuid_extensions import uuid7
from dataclasses import dataclass
from typing import Final
import time
import json

# Load environment variables and set up Gemini API client
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key = API_KEY)

# Initialize FastAPI application
app = FastAPI()

# --------------------- MIDDLEWARES -------------------- #


# Configure CORS (Cross-Origin Resource Sharing) settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------- DEFINES ---------------------- #

MODEL_NAME:Final = "gemini-2.5-flash-preview-05-20"
SYSTEM_PROMPT:Final = """Your name is Tina, a bubbly friendly helper trying to find the user the best insurance policy that suits their needs. There are 3 different insurance policies. Mechanical breakdown insurance, comprehensive cover and third party. Mechanical business insurance is not available for trucks and racing cars and comprehensive car insurance is not available to cars older than 10 years old. You will start the conversation by saying: “Hi my name is Tina. Would you like me to help you find the insurance policy that suits your needs ? “. If the user responds positively you can help them. If they respond negatively then thank them for their time and let them know you are always there for help. You will not offer the 3 insurance policies up front you will ask the user questions to determine what is the best policy for them. 
You can ask as many questions as you wish to determine the insurance type that will suit them best but keep them updated as to how close you are to deciding the best type of policy. Please also explain the pros and cons of each policy type when you provide the recommendation. """

# Define data models for request validation
class UserData(BaseModel):
    hello: str

# Define message model for chat requests
class Message(BaseModel):
    uuid: str
    message: str

class ChatSession:
    def __init__(self):
        self.lastContact :float = time.time()
        self._session = client.aio.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=[
                    types.Part.from_text(text=SYSTEM_PROMPT),
                ],
            )
        )

chatSessions:dict = {}
# ---------------------- ENDPOINTS --------------------- #

# Basic endpoint to test if server is running
@app.get("/")
def read_root():
    return "hello world"

# Test endpoint for POST requests
@app.post("/postTest")
def sendback(userin: UserData):
    return userin

# Endpoint to generate UUID using uuid7
@app.get("/api/uuid")
def sendUUID():
    return {"uuid": uuid7()}


# Chat endpoint that integrates with Gemini AI
@app.post("/api/chat")
async def chat(userin: Message) -> str:

    if userin.uuid not in chatSessions:
        chatSessions[userin.uuid] = ChatSession()

    resp = await chatSessions[userin.uuid]._session.send_message(userin.message)
    return resp.candidates[0].content.parts[0].text

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # await websocket.send_text(str(uuid7()))
    userUUID: str = str(uuid7())
    await websocket.send_json({"uuid": userUUID })
    chatSessions[userUUID]= ChatSession()
    aiResp = await chatSessions[userUUID]._session.send_message(" ")
    await websocket.send_json({"message": aiResp.candidates[0].content.parts[0].text})
    try:
        while True:
            data = await websocket.receive_json()
            # userinput = json.loads(data)
            print(data)
            aiResp = await chatSessions[userUUID]._session.send_message(data["message"])
            await websocket.send_json({"message": aiResp.candidates[0].content.parts[0].text})
    except WebSocketDisconnect:
        print(userUUID+": Disconnected ")
        