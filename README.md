# 🤖 Syntera AI

A modular **Agentic AI system** built with **LangChain, LangGraph, MCP (Model Context Protocol), FastMCP, and configurable LLM providers**.

The project demonstrates how multiple specialized agents can be orchestrated through a stateful workflow while research capabilities are exposed through MCP rather than being tightly coupled to the Research Agent.

> **Project status:** Active learning/engineering project. The current implementation focuses on multi-agent orchestration, MCP integration, tool discovery, coding assistance, research, and extensibility. The roadmap below describes the next production-oriented upgrades.

---

## 🎯 Project Overview

The system accepts a user query and uses a **Supervisor Agent** to determine the initial task category.

Current high-level routing:

```text
                         User Query
                              │
                              ▼
                     ┌─────────────────┐
                     │ Supervisor      │
                     │ Agent           │
                     └────────┬────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
             General       Research       Coding
                │             │             │
                ▼             ▼             ▼
               END           END           END
```

The important design principle is that the Supervisor performs **initial routing**, while specialist agents are responsible for performing their own domain-specific work.

The Coding Agent is designed to be capable of generating code, inspecting an existing codebase, and using filesystem/code-analysis tools. A future upgrade will allow it to explicitly request research when additional information is required.

---

## 🧩 Core Components

### Supervisor Agent

Responsible for:

- Understanding the user's initial request
- Selecting the appropriate specialist
- Returning a structured routing decision
- Avoiding direct execution of specialist tasks

### General Agent

Handles:

- General questions
- Explanations
- Conversational requests
- Tasks that do not require specialized tools

### Research Agent

Responsible for:

- Information gathering
- Web research
- Academic research
- YouTube discovery and transcript retrieval
- Reading webpages
- Synthesizing research results

Research capabilities are exposed through an MCP server.

### Coding Agent

Responsible for:

- Code generation
- Code analysis
- Existing project inspection
- File operations when explicitly requested
- Software-engineering tasks

The Coding Agent follows an important distinction:

> Asking for code does not automatically mean creating a file. Filesystem write operations are performed only when the user explicitly requests a file operation.

---

## 🔌 MCP Integration

The project uses **Model Context Protocol (MCP)** to decouple research capabilities from the Research Agent.

Current architecture:

```text
Research Agent
      │
      ▼
LangChain-compatible MCP Tools
      │
      ▼
MCP Client
      │
      ▼
MCP Manager
      │
      ▼
Research MCP Server
      │
      ├── DuckDuckGo Search
      ├── Google Search
      ├── Webpage Reader
      ├── YouTube Search
      ├── YouTube Transcript
      └── arXiv Search
```

The MCP server is implemented using **FastMCP** and currently communicates through a local **stdio** connection.

The Research Agent discovers the available MCP tools at runtime instead of hardcoding the implementation of every research capability.

---

## 🌟 Current Features

- 🤖 Multi-agent architecture
- 🧠 Supervisor-based initial routing
- 🔍 Specialized Research Agent
- 💻 Specialized Coding Agent
- 💬 General conversational Agent
- 🔌 MCP-based research tools
- 🔎 Dynamic MCP tool discovery
- 🧩 LangChain tool adapters for MCP
- 🔄 LangGraph workflow orchestration
- 📝 Structured workflow state
- 📊 Detailed logging
- ⚡ Async MCP/tool execution
- 🦙 Ollama support for local inference
- ☁️ Groq support for cloud inference
- 🔁 Ollama/Groq model configuration
- 🛠️ Filesystem and Python AST tools for coding
- 📈 Workflow visualization
- 🧪 Component and workflow testing support

---

## 🏗️ Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Agent Framework | LangChain |
| Workflow | LangGraph |
| Protocol | MCP |
| MCP Framework | FastMCP |
| Local LLM | Ollama |
| Cloud LLM | Groq |
| Research | DuckDuckGo, Google, arXiv, YouTube, Webpage Reader |
| Validation | Pydantic |
| Web Parsing | BeautifulSoup |
| YouTube | yt-dlp, youtube-transcript-api |
| Configuration | Pydantic Settings |
| UI | Streamlit (planned/current extension) |

---

## 📦 Installation

### Prerequisites

- Python 3.10+
- pip
- Git
- Optional: Ollama
- Groq API key if using Groq
- Google Search credentials if using Google Search through the MCP server

### Setup

```bash
git clone <repository-url>
cd Syntera-AI

python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
GROQ_API_KEY=your_groq_api_key

GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_cse_id

OLLAMA_BASE_URL=http://localhost:11434

SUPERVISOR_MODEL=llama-3.3-70b-versatile
GENERAL_MODEL=llama-3.3-70b-versatile
RESEARCH_MODEL=llama-3.3-70b-versatile
CODING_MODEL=llama-3.3-70b-versatile

SUPERVISOR_OLLAMA_MODEL=llama3.2:latest
GENERAL_OLLAMA_MODEL=llama3.2:latest
RESEARCH_OLLAMA_MODEL=llama3.2:latest
CODING_OLLAMA_MODEL=llama3.2:latest
```

