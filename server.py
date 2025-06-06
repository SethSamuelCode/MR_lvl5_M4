from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 

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


@app.get("/")
def read_root():
    return "hello world"

@app.post("/postTest")
def sendback():
    