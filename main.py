from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# OpenAI Agent SDK
from agents import (
    Agent,
    AsyncOpenAI,
    Runner,
    OpenAIChatCompletionsModel,
    RunConfig
)

load_dotenv()

# ------------------------------
#  SETUP: Gemini Client + Model
# ------------------------------
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash"
)

run_config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True,
)

# -------------------------------------------------------
#  AGENT (your personalized instructions for portfolio)
# -------------------------------------------------------
agent = Agent(
    name="Codizzz Assistant",
    instructions="""
You are a highly skilled AI assistant built by a full-stack developer named Umer Ali (Codizzz).
You help users with Next.js, TypeScript, React.js, Tailwind CSS, Python, AI, Machine Learning,
Web Development, Problem-Solving, Debugging Code, and concepts related to the OpenAI Agent SDK.

Always explain answers clearly, simply, and in a friendly tone.
If a user asks for code, provide clean and optimized code.
If a user asks about AI or backend topics, give practical, real-world explanations.

Your purpose is to act like a helpful coding buddy for learners and developers.
    """,
    model=model
)

# -------------
#  FASTAPI APP
# -------------
app = FastAPI()

# CORS (Frontend <-> Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Codizzz AI Assistant Backend is running!"}

# Request Schema
class ChatMessage(BaseModel):
    message: str

# Chat Endpoint
@app.post("/chat")
async def chat(req: ChatMessage):
    result = await Runner.run(
        agent,
        req.message,
        run_config=run_config
    )
    return {"response": result.final_output}
