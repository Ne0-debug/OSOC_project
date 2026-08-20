from fastapi import FastAPI
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

@app.get("/test")
def test():
    response = model.generate_content("In one sentence, what is the RTI Act, 2005?")
    return {"answer": response.text}