# 🚀 PaceBuddy — Multi-Agent AI System for Task, Schedule & Information Management

> **An API-first, production-ready multi-agent AI system that intelligently manages tasks, schedules, reminders, and contextual information by orchestrating multiple specialized agents and external tools.**

🌐 **Live Demo:** [https://pacebuddy2-417661527307.us-central1.run.app/dev-ui/?app=PaceBuddy](https://pacebuddy2-417661527307.us-central1.run.app/dev-ui/?app=PaceBuddy)
📦 **Repository:** [https://github.com/ashu485761/Pace-Buddy.git](https://github.com/ashu485761/Pace-Buddy.git)

---

## 📌 Problem Statement

Build a **multi-agent AI system** that helps users manage **tasks, schedules, and information** by interacting with **multiple tools and data sources**.

### ✅ Core Requirements Covered

* ✔ **Primary orchestrator agent** coordinating sub-agents
* ✔ **Multi-agent workflow execution**
* ✔ **Task & schedule management**
* ✔ **Structured data handling**
* ✔ **API-based cloud deployment**
* ✔ **Tool integration support (calendar, reminders, notes, info retrieval)**
* ✔ **Scalable cloud-native architecture**

---

# 🎯 What Makes PaceBuddy Special

PaceBuddy is not just a chatbot — it is a **real-world productivity intelligence platform**.

It uses a **hierarchical multi-agent architecture** where a **main coordinator agent** delegates responsibilities to domain-specific sub-agents.

This makes the system:

* ⚡ Faster in decision making
* 🧠 Better at task decomposition
* 🔄 Reliable in multi-step workflows
* ☁ Cloud deployable as microservice APIs
* 📈 Easy to scale with more tools and agents

---

# 🏗️ System Architecture

```text
                        ┌─────────────────────┐
                        │     User Query      │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │  Primary AI Agent   │
                        │   (Orchestrator)    │
                        └───────┬─────┬───────┘
                                │     │
                ┌───────────────┘     └───────────────┐
                ▼                                     ▼
      ┌──────────────────┐                  ┌──────────────────┐
      │ Scheduling Agent │                  │ Information Agent│
      │ - reminders      │                  │ - search notes   │
      │ - events         │                  │ - retrieve data  │
      └──────────────────┘                  └──────────────────┘
                │                                     │
                └───────────────┬─────────────────────┘
                                ▼
                      ┌────────────────────┐
                      │ External MCP Tools │
                      │ Calendar / Notes   │
                      │ Task Storage / API │
                      └────────────────────┘
```

---

# ⚙️ Multi-Agent Workflow

The intelligence of PaceBuddy lies in how agents collaborate.

## 1) 🧠 Primary Orchestrator Agent

The **main agent** receives the user intent and performs:

* Intent detection
* Task classification
* Context understanding
* Agent delegation
* Final response synthesis

## 2) 📅 Scheduling Agent

Handles:

* Meeting reminders
* Deadlines
* Study schedules
* Habit tracking
* Daily planning

## 3) 📚 Information Agent

Handles:

* Retrieving saved notes
* Searching structured data
* Summarizing stored information
* Querying tool responses

## 4) 🔗 Tool Interaction Layer

The agents connect with:

* Calendar systems
* Reminder workflows
* Database / storage
* External APIs
* MCP-compatible tools

---

# 🔥 Key Features

## ✅ Intelligent Task Planning

Automatically converts natural language into executable tasks.

**Example:**

> “Remind me to revise DSA tomorrow at 8 PM and save notes from today’s lecture.”

The orchestrator splits this into:

* Reminder creation
* Note storage
* Future retrieval reference

---

## ✅ Multi-Step Execution

Supports chained workflows such as:

1. Create task
2. Schedule reminder
3. Save metadata
4. Retrieve when requested
5. Update status

---

## ✅ Cloud-Native API Deployment

Deployed on **Google Cloud Run**, enabling:

* High availability
* Low-latency API responses
* Containerized deployment
* Production-ready endpoints

---

## ✅ Developer UI for Testing

The included **Dev UI endpoint** allows judges to directly test:

* agent orchestration
* workflow execution
* task routing
* session memory
* multi-turn conversations

---

# 🛠️ Tech Stack

## 💻 Backend

* Python
* FastAPI / Agent API
* Multi-Agent orchestration logic

## ☁ Cloud

* Google Cloud Run
* Service Account authentication
* Container Registry
* Environment-based config

## 🧠 AI Layer

* LLM-powered orchestration
* Tool routing
* Context memory
* Workflow decomposition

## 🔗 Integrations

* MCP tool connectors
* Reminder systems
* Calendar APIs
* Structured storage

---

# 📂 Project Structure

```text
PaceBuddy/
├── agent.py
├── __init__.py
├── requirements.txt
├── .env
└── deployment configs
```

---

# 🚀 Deployment

## Live Endpoint

```text
https://pacebuddy2-417661527307.us-central1.run.app
```

## Dev UI

```text
https://pacebuddy2-417661527307.us-central1.run.app/dev-ui/?app=PaceBuddy
```

---

# 🧪 Example Test Cases for Judges

## 📌 Test 1 — Reminder Workflow

**Prompt:**

```text
Remind me to submit my hackathon PPT tomorrow at 10 AM
```

**Expected:**

* task parsed
* schedule extracted
* reminder workflow triggered

## 📌 Test 2 — Multi-Agent Delegation

**Prompt:**

```text
Save today’s thermodynamics notes and remind me to revise on Sunday
```

**Expected:**

* info agent stores note
* scheduler agent sets reminder
* orchestrator merges result

## 📌 Test 3 — Information Retrieval

**Prompt:**

```text
What notes did I save for my DSA interview preparation?
```

**Expected:**

* retrieval agent searches stored data
* summarized response returned

---

# 🏆 Innovation Highlights

Why this stands out for judges:

* 🌟 **Real-world usability** beyond a simple chatbot
* 🌟 **True multi-agent orchestration design**
* 🌟 **Production deployment on cloud**
* 🌟 **Scalable architecture for future tools**
* 🌟 **MCP-compatible workflow expansion**
* 🌟 **Practical student productivity use case**

---

# 📈 Future Scope

* Google Calendar sync
* WhatsApp reminders
* Voice assistant support
* Team collaboration tasks
* Hackathon project planner
* Study + fitness schedule fusion
* Smart prioritization engine

---

# 👨‍💻 Author

**Ashutosh Biswal**
B.Tech Student | AI + Multi-Agent Systems | Cloud Deployment

---

# ⭐ Judge Impact Statement

> **PaceBuddy demonstrates how multi-agent AI can move beyond conversations into real productivity execution.**
>
> It combines **agent orchestration, cloud deployment, workflow automation, and tool integration** into a practical system that solves everyday task management challenges.

This directly aligns with the competition goal of building **API-based multi-agent systems that interact with multiple tools and structured data sources.**