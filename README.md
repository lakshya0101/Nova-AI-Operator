# NOVA — Personal AI Operating System

<p align="center">
<img src="https://img.shields.io/badge/NOVA-Personal%20AI%20Operating%20System-7C3AED?style=for-the-badge&logo=openai&logoColor=white" alt="NOVA" />
<img src="https://img.shields.io/badge/Architecture-Multi--Agent-2563EB?style=for-the-badge" alt="Multi-Agent Architecture" />
<img src="https://img.shields.io/badge/Protocol-MCP-0EA5E9?style=for-the-badge" alt="MCP" />
</p>

<p align="center">
<strong>Think. Plan. Delegate. Execute. Remember.</strong>
<br/>
<em>An intelligent AI operator designed to transform natural-language instructions into coordinated, multi-step actions.</em>
</p>

<p align="center">
<a href="#-overview">Overview</a> •
<a href="#-key-capabilities">Capabilities</a> •
<a href="#-system-architecture">Architecture</a> •
<a href="#-technology-stack">Tech Stack</a> •
<a href="#-getting-started">Installation</a> •
<a href="#-documentation">Documentation</a>
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-Backend-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/FastAPI-API-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/Next.js-Frontend-000000?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js" />
<img src="https://img.shields.io/badge/TypeScript-Frontend-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
<img src="https://img.shields.io/badge/Tailwind_CSS-Styling-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
<img src="https://img.shields.io/badge/SQLite-Persistence-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite" />
<img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=flat-square" alt="SQLAlchemy" />
<img src="https://img.shields.io/badge/NVIDIA-Nemotron-76B900?style=flat-square&logo=nvidia&logoColor=white" alt="NVIDIA Nemotron" />
</p>

---

## ✦ Overview

**NOVA (Personal AI Operating System)** is a multi-agent AI operator designed to move beyond conventional conversational assistants.

Traditional AI assistants primarily respond to individual prompts. NOVA is designed to understand objectives, break them into actionable steps, coordinate specialized agents, interact with tools, maintain persistent contextual memory, and execute workflows with appropriate human oversight.

It brings together an orchestration engine, six specialized agents, a persistent memory layer, external research capabilities, model routing, and an interactive operations dashboard.

Rather than treating every interaction as an isolated conversation, NOVA aims to provide a continuous environment where information, decisions, projects, tasks, and workflows can work together.

> [!IMPORTANT]
> **The core idea behind NOVA:** An AI system should not simply tell you what needs to be done. It should be capable of planning the work, coordinating the right capabilities, executing approved actions, and learning from the outcomes.

### Why NOVA?

| Conventional AI Assistant | NOVA |
|---|---|
| Responds to individual prompts | Understands multi-step objectives |
| Primarily conversational | Plan-oriented and execution-focused |
| Limited contextual continuity | Persistent, categorized memory |
| Single-agent interaction | Six specialized agents |
| Limited workflow visibility | Observable execution timeline |
| Tool execution with limited oversight | Human-in-the-loop approval |
| Isolated interactions | Context-aware workflows |

---

## ✦ Key Capabilities

### 01. Multi-Agent Intelligence

NOVA follows a specialized multi-agent architecture in which individual agents handle distinct responsibilities while collaborating through a centralized orchestration layer.

| Agent | Primary Responsibility |
|---|---|
| 🧠 **Planner Agent** | Interprets objectives and decomposes them into actionable steps |
| 🔍 **Research Agent** | Retrieves external information and performs research |
| 🗂️ **Memory Agent** | Manages contextual memory and information retrieval |
| ⚙️ **Execution Agent** | Coordinates tool execution and approved operations |
| 🛡️ **Critic Agent** | Evaluates plans, outputs, and execution quality |
| 🔄 **Reflection Agent** | Reviews outcomes and captures useful improvements |

The agents work together rather than operating as six unrelated assistants.

### 02. Persistent Contextual Memory

NOVA incorporates a structured memory layer to retain useful information across interactions.

Memory is organized into seven categories:

| Memory Category | Purpose |
|---|---|
| **Profile** | User preferences and personal context |
| **Decision** | Previously established decisions |
| **Project** | Project-related context and progress |
| **Task** | Tasks, priorities, and associated information |
| **Learned** | Knowledge and lessons captured over time |
| **Workflow** | Reusable workflow context |
| **Conversation** | Relevant conversational history |

