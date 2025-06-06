from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel 
from dotenv import load_dotenv 
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

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

