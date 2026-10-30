# NOVA 2.0 – Setup & Installation Guide

This guide walks you through setting up and running **NOVA – Personal AI Operating System** locally.

---

## Prerequisites

- **Python:** 3.10 or higher
- **Node.js:** 18.x or higher (Node 20+ recommended)
- **Git**
- Optional: Nebius Token Factory API Key (`NEBIUS_API_KEY`)
- Optional: Tavily Search API Key (`TAVILY_API_KEY`)

*(Note: NOVA includes an intelligent local simulation fallback for both Nebius and Tavily, allowing full offline testing and development without live cloud credentials.)*

---

## 1. Backend Setup

### Clone Repository & Navigate
```bash
git clone https://github.com/lakshya0101/Nova-AI-Operator.git
cd Nova-AI-Operator
```

### Create and Activate Virtual Environment
```bash
# On Windows PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# On macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` to configure your API keys:
```env
# Optional Live Nebius Credentials
NEBIUS_API_KEY=your_nebius_api_key_here
NEBIUS_BASE_URL=https://api.studio.nebius.ai/v1
NEBIUS_MODEL_LIGHTNING=nvidia/nemotron-mini-4b-instruct
NEBIUS_MODEL_SUPER=nvidia/llama-3.1-nemotron-70b-instruct

# Optional Live Tavily Credentials
TAVILY_API_KEY=your_tavily_api_key_here

# Persistence
DATABASE_URL=sqlite:///./nova.db
```

### Run Automated Backend Tests
```bash
pytest -v
```
All 36 tests across orchestration, specialized agents, memory, MCP protocol, and Nebius client will run and pass.

### Start the FastAPI & MCP Server
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
The server will initialize SQLite schemas, seed default memories and preferences, and mount the MCP Streamable HTTP session manager at `http://127.0.0.1:8000/mcp`.

- API Documentation: `http://127.0.0.1:8000/docs`
- Health Endpoint: `http://127.0.0.1:8000/health`

---

## 2. Frontend Setup (Next.js Command Center)

Open a new terminal window:

```bash
cd frontend
npm install
npm run dev
```

Open your browser to:
```
http://localhost:3000
```

---

## 3. Running the Benchmark Demonstration

1. In the NOVA Command Center UI, navigate to the **AI Workspace**.
2. Select or enter the primary benchmark instruction:
   > *"Organize my evening. Prioritize my unfinished tasks, research the latest AI agent developments, and leave time for interview preparation."*
3. Click **Preview Plan (Dry Run)** to observe:
   - Memory Agent semantically retrieving personal context.
   - Tavily Research Agent retrieving verified web citations.
   - Planner Agent generating the multi-step schedule with approval gates.
   - Critic Agent verifying safety constraints.
4. Click **Execute Workflow (Approved)** to execute the action items via MCP tools, create the Interview Preparation task in persistent storage, and trigger the Reflection Agent to save the workflow outcome into long-term memory.

