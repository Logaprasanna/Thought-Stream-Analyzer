from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_database, get_entries, new_entry

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware,
    allow_methods = ['*'],
    allow_headers = ['*'],
    allow_credentials = True,
    allow_origins = ['*']
    )

class EntryCreate(BaseModel):
    content: str 
    category: str = "journal"

@app.get("/api/entries")
async def getting_entries():
    entries = get_entries()
    return {
        "entries":entries
        }

@app.post("/api/entries")
async def post_new_entry(entry: EntryCreate):
    key_id = new_entry(entry.content, entry.category)
    return {"message":"Your entry is saved", "key" :key_id}

@app.get("/")
async def root():
    return{"message": "The server is up and running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