**Memory capabilities include:**
- Persistent memory storage.
- Context retrieval.
- Semantic similarity-based matching.
- Memory deduplication.
- Categorized memory management.
- Integration with agent workflows.

### 03. Intelligent Planning and Execution

NOVA transforms natural-language instructions into structured execution plans.

**The orchestration layer supports:**
- Intent interpretation.
- Task decomposition.
- Execution-step generation.
- Specialized agent coordination.
- Dependency-aware workflow execution.
- Execution status tracking.
- Approval-gated state-changing operations.
- Outcome evaluation and reflection.

### 04. Human-in-the-Loop (HITL)

Automation should not eliminate user control.

NOVA incorporates approval checkpoints for designated state-changing operations, separating planning from authorization and execution.

This provides a controlled execution model where users can review operations before allowing them to proceed.

**Key principles:**
- Explicit approval for designated operations.
- Controlled execution.
- Separation of planning and execution.
- Traceable workflow activity.

### 05. External Research and Source Attribution

The Research Agent integrates with Tavily to retrieve external information and provide research context to downstream workflows.

**Capabilities include:**
- External web research.
- Structured research results.
- Source attribution.
- Research-driven workflow context.

### 06. Intelligent Model Routing

NOVA integrates with Nebius Token Factory and NVIDIA Nemotron models through a configurable model-routing layer.

The design supports two inference tiers:

| Model Tier | Intended Usage | Model Identifier |
|---|---|---|
| **Lightning** | Lightweight and faster operations | `nvidia/nemotron-mini-4b-instruct` |
| **Super** | Complex reasoning and demanding tasks | `nvidia/llama-3.1-nemotron-70b-instruct` |

The routing architecture balances responsiveness, model capability, and task complexity.

### 07. Model Context Protocol (MCP)

NOVA exposes an MCP-compatible server using Streamable HTTP.

This provides a standardized integration interface for connecting compatible external clients and tools to NOVA's capabilities.

The MCP layer includes server configuration, session management, and tool connectivity.

### 08. Interactive Operations Dashboard

NOVA includes a Next.js dashboard designed to provide a centralized operational view of the system.

| Dashboard Module | Function |
|---|---|
| **Overview Dashboard** | High-level operational overview |
| **Workspace** | Primary interaction environment |
| **Agent Monitor** | Agent activity and execution visibility |
| **Memory Explorer** | Explore categorized contextual memory |
| **Task Manager** | View and manage tasks |
| **Research Panel** | Display research information |
| **Execution Timeline** | Follow workflow execution steps |

---

## ✦ System Architecture

NOVA follows a modular architecture that separates the frontend, backend API, orchestration engine, specialized agents, persistence, and external integrations.

### High-Level Architecture

```mermaid
flowchart TB
    U(["User"])
    subgraph PRESENTATION["Presentation Layer"]
        UI["Next.js Dashboard"]
        WS["Workspace"]
        AM["Agent Monitor"]
        ME["Memory Explorer"]
        TM["Task Manager"]
        ET["Execution Timeline"]
    end
    subgraph BACKEND["Backend Layer"]
        API["FastAPI Backend"]
        ORCH["Orchestration Engine"]
    end
    subgraph AGENTS["Specialized Agent Layer"]
        PA["Planner Agent"]
        RA["Research Agent"]
        MA["Memory Agent"]
        EA["Execution Agent"]
        CA["Critic Agent"]
        RFA["Reflection Agent"]
    end
    subgraph INTEGRATIONS["External Integrations"]
        LLM["Model Routing"]
        NEB["Nebius / NVIDIA Nemotron"]
        TAV["Tavily Research"]
        MCP["MCP Streamable HTTP"]
        EXT["External MCP Clients"]
        HITL["Human Approval"]
        TOOLS["Execution Tools"]
    end
    subgraph DATA["Persistence Layer"]
        DB["Database Abstraction"]
        SQLITE[("SQLite")]
        PG[("PostgreSQL / pgvector")]
    end

    U --> UI
    UI --> WS
    UI --> AM
    UI --> ME
    UI --> TM
    UI --> ET
    UI <--> API
    API <--> ORCH
    ORCH <--> PA
    ORCH <--> RA
    ORCH <--> MA
    ORCH <--> EA
    ORCH <--> CA
    ORCH <--> RFA
    ORCH --> LLM
    LLM --> NEB
    RA --> TAV
    EA --> HITL
    HITL --> TOOLS
    MA <--> DB
    RFA --> DB
    DB --> SQLITE
    DB -. "Optional backend" .-> PG
    API <--> MCP
    MCP <--> EXT

    classDef presentation fill:#1d4ed8,color:#fff,stroke:#60a5fa
    classDef backend fill:#6d28d9,color:#fff,stroke:#a78bfa
    classDef agent fill:#0f766e,color:#fff,stroke:#5eead4
    classDef integration fill:#92400e,color:#fff,stroke:#fbbf24
    classDef data fill:#334155,color:#fff,stroke:#94a3b8

    class UI,WS,AM,ME,TM,ET presentation
    class API,ORCH backend
    class PA,RA,MA,EA,CA,RFA agent
    class LLM,NEB,TAV,MCP,EXT,HITL,TOOLS integration
    class DB,SQLITE,PG data
```

