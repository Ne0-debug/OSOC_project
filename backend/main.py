from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

# Load source context at startup
SOURCE_PATH = Path(__file__).parent / "docs_temp" / "dummy_source.txt"
with open(SOURCE_PATH, "r", encoding="utf-8") as f:
    SOURCE_CONTEXT = f.read()

@app.get("/test")
def test():
    response = model.generate_content("In one sentence, what is the RTI Act, 2005?")
    return {"answer": response.text}

class AskRequest(BaseModel):
    query: str

@app.post("/ask")
def ask(request: AskRequest):
    prompt = f"""You are a helpful legal assistant. Answer the user's question using ONLY the context below. If the answer isn't in the context, say you don't have that information.

Context:
{SOURCE_CONTEXT}

Question: {request.query}

Answer:"""

    response = model.generate_content(prompt)
    return {"answer": response.text}