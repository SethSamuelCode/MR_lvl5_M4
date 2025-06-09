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

# Define models for managing chat sessions with Gemini AI
class ChatSession:
    def __init__(self):
        # Track last interaction time for potential session cleanup
        self.lastContact :float = time.time()
        
        # Initialize a new chat session with Gemini AI
        self._session = client.aio.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=[
                    # Set up the AI assistant's personality and role
                    types.Part.from_text(text=SYSTEM_PROMPT),
                ],
            )
        )

# Dictionary to store active chat sessions, keyed by UUID
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
    # Create new chat session if one doesn't exist for this UUID
    if userin.uuid not in chatSessions:
        chatSessions[userin.uuid] = ChatSession()

    # Send message to Gemini AI and return its response
    resp = await chatSessions[userin.uuid]._session.send_message(userin.message)
    return resp.candidates[0].content.parts[0].text

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the incoming WebSocket connection
    await websocket.accept()
    
    # Generate a unique identifier for this connection
    userUUID: str = str(uuid7())
    
    # Create a new chat session for this connection
    chatSessions[userUUID]= ChatSession()
    
    # Send initial AI response to trigger Tina's introduction
    # Empty string triggers the system prompt
    aiResp = await chatSessions[userUUID]._session.send_message(" ")
    await websocket.send_json({"message": aiResp.candidates[0].content.parts[0].text})
    
    try:
        # Main communication loop
        while True:
            # Receive text message from the client
            data = await websocket.receive_text()
            print(data)  # Log received message
            
            # Send user's message to Gemini AI and get response
            aiResp = await chatSessions[userUUID]._session.send_message(data)
            
            # Send AI's response back to the client
            await websocket.send_json({"message": aiResp.candidates[0].content.parts[0].text})
            
    except WebSocketDisconnect:
        # Handle client disconnection
        print(userUUID+": Disconnected ")
        # Clean up by removing the chat session
        del chatSessions[userUUID]