### Architecture Principles

- **Modularity:** Specialized components have clearly defined responsibilities.
- **Separation of concerns:** Presentation, orchestration, persistence, and integrations remain distinct.
- **Extensibility:** Model providers and MCP-compatible integrations can be extended.
- **Observability:** Agent activity and workflow execution are exposed through the dashboard.
- **Human oversight:** Designated state-changing operations require approval.
- **Persistence:** Useful contextual information is retained across sessions.

### Agent Execution Lifecycle

A typical NOVA workflow follows a structured lifecycle:

```mermaid
flowchart TD
    A(["User Instruction"]) --> B["Intent Interpretation"]
    B --> C["Planner Agent"]
    C --> D["Generate Execution Plan"]
    D --> E["Orchestration Engine"]
    E --> F{"Select Required Agent"}
    F --> G["Research Agent"]
    F --> H["Memory Agent"]
    F --> I["Execution Agent"]
    F --> J["Critic Agent"]
    G --> K["Return Agent Result"]
    H --> K
    I --> L{"Approval Required?"}
    L -->|Yes| M["Human Approval"]
    L -->|No| N["Execute Operation"]
    M -->|Approved| N
    M -->|Rejected| O["Skip / Handle Rejection"]
    N --> K
    O --> K
    J --> K
    K --> P["Evaluate Workflow Outcome"]
    P --> Q["Reflection Agent"]
    Q --> R["Update Relevant Context"]
    R --> S(["Execution Summary"])
```

### Execution Philosophy

NOVA separates the stages of understanding, planning, authorization, execution, and reflection.
This makes workflows easier to inspect, reason about, and control.

### Memory and Database Architecture

NOVA uses a persistence layer to retain tasks, preferences, and contextual memory.
SQLite is the default database configuration. PostgreSQL with pgvector is included as an optional extended persistence direction.

#### Logical Persistence Architecture

```mermaid
flowchart TB
    subgraph AGENT_LAYER["Agent Layer"]
        MA["Memory Agent"]
        PA["Planner Agent"]
        RA["Research Agent"]
        RFA["Reflection Agent"]
    end
    subgraph MEMORY_LAYER["Memory Service Layer"]
        MS["Memory Service"]
        RET["Memory Retrieval"]
        DEDUP["Deduplication"]
        SIM["Semantic Similarity"]
        CAT["Memory Categorization"]
    end
    subgraph ORM_LAYER["Persistence Abstraction"]
        ORM["SQLAlchemy ORM"]
        DB["Database Configuration"]
    end
    subgraph STORAGE["Storage Backends"]
        SQLITE[("SQLite - Default")]
        POSTGRES[("PostgreSQL - Optional")]
        VECTOR[("pgvector - Optional")]
    end

    MA <--> MS
    PA --> RET
    RA --> RET
    RFA --> MS
    MS --> RET
    MS --> DEDUP
    MS --> SIM
    MS --> CAT
    RET --> ORM
    DEDUP --> ORM
    SIM --> ORM
    CAT --> ORM
    ORM --> DB
    DB --> SQLITE
    DB -. "Optional configuration" .-> POSTGRES
    POSTGRES -. "Vector extension" .-> VECTOR
```