---

## 🚀 Running the Application

### Groq

```bash
python main.py
```

### Ollama

```bash
python main.py --use-ollama
```

The application initializes the MCP server, discovers its tools, initializes the agents, compiles the LangGraph workflow, and then accepts queries.

---

## 💬 Example Queries

### General

```text
What is machine learning?
Explain object-oriented programming.
What is the difference between Python and JavaScript?
```

### Research

```text
Find recent papers on RAG systems.
Search YouTube for LangChain tutorials.
What are the latest developments in agentic AI?
```

### Coding

```text
Give me a Python implementation of a REST API.
Analyze the structure of my Python project.
Create a Python file containing a FastAPI application.
```

---

# 🚀 Scope of Upgrade

The current implementation establishes the core multi-agent + MCP pipeline. The next stage is to evolve it from a **single-query workflow** into a more complete **stateful agentic application**.

The upgrades below are intentionally separated from the current implementation.

## 1. 💬 Message History

Current behavior is primarily query-oriented.

Upgrade:

```text
User
 ├── Message 1
 ├── Message 2
 ├── Message 3
 └── ...
```

Maintain conversation history so the agents can understand references such as:

```text
User: Create a FastAPI application.
User: Add authentication to it.
User: Now add tests.
```

The third request should be understood in the context of the previous conversation.

Potential implementation:

- LangGraph message state
- `MessagesState`
- Conversation history in persistent storage
- Token/window management
- History summarization for long conversations

---

## 2. 👤 Session Management

Introduce a unique `session_id` for every conversation.

```text
session_id
    │
    ├── conversation history
    ├── workflow state
    ├── user preferences
    └── session metadata
```

Potential storage:

- SQLite for local development
- PostgreSQL for production
- Redis for fast session state/cache

---

## 3. 🧠 Persistent Memory

Separate short-term conversation history from longer-term memory.

Possible memory categories:

```text
Short-Term Memory
    └── Current conversation

Long-Term Memory
    ├── User preferences
    ├── Project context
    ├── Previous decisions
    └── Useful persistent facts
```

A future version can add a memory/retrieval layer using a vector database where appropriate.

---

## 4. 🔁 Dynamic Agent Collaboration

The current Supervisor performs initial routing.

Future pipeline:

```text
User
  ↓
Supervisor
  ↓
Coding Agent
  ↓
"I need research"
  ↓
Research Agent
  ↓
Research Result
  ↓
Coding Agent
  ↓
Final Result
```

The important change is that the Coding Agent—not the Supervisor—can determine that additional research is required.

This can later evolve into:

```text
Coding
  ↓
Research
  ↓
Coding
  ↓
Research
  ↓
Coding
  ↓
END
```

with explicit iteration limits and termination conditions.

---

## 5. 🧭 Better Planning

Introduce planning for complex requests.

```text
User Request
     ↓
Planner
     ↓
Task Plan
     ├── Research
     ├── Coding
     ├── Validation
     └── Final Response
```

This allows the system to decompose complex tasks instead of treating every request as a single operation.

---

## 6. 🛠️ More MCP Servers

The current MCP layer contains research capabilities.

Future MCP servers could include:

```text
mcp_servers/
├── research_server.py
├── filesystem_server.py
├── database_server.py
├── github_server.py
├── browser_server.py
└── documentation_server.py
```

This would demonstrate MCP as a reusable capability layer rather than only a research integration.

---

## 7. 🔐 Tool Permissions and Sandboxing

As coding capabilities grow, filesystem access should become controlled.

Potential improvements:

- Allowed directories
- Read/write permissions
- Path validation
- Command execution restrictions
- Tool-level authorization
- User approval before destructive operations
- Sandboxed code execution

---

## 8. 🖥️ Streamlit UI

Add a user-facing interface:

```text
┌─────────────────────────────────────────┐
│          Syntera AI Assistant       │
├─────────────────────────────────────────┤
│                                         │
│ User: Research RAG and implement it     │
│                                         │
│ AI: Researching...                      │
│                                         │
│ AI: Implementation complete...          │
│                                         │
├─────────────────────────────────────────┤
│ Ask something...                    ➤   │
└─────────────────────────────────────────┘
```

Potential UI features:

- Chat interface
- Session selector
- Conversation history
- Agent activity/status
- Tool-call visibility
- Research sources
- Code blocks
- File-operation status
- Clear conversation
- New conversation

---

## 9. 📡 Streaming Responses

Instead of waiting for the entire workflow:

```text
User
 ↓
Supervisor...
 ↓
Researching...
 ↓
Calling search tool...
 ↓
Analyzing results...
 ↓
Generating response...
```

