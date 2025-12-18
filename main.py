from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from mangum import Mangum
import os
import sys
import traceback

# -------- Email Service ----------
from email_service import send_contact_email

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
#            Lazy Agent Initialization
# =========================================================
_agent = None
_session = None
_run_config = None

def get_agent():
    """Lazy initialization of agent to prevent startup crashes"""
    global _agent, _session, _run_config

    if _agent is not None:
        return _agent, _session, _run_config

    try:
        # Import here to prevent module-level import errors
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

        # Check for required environment variable
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")

        # Initialize client
        client = AsyncOpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )

        # Initialize model
        model = OpenAIChatCompletionsModel(
            model="openai/gpt-oss-120b",
            openai_client=client
        )

        # Create run config
        _run_config = RunConfig(
            model=model,
            model_provider=client,
            tracing_disabled=True,
        )

        # Define portfolio tool
        @function_tool
        async def get_portfolio_info():
            info = """
            Umer Ali is a full-stack developer specializing in Next.js, TypeScript, React.js,
            Tailwind CSS, Python, AI and Web Development.
            He has expertise in problem-solving, debugging code, and concepts related to Agent SDK.
            """
            return info

        # Create agent
        _agent = Agent(
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

        # Create session with /tmp path for Vercel compatibility
        _session = SQLiteSession("/tmp/chat_history.db")

        return _agent, _session, _run_config

    except Exception as e:
        print(f"Error initializing agent: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        raise HTTPException(
            status_code=500,
            detail=f"Agent initialization failed: {str(e)}"
        )

# =========================================================
#                     ROUTES
# =========================================================

@app.get("/")
def home():
    return {"message": "Merged Portfolio Backend is running!"}


@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "groq_api_key_set": bool(os.getenv("GROQ_API_KEY")),
        "gmail_configured": bool(os.getenv("GMAIL_ADDRESS") and os.getenv("GMAIL_APP_PASSWORD"))
    }


# ----------------------------
#     CHATBOT ROUTE
# ----------------------------
class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatMessage):
    try:
        # Lazy load agent
        agent, session, run_config = get_agent()

        # Import Runner here to avoid module-level import
        from agents import Runner

        result = await Runner.run(
            agent,
            req.message,
            run_config=run_config,
            session=session,
        )
        return {"response": result.final_output}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Chat error: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )



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

    except HTTPException:
        raise
    except Exception as e:
        print("Contact Error:", e, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        raise HTTPException(500, "Internal Server Error")


# =========================================================
#           VERCEL SERVERLESS HANDLER
# =========================================================
handler = Mangum(app, lifespan="off")

# =========================================================
#               LOCAL DEV SERVER (optional)
# =========================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
