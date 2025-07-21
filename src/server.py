from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response
from src.reader import read_epub

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]  
)

@app.get("/books")
async def main(name: str):
    data = read_epub(name)
    return {"good_read": data}