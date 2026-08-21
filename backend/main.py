from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

load_dotenv()

app = FastAPI()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

# --- Load all chunk files at startup ---
CHUNKS_DIR = Path(__file__).parent / "docs_temp" / "chunks"

def load_chunks():
    chunks = []
    for file_path in CHUNKS_DIR.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")
        first_line = text.splitlines()[0]
        topic = first_line.replace("# Topic:", "").strip()
        chunks.append({
            "filename": file_path.name,
            "topic": topic,
            "text": text
        })
    return chunks

CHUNKS = load_chunks()

@app.get("/test")
def test():
    response = model.generate_content("In one sentence, what is the RTI Act, 2005?")
    return {"answer": response.text}

STOPWORDS = {"the", "is", "of", "a", "an", "to", "in", "for", "and", "or", "what", "how", "do", "does", "i", "my", "can", "you", "me", "on", "at", "with"}

def score_chunk(query: str, chunk: dict) -> int:
    query_words = set(re.findall(r"\w+", query.lower())) - STOPWORDS
    chunk_words = set(re.findall(r"\w+", (chunk["topic"] + " " + chunk["text"]).lower())) - STOPWORDS
    return len(query_words & chunk_words)

def select_relevant_chunks(query: str, top_n: int = 3):
    scored = [(score_chunk(query, chunk), chunk) for chunk in CHUNKS]
    scored.sort(key=lambda x: x[0], reverse=True)
    relevant = [chunk for score, chunk in scored if score >= 2]
    return relevant[:top_n]

class AskRequest(BaseModel):
    query: str

@app.post("/ask")
def ask(request: AskRequest):
    relevant_chunks = select_relevant_chunks(request.query)

    if not relevant_chunks:
        return {"answer": "I don't have information on this in my current sources.", "sources": []}

    context = "\n\n".join(
        f"[Source: {c['filename']}]\n{c['text']}" for c in relevant_chunks
    )

    prompt = f"""You are a helpful legal assistant. Answer the user's question using ONLY the context below. 
Cite which source file(s) you used at the end of your answer, like "(Source: filename.md)".
If the context does not contain the answer, say "I don't have information on this" — do not guess.

Context:
{context}

Question: {request.query}

Answer:"""

    response = model.generate_content(prompt)
    return {
        "answer": response.text,
        "sources": [c["filename"] for c in relevant_chunks]
    }