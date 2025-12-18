from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# -------- Email Service ----------
from email_service import send_contact_email

# -------- Agent SDK Imports -------
from agents import (
    Agent,
    AsyncOpenAI,
    Runner,
    OpenAIChatCompletionsModel,
    RunConfig,
    SQLiteSession,
    ModelSettings,
    function_tool
)

load_dotenv()

# =========================================================
#                  FastAPI App Setup
# =========================================================
app = FastAPI(title="Portfolio Full Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
#                GEMINI CLIENT + MODEL
# =========================================================
client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

model = OpenAIChatCompletionsModel(
    model="openai/gpt-oss-120b",  # Ya llama3-groq-70b-tool-use
    openai_client=client
)


run_config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True,
)


# =========================================================
#                  Portfolio Tool
# =========================================================
@function_tool
async def get_portfolio_info():
    info = """
    Umer Ali is a full-stack developer specializing in Next.js, TypeScript, React.js,
    Tailwind CSS, Python, AI and Web Development.
    He has expertise in problem-solving, debugging code, and concepts related to Agent SDK.
    """
    return info


# =========================================================
#                       AGENT
# =========================================================
agent = Agent(
    name="Portfolio Assistant",
    instructions="""
You are Umer Ali's AI portfolio assistant.

# Responsibilities
- Answer portfolio questions
- Help with coding and debugging
- Assist with Agent SDK topics
- Provide clean working code

Always call get_portfolio_info() when asked about Umer.
    """,
    model=model,
    model_settings=ModelSettings(
        max_tokens=170,
        temperature=0.3,
    ),
    tools=[get_portfolio_info],
)

session = SQLiteSession("chat_history.db")

# =========================================================
#                     ROUTES
# =========================================================

@app.get("/")
def home():
    return {"message": "Merged Portfolio Backend is running!"}


# ----------------------------
#     CHATBOT ROUTE
# ----------------------------
class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatMessage):
    result = await Runner.run(
        agent,
        req.message,
        run_config=run_config,
        session=session,
    )
    return {"response": result.final_output}



# ----------------------------
#     CONTACT FORM ROUTE
# ----------------------------
class ContactFormData(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str
    subject: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=2000)

@app.post("/contact")
async def contact_form(form_data: ContactFormData):
    try:
        success = await send_contact_email(
            sender_name=form_data.name,
            sender_email=form_data.email,
            subject=form_data.subject,
            message=form_data.message
        )

        if success:
            return {"success": True, "message": "Your message has been sent!"}
        else:
            raise HTTPException(500, "Failed to send email.")

    except Exception as e:
        print("Contact Error:", e)
        raise HTTPException(500, "Internal Server Error")



# =========================================================
#               LOCAL DEV SERVER (optional)
# =========================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