#### Logical Memory Model

The following diagram illustrates NOVA's memory classification. It represents logical memory categories, not a physical database schema.

```mermaid
mindmap
  root((NOVA Memory))
    Profile
      Preferences
      User Context
    Decision
      Previous Decisions
      Rationale
    Project
      Project Context
      Progress
    Task
      Priorities
      Task Context
    Learned
      Knowledge
      Lessons
    Workflow
      Workflow Context
      Reusable Patterns
    Conversation
      Interaction Context
      Relevant History
```

#### Persistence Design

| Component | Purpose |
|---|---|
| **SQLAlchemy** | Database interaction and ORM abstraction |
| **SQLite** | Default local persistence |
| **PostgreSQL** | Optional extended database backend |
| **pgvector** | Optional vector storage capability |
| **Memory Service** | Memory creation, retrieval, and management |
| **Database Configuration** | Centralized persistence configuration |

> [!NOTE]
> PostgreSQL/pgvector support is an optional architectural direction. Its live deployment and end-to-end operation should be validated separately before being treated as a verified production capability.

### Research and Model Integration

NOVA separates external intelligence providers from the orchestration layer.

#### Model Integration

```mermaid
flowchart TD
    A["Orchestration Engine"] --> B["Model Routing Layer"]
    B --> C{"Task Complexity / Routing"}
    C --> D["Lightning Tier"]
    C --> E["Super Tier"]
    D --> F["Nebius Token Factory"]
    E --> F
    F --> G["NVIDIA Nemotron Models"]
    G --> H["Structured Agent Response"]
    H --> A
```

#### Research Integration

```mermaid
sequenceDiagram
    autonumber
    participant O as Orchestrator
    participant R as Research Agent
    participant T as Tavily
    participant M as Memory Agent
    O->>R: Research request
    R->>T: Submit external search
    T-->>R: Search results and sources
    R->>R: Structure research findings
    R-->>O: Return research context
    O->>M: Provide relevant context
    M-->>O: Return contextual information
    O->>O: Continue workflow
```

---

## ✦ Technology Stack

NOVA combines a modern web frontend, Python backend, multi-agent orchestration, persistent storage, and external AI integrations.

| Layer | Technologies |
|---|---|
| **Frontend Framework** | Next.js 14 |
| **Frontend Language** | TypeScript |
| **Styling** | Tailwind CSS |
| **UI Icons** | Lucide React |
| **Animations** | Framer Motion |
| **Backend Framework** | Python, FastAPI |
| **API Documentation** | FastAPI / OpenAPI |
| **AI Models** | Nebius Token Factory, NVIDIA Nemotron |
| **Research Integration** | Tavily |
| **ORM** | SQLAlchemy |
| **Default Database** | SQLite |
| **Optional Database** | PostgreSQL, pgvector |
| **Agent Connectivity** | Model Context Protocol |
| **MCP Transport** | Streamable HTTP |
| **Testing** | Pytest |
| **Package Management** | pip, npm |

### Technology Highlights

<p>
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" />
<img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
<img src="https://img.shields.io/badge/Tailwind-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" />
<img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square" />
<img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" />
<img src="https://img.shields.io/badge/NVIDIA-76B900?style=flat-square&logo=nvidia&logoColor=white" />
<img src="https://img.shields.io/badge/MCP-2563EB?style=flat-square" />
</p>

---

## ✦ Project Structure

