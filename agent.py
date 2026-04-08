import os
import logging
import datetime
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

import google.cloud.logging
from google.cloud import datastore

from mcp.server.fastmcp import FastMCP
from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext

# ================= CONFIG =================
load_dotenv()

PROJECT_NAME = "PaceBuddy"
OWNER_NAME = "Ashutosh"

PROJECT_ID = os.getenv("PROJECT_ID", "")
PROJECT_NUMBER = os.getenv("PROJECT_NUMBER", "")
SA_NAME = os.getenv("SA_NAME", "lab2-cr-service")
SERVICE_ACCOUNT = os.getenv(
    "SERVICE_ACCOUNT",
    "",
)

MODEL_NAME = os.getenv("MODEL", "gemini-2.5-flash")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv(
    "GOOGLE_GENAI_USE_VERTEXAI", "True"
)

try:
    cloud_logging_client = google.cloud.logging.Client(project=PROJECT_ID)
    cloud_logging_client.setup_logging()
except Exception:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(PROJECT_NAME)

# ================= DATABASE =================
db = datastore.Client(project=PROJECT_ID)

# ================= MCP =================
mcp = FastMCP(PROJECT_NAME)

@mcp.tool()
def add_task(title: str, due_date: Optional[str] = None) -> str:
    try:
        key = db.key("Task")
        task = datastore.Entity(key=key)
        task.update({
            "title": title,
            "due_date": due_date or "Not set",
            "completed": False,
            "created_at": datetime.datetime.utcnow().isoformat(),
        })
        db.put(task)
        return f"Task added for {OWNER_NAME}: {title}"
    except Exception as e:
        logger.exception("add_task failed")
        return f"Error: {e}"

@mcp.tool()
def list_tasks() -> str:
    try:
        query = db.query(kind="Task")
        tasks = list(query.fetch())

        if not tasks:
            return "No tasks found."

        result = ["PaceBuddy Tasks:"]
        for task in tasks:
            status = "Done" if task.get("completed") else "Pending"
            result.append(f"- {task['title']} | {status} | ID={task.key.id}")

        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def complete_task(task_id: int) -> str:
    try:
        key = db.key("Task", task_id)
        task = db.get(key)

        if not task:
            return "Task not found."

        task["completed"] = True
        db.put(task)
        return f"Task {task_id} completed."
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def add_note(title: str, content: str) -> str:
    try:
        key = db.key("Note")
        note = datastore.Entity(key=key)
        note.update({
            "title": title,
            "content": content,
            "owner": OWNER_NAME,
            "created_at": datetime.datetime.utcnow().isoformat(),
        })
        db.put(note)
        return f"Note saved for {OWNER_NAME}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def schedule_event(title: str, date_time: str) -> str:
    try:
        key = db.key("CalendarEvent")
        event = datastore.Entity(key=key)
        event.update({
            "title": title,
            "date_time": date_time,
            "owner": OWNER_NAME,
            "created_at": datetime.datetime.utcnow().isoformat(),
        })
        db.put(event)
        return f"Event '{title}' scheduled for {date_time}"
    except Exception as e:
        return f"Error: {e}"

# ================= MULTI AGENT =================
def save_prompt(tool_context: ToolContext, prompt: str):
    tool_context.state["workflow_prompt"] = prompt
    return {"saved": True}

def planner_instruction(ctx):
    prompt = ctx.state.get("workflow_prompt", "Help the user")
    return f"""
You are the primary orchestration agent for {PROJECT_NAME}.
Coordinate sub-agents and tools to complete workflows.

Current request: {prompt}
"""

TaskAgent = Agent(
    name="task_agent",
    model=MODEL_NAME,
    instruction=f"You manage tasks for {OWNER_NAME}",
    tools=[add_task, list_tasks, complete_task, schedule_event],
)

NotesAgent = Agent(
    name="notes_agent",
    model=MODEL_NAME,
    instruction=f"You manage notes for {OWNER_NAME}",
    tools=[add_note],
)

WorkflowAgent = SequentialAgent(
    name="workflow_agent",
    sub_agents=[TaskAgent, NotesAgent],
)

root_agent = Agent(
    name="primary_orchestrator",
    model=MODEL_NAME,
    instruction=planner_instruction,
    tools=[save_prompt],
    sub_agents=[WorkflowAgent],
)

RootAgent = root_agent

# ================= FASTAPI =================
app = FastAPI(title=PROJECT_NAME)

class UserRequest(BaseModel):
    prompt: str

@app.get("/")
def home() -> Dict[str, Any]:
    return {
        "project": PROJECT_NAME,
        "owner": OWNER_NAME,
        "status": "running",
    }

@app.post("/api/v1/pacebuddy/chat")
async def chat(request: UserRequest):
    try:
        final_reply = ""
        async for event in root_agent.run_async(
            {"workflow_prompt": request.prompt}
        ):
            if hasattr(event, "text") and event.text:
                final_reply = event.text

        return {
            "status": "success",
            "reply": final_reply or "Workflow completed successfully",
        }

    except Exception as e:
        logger.exception("chat failed")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)