Stream intermediate status and final tokens to the UI.

---

## 10. 📊 Observability

Expand logging into structured observability.

Track:

- Session ID
- Request ID
- Agent execution
- Tool calls
- MCP server
- Tool latency
- LLM latency
- Token usage
- Errors
- Retries
- Final response time

Potential future integrations:

- OpenTelemetry
- LangSmith
- Prometheus/Grafana
- Structured JSON logs

---

## 11. 🧪 Automated Evaluation

Introduce evaluation datasets for:

- Supervisor routing
- Research quality
- Tool selection
- Coding correctness
- Agent collaboration
- Final answer quality

Example:

```text
Input
  ↓
Expected Route
  ↓
Actual Route
  ↓
Pass/Fail
```

---

## 12. 🛡️ Reliability and Recovery

Future workflow should support:

- Tool retries
- LLM retries
- Timeout handling
- MCP reconnection
- Partial failure recovery
- Fallback models
- Maximum agent iterations
- Maximum tool calls
- Graceful workflow termination

---

## 13. 🔑 Authentication and Multi-User Support

For deployment:

- User authentication
- Session isolation
- Per-user conversation history
- API key management
- Role-based tool permissions
- Usage limits

---

## 14. 🌐 Production Deployment

Potential production architecture:

```text
                    ┌───────────────┐
                    │   Streamlit   │
                    │      UI       │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Agent Service │
                    │ LangGraph     │
                    └───────┬───────┘
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
             Database     MCP        LLM APIs
                │         Servers
                │
                ▼
             Sessions /
             Memory
```

Potential deployment targets:

- Docker
- Kubernetes
- Cloud VM/container platforms
- Managed databases
- Dedicated MCP services

---

# 🗺️ Suggested Upgrade Roadmap

### Phase 1 — Conversation

- [ ] Message history
- [ ] Session IDs
- [ ] Streamlit chat UI
- [ ] Persistent conversations

### Phase 2 — Agentic Behavior

- [ ] Coding Agent research requests
- [ ] Research → Coding → Research loops
- [ ] Agent iteration limits
- [ ] Better state schema
- [ ] Planning/decomposition

### Phase 3 — MCP Expansion

- [ ] Additional MCP servers
- [ ] MCP resources
- [ ] MCP prompts
- [ ] Authentication/authorization
- [ ] Tool permissions

### Phase 4 — Production Reliability

- [ ] Retries
- [ ] Timeouts
- [ ] Recovery
- [ ] Structured logging
- [ ] Observability
- [ ] Automated evaluation

### Phase 5 — Production Platform

- [ ] Multi-user authentication
- [ ] Persistent memory
- [ ] Database-backed sessions
- [ ] Sandboxed coding execution
- [ ] Docker deployment
- [ ] Production monitoring

---

## 📚 Detailed Architecture Documentation

The detailed technical architecture is maintained separately so that this README remains focused on the project purpose, setup, usage, current capabilities, and roadmap.

See:

**[`PROJECT_ARCHITECTURE.md`](PROJECT_ARCHITECTURE.md)**

It contains:

- Directory structure
- Agent responsibilities
- LangGraph workflow
- Pipeline architecture
- State schema
- MCP architecture
- MCP client/manager flow
- Tool discovery
- Agent interaction
- LLM architecture
- Current vs planned workflow
- Upgrade architecture

---

## 📊 Current Project Snapshot

| Component | Current |
|---|---|
| Agents | 4 |
| MCP Servers | 1 |
| Research MCP Tools | 6 |
| Coding Tools | 6 |
| Workflow | LangGraph |
| MCP Framework | FastMCP |
| MCP Transport | stdio |
| Local LLM | Ollama |
| Cloud LLM | Groq |
| UI | CLI; Streamlit extension |
| Sessions | Planned |
| Message History | Planned |
| Persistent Memory | Planned |
| Dynamic Agent Collaboration | Planned |
| Production Deployment | Planned |

---

## 🎯 Project Goal

The long-term goal is to evolve **Syntera AI** from a basic multi-agent workflow into a modular **Agentic AI platform** where:

- Agents specialize in different responsibilities.
- Agents can collaborate dynamically.
- MCP provides a standardized capability layer.
- Conversation state persists across interactions.
- Sessions isolate users and conversations.
- Tools are discovered and invoked dynamically.
- The system can research, code, validate, and iterate.
- The application can run locally or be deployed as a production service.

---

## 📄 Documentation

- [`README.md`](README.md) — Project overview, setup, usage, capabilities, and roadmap
- [`PROJECT_ARCHITECTURE.md`](PROJECT_ARCHITECTURE.md) — Detailed architecture and implementation documentation

---

## 📌 Status

**Current stage:** Multi-agent + MCP foundation

**Next major milestone:** Stateful conversational Agentic AI workflow with Streamlit UI and dynamic Coding ↔ Research collaboration.