```text
NOVA-AI-OPERATOR/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── planner_agent.py
│   │   │   ├── research_agent.py
│   │   │   ├── memory_agent.py
│   │   │   ├── execution_agent.py
│   │   │   ├── critic_agent.py
│   │   │   └── reflection_agent.py
│   │   ├── core/
│   │   │   └── nebius_client.py
│   │   ├── models/
│   │   │   ├── memory.py
│   │   │   ├── preference.py
│   │   │   └── task.py
│   │   ├── schemas/
│   │   │   ├── memory.py
│   │   │   ├── orchestration.py
│   │   │   ├── preference.py
│   │   │   ├── research.py
│   │   │   └── task.py
│   │   ├── services/
│   │   │   ├── memory_service.py
│   │   │   ├── orchestration_service.py
│   │   │   ├── preference_service.py
│   │   │   ├── task_service.py
│   │   │   └── tavily_service.py
│   │   ├── tools/
│   │   │   └── mcp_server.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_agents.py
│   │   ├── test_health.py
│   │   ├── test_mcp.py
│   │   ├── test_memory.py
│   │   ├── test_nebius.py
│   │   ├── test_orchestration.py
│   │   ├── test_tasks.py
│   │   └── test_tavily.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── legacy/
│   │   ├── app.js
│   │   ├── index.html
│   │   └── style.css
│   ├── src/
│   │   ├── app/
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   └── components/
│   │       ├── AgentMonitor.tsx
│   │       ├── DashboardOverview.tsx
│   │       ├── ExecutionTimeline.tsx
│   │       ├── MemoryExplorer.tsx
│   │       ├── ResearchPanel.tsx
│   │       ├── Sidebar.tsx
│   │       ├── TaskManager.tsx
│   │       └── Workspace.tsx
│   ├── next-env.d.ts
│   ├── next.config.js
│   ├── package.json
│   ├── package-lock.json
│   └── tailwind.config.js
├── scripts/
│   ├── verify_mcp_client.py
│   ├── verify_milestone_l1.py
│   ├── verify_nebius_live.py
│   ├── verify_production_readiness.py
│   └── verify_tavily_live.py
├── .env.example
├── .gitignore
├── API_CONTRACT.md
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── FINAL_RELEASE_CHECKLIST.md
├── LICENSE
├── PRODUCTION_READINESS_REPORT.md
├── README.md
├── SETUP.md
└── requirements.txt
```

---

## ✦ Getting Started

Follow the steps below to run NOVA locally.

### Prerequisites

Make sure the following are installed:
- Python 3.10+
- Node.js (v18+) and npm
- Git
- API credentials for the external integrations you intend to enable (Nebius, Tavily)

### 1. Clone the Repository

```bash
git clone https://github.com/lakshya0101/Nova-AI-Operator.git
cd Nova-AI-Operator
```

### 2. Set Up the Backend

Navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment:
```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a local environment file:

**Windows PowerShell:**
```powershell
Copy-Item .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

Configure the relevant variables in `.env`:
```ini
# NOVA Configuration
LOG_LEVEL=INFO

# Persistence
DATABASE_URL=sqlite:///./nova.db

# Nebius Token Factory
NEBIUS_API_KEY=
NEBIUS_BASE_URL=https://api.studio.nebius.ai/v1

# Model Configuration
NEBIUS_MODEL_LIGHTNING=nvidia/nemotron-mini-4b-instruct
NEBIUS_MODEL_SUPER=nvidia/llama-3.1-nemotron-70b-instruct

# External Research
TAVILY_API_KEY=

# MCP Configuration
MCP_SERVER_NAME=nova
MCP_SERVER_VERSION=2.0.0
MCP_MOUNT_PATH=/mcp
```

> [!WARNING]
> Keep your actual API keys in your local `.env` file. Never commit credentials, tokens, or other secrets to the repository.

### 4. Start the Backend Server

From the backend directory:
```bash
uvicorn app.main:app --reload --port 8000
```

- **Backend API:** `http://localhost:8000`
- **Interactive Documentation:** `http://localhost:8000/docs`

### 5. Start the Frontend

Open another terminal and navigate to the frontend directory:
```bash
cd frontend
npm install
npm run dev
```

- **Frontend Dashboard:** `http://localhost:3000`

### 6. Access NOVA

Once both services are running, open your browser:
```text
http://localhost:3000
```

The NOVA operational dashboard should now be available locally. For additional configuration details, refer to [SETUP.md](SETUP.md).

---

## ✦ Testing and Validation

NOVA includes automated tests and verification scripts covering its core backend functionality.

### Test Coverage Areas

| Area | Validation Focus |
|---|---|
| **Agents** | Agent behavior and coordination |
| **Memory** | Memory creation, retrieval, and management |
| **Orchestration** | Workflow planning and execution |
| **Approval** | Approval enforcement and security checkpoints |
| **MCP** | MCP server functionality and tool registry |
| **Tasks** | Task management operations |
| **Health** | Backend health and API behavior |
| **Integrations** | Model and research integration interfaces |

