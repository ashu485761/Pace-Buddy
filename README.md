# 🔔 Reminder AI: Multi-Agent Workspace Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.130.0-05998b.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Run-4285F4?style=flat&logo=google-cloud)](https://cloud.google.com/run)
[![Agent SDK](https://img.shields.io/badge/Google%20ADK-1.14.0-blue)](https://github.com/google/unitig)

An intelligent, multi-agent reminder system built with **Google ADK 1.14.0**, **FastAPI**, and **Google Cloud Datastore**. This project demonstrates sophisticated agent orchestration where a root coordinator delegates tasks to specialized sub-agents.

## 🚀 Features

* [cite_start]**Multi-Agent Orchestration**: Features a `Root Agent` for intent parsing and a `Reminder Specialist` for tool execution[cite: 1, 2].
* [cite_start]**Structured Data Persistence**: Integrates with Google Cloud Datastore (named `genai` database) to store and retrieve reminders.
* [cite_start]**MCP Tool Integration**: Uses the **Model Context Protocol (FastMCP)** to standardize how agents interact with the database[cite: 1, 2].
* [cite_start]**Production Ready**: Fully containerized for **Google Cloud Run** with built-in Cloud Logging support[cite: 1, 2].

## 📂 Project Structure

```text
.
├── agent/
│   ├── __init__.py      # Module initialization
│   └── agent.py         # Logic for Datastore, MCP, and Agents
├── .env                 # Environment variables (Local)
├── Dockerfile           # Python 3.12 optimized container
├── README.md            # You are here!
└── requirements.txt     # Pinned 2026-compatible dependencies
