from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize app
app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found. Check your .env file")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Request model
class ChatRequest(BaseModel):
    user_id: str
    message: str

# Health check
@app.get("/")
def home():
    return {"message": "Backend is live"}

# Chat endpoint
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ updated model
            messages=[
                {"role": "user", "content": req.message}
            ]
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}