### Run Backend Tests

From the repository root or backend directory:
```bash
pytest -v
```

### Additional Verification Scripts

The `scripts/` directory contains dedicated verification utilities:

| Script | Purpose |
|---|---|
| `verify_mcp_client.py` | MCP client verification |
| `verify_milestone_l1.py` | Milestone verification |
| `verify_nebius_live.py` | Live Nebius integration verification |
| `verify_production_readiness.py` | Production-readiness checks |
| `verify_tavily_live.py` | Live Tavily integration verification |

> [!IMPORTANT]
> Passing automated tests and local simulations does not establish that every external service is working live. Nebius inference, Tavily research, and optional PostgreSQL/pgvector functionality require their respective credentials, configuration, and separate integration testing.

---

## ✦ Security and Execution Control

NOVA is designed around controlled execution rather than unrestricted automation.

**Key considerations include:**
- Environment-based configuration for external credentials.
- Approval checkpoints for designated state-changing actions.
- Separation of planning and execution.
- Modular integration boundaries.
- Observable workflow execution.
- Persistent operational context.

As the system evolves, additional permission controls, deployment safeguards, and operational security measures will continue to be refined.

---

## ✦ Roadmap

NOVA is being developed toward a more capable, reliable, and extensible personal AI operating environment.

```mermaid
flowchart LR
    A["Foundation"] --> B["Multi-Agent Intelligence"] --> C["Persistent Memory"] --> D["Tool Orchestration"] --> E["Advanced Automation"] --> F["Production-Ready AI OS"]

    classDef completed fill:#065f46,color:#fff,stroke:#34d399
    classDef ongoing fill:#1d4ed8,color:#fff,stroke:#60a5fa
    classDef future fill:#475569,color:#fff,stroke:#cbd5e1

    class A,B,C,D completed
    class E ongoing
    class F future
```

### Planned Enhancements

| Area | Future Direction |
|---|---|
| **Agent Intelligence** | More adaptive planning and agent coordination |
| **Memory** | Improved contextual retrieval and memory refinement |
| **Model Routing** | Additional providers and intelligent model selection |
| **Automation** | Broader real-world workflow execution |
| **Integrations** | Expanded MCP tools and external services |
| **Security** | More granular permission management |
| **Observability** | Richer traces, metrics, and system-level monitoring |
| **Deployment** | Production-oriented deployment and scaling |

---

## ✦ Documentation

Explore the technical documentation included in the repository:

| Document | Description |
|---|---|
| [Architecture](ARCHITECTURE.md) | System design and architectural components |
| [Setup Guide](SETUP.md) | Local installation and configuration |
| [API Contract](API_CONTRACT.md) | Backend API contracts |
| [Production Readiness Report](PRODUCTION_READINESS_REPORT.md) | Implementation and readiness assessment |
| [Final Release Checklist](FINAL_RELEASE_CHECKLIST.md) | Release verification checklist |
| [Contributing Guidelines](CONTRIBUTING.md) | Contribution workflow and guidelines |
| [License](LICENSE) | Project licensing information |

---

## ✦ Contributors

NOVA is developed collaboratively:

| Contributor | Contribution |
|---|---|
| **Lakshya Dogra** | Project architecture, AI orchestration, backend engineering, and system integration |
| **Smriti Verma** | Project collaboration and development |

---

## ✦ Contributing

Contributions, ideas, and improvements are welcome. If you would like to contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Implement your changes.
4. Add or update relevant tests.
5. Submit a pull request with a clear description.

Please review [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.

---

## ✦ License

This project is distributed under the Apache License 2.0. Please refer to [LICENSE](LICENSE) for the applicable terms.

---

<p align="center">
<img src="https://img.shields.io/badge/Built%20with-AI%20%2B%20Engineering-7C3AED?style=for-the-badge" alt="Built with AI and Engineering" />
</p>

<h3 align="center">NOVA — From Conversations to Coordinated Action.</h3>

<p align="center">
<em>Building a more capable, contextual, and controllable personal AI operating system.</em>
</p>

<p align="center">
<a href="https://github.com/lakshya0101/Nova-AI-Operator">Explore NOVA on GitHub</a>
</p>
