import os
import logging
import datetime
import google.cloud.logging
from google.cloud import datastore
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from mcp.server.fastmcp import FastMCP 

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext

# --- 1. Infrastructure Setup ---
try:
    cloud_logging_client = google.cloud.logging.Client()
    cloud_logging_client.setup_logging()
except Exception:
    logging.basicConfig(level=logging.INFO)

load_dotenv()
model_name = os.getenv("MODEL", "gemini-1.5-flash")

# --- 2. Database Setup (Named 'genai') ---
db = datastore.Client(database="genai") 
mcp = FastMCP("ReminderTools")

# ================= 3. MCP TOOLS =================

@mcp.tool()
def create_reminder(text: str, remind_at: str) -> str:
    """Saves a reminder to the 'genai' database. Format: YYYY-MM-DD HH:MM."""
    try:
        key = db.key('Reminder')
        reminder = datastore.Entity(key=key)
        reminder.update({
            'text': text, 
            'remind_at': remind_at,
            'status': 'pending',
            'created_at': datetime.datetime.now()
        })
        db.put(reminder)
        return f"🔔 Success: Reminder for '{text}' saved in 'genai' database."
    except Exception as e:
        logging.error(f"Datastore Error: {e}")
        return f"Datastore Error: {str(e)}"

@mcp.tool()
def list_reminders() -> str:
    """Lists all pending reminders from the 'genai' database."""
    try:
        query = db.query(kind='Reminder')
        results = list(query.fetch())
        if not results: return "No reminders found in 'genai' database."
        return "\n".join([f"⏰ {r['remind_at']}: {r['text']}" for r in results])
    except Exception as e:
        return f"Query Error: {str(e)}"

# ================= 4. AGENTS =================

def add_prompt_to_state(tool_context: ToolContext, prompt: str):
    """Bridges the gap between Root input and Workflow execution."""
    tool_context.state["PROMPT"] = prompt
    return {"status": "state_updated"}

reminder_specialist = Agent(
    name="reminder-specialist",
    model=model_name,
    instruction=lambda ctx: f"Goal: {ctx.state.get('PROMPT')}. Help the user manage reminders.",
    tools=[create_reminder, list_reminders]
)

workflow = SequentialAgent(name="workflow", sub_agents=[reminder_specialist])

root_agent = Agent(
    name="root",
    model=model_name,
    instruction=lambda ctx: f"User input: {ctx.state.get('user_input')}. Save it and trigger workflow.",
    tools=[add_prompt_to_state],
    sub_agents=[workflow]
)

# ================= 5. API =================

app = FastAPI(title="Reminder Multi-Agent API")

class ReminderRequest(BaseModel):
    prompt: str

@app.post("/api/v1/reminders/chat")
async def chat(request: ReminderRequest):
    try:
        final_reply = ""
        # .run_async is the standard for google-adk 1.14.0 
        async for event in root_agent.run_async({"user_input": request.prompt}):
            if hasattr(event, 'text') and event.text:
                final_reply = event.text
        return {"status": "success", "reply": final_reply}
    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)