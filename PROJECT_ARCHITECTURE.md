# 🏗️ Project Architecture — Multi-Agent AI System

This document contains the detailed technical architecture of the project.

The `README.md` describes **what the project is and where it is going**.

This document describes **how the project currently works** and how the planned upgrades fit into the architecture.

---

# 1. System Overview

The system is a multi-agent application built around:

```text
Python
  │
  ├── LangChain
  │      └── Agent creation + tool integration
  │
  ├── LangGraph
  │      └── Workflow orchestration + state
  │
  ├── MCP / FastMCP
  │      └── External capability layer
  │
  └── Ollama / Groq
         └── LLM inference
```

The application currently contains four agents:

```text
Supervisor Agent
General Agent
Research Agent
Coding Agent
```

---

# 2. Directory Structure

```text
Multi-Agents/
│
├── agents/
│   ├── supervisor/
│   │   ├── agent.py
│   │   └── prompt.py
│   │
│   ├── general/
│   │   ├── agents.py
│   │   └── prompt.py
│   │
│   ├── research/
│   │   ├── agent.py
│   │   └── prompt.py
│   │
│   └── coding/
│       ├── agent.py
│       └── prompt.py
│
├── orchestrator/
│   ├── workflow.py
│   ├── nodes.py
│   └── routes.py
│
├── schemas/
│   ├── state.py
│   └── routing.py
│
├── mcp_client/
│   ├── client.py
│   ├── manager.py
│   └── langchain_adapters.py
│
├── mcp_servers/
│   └── research_server.py
│
├── tools/
│   └── coding/
│       ├── code_analysis.py
│       └── filesystem.py
│
├── config/
│   ├── settings.py
│   └── logging_config.py
│
├── models/
│   └── llm.py
│
├── logs/
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── workflow.png
├── README.md
└── PROJECT_ARCHITECTURE.md
```

---

# 3. Responsibility of Each Layer

## `agents/`

Contains agent definitions and prompts.

Agents should focus on **reasoning and task execution**, not workflow orchestration.

---

## `orchestrator/`

Contains LangGraph workflow logic.

Responsibilities:

- Define nodes
- Connect nodes
- Define conditional routing
- Execute the agent pipeline
- Coordinate state transitions

---

## `schemas/`

Contains structured data models.

Important schemas:

```text
AgentState
RoutingDecision
```

The state is the shared data passed through the LangGraph workflow.

---

## `mcp_client/`

Contains the application-side MCP infrastructure.

```text
client.py
    ↓
Low-level MCP communication

manager.py
    ↓
MCP server lifecycle + registration

langchain_adapters.py
    ↓
MCP tool → LangChain StructuredTool
```

---

## `mcp_servers/`

Contains MCP server implementations.

Current server:

```text
research_server.py
```

It exposes research capabilities using FastMCP.

---

## `tools/`

Contains tools that remain local to the application.

Current coding tools include:

- File listing
- File reading
- File writing
- File creation
- File appending
- Python AST analysis

---

## `models/`

Centralizes LLM configuration.

The system can select between:

```text
Ollama
   │
   └── Local inference

Groq
   │
   └── Cloud inference
```

---

# 4. Current Agent Architecture

```text
                         ┌─────────────────┐
                         │    User Query   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Supervisor    │
                         │      Agent      │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       ┌────────────┐      ┌────────────┐      ┌────────────┐
       │  General   │      │  Research  │      │   Coding   │
       │   Agent    │      │   Agent    │      │   Agent    │
       └────────────┘      └─────┬──────┘      └─────┬──────┘
                                 │                   │
                                 ▼                   ▼
                            MCP Tools           Local Tools
```

The Supervisor is responsible for **initial classification**, not for performing the actual specialist task.

---

# 5. Current LangGraph Pipeline

The current pipeline is:

```text
START
  │
  ▼
Supervisor
  │
  ├──────────────► General ──────────► END
  │
  ├──────────────► Research ─────────► END
  │                  |
  │                  ▼
  └──────────────► Coding ───────────► END
```

---

# 6. Workflow State

The current workflow uses a shared state object.

Conceptually:

```python
AgentState(
    user_query="...",
    supervisor_route="...",
    supervisor_route_rationale="...",
    general_result="...",
    research_result="...",
    coding_result="..."
)
```

The state allows nodes to exchange information without directly coupling the agent implementations.

---

# 7. Current Query Lifecycle

## Step 1 — User Input

```text
User
 ↓
main.py
```

The application receives a query.

---

## Step 2 — Workflow Invocation

```text
main.py
 ↓
LangGraph workflow
```

The workflow receives:

```python
{
    "user_query": query
}
```

---

## Step 3 — Supervisor

The Supervisor receives the query and produces a structured routing decision.

Conceptually:

```python
RoutingDecision(
    route="Research",
    rationale="The user is asking for external information."
)
```

---

## Step 4 — Conditional Routing

The LangGraph routing function reads:

```text
state.supervisor_route
```

and selects the corresponding node.

---

## Step 5 — Specialist Agent

The selected agent performs the actual task.

### General

```text
Query
 ↓
General LLM
 ↓
Response
```

### Research

```text
Query
 ↓
Research Agent
 ↓
MCP Tool
 ↓
MCP Server
 ↓
External Source
 ↓
Tool Result
 ↓
Research Agent
 ↓
Research Result
```

### Coding

```text
Query
 ↓
Coding Agent
 ↓
Local Coding Tools
 ↓
Code / File Operation / Analysis
 ↓
Coding Result
```

---

# 8. MCP Architecture

MCP is used as a capability layer.

```text
                     Research Agent
                            │
                            ▼
                  LangChain MCP Tools
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
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
       Search          Web Content        Academic
          │                 │                 │
          ▼                 ▼                 ▼
     DuckDuckGo          Webpage           arXiv

Additional capabilities:
    Google Search
    YouTube Search
    YouTube Transcript
```

---

# 9. MCP Client Flow

The application performs the following lifecycle:

```text
Application Start
       │
       ▼
Create MCPManager
       │
       ▼
Register Research MCP Server
       │
       ▼
Create MCPClient
       │
       ▼
Connect using stdio
       │
       ▼
List MCP Tools
       │
       ▼
Convert MCP tool schemas
       │
       ▼
Create LangChain StructuredTools
       │
       ▼
Inject tools into Research Agent
```

---

# 10. MCP Tool Invocation

When the Research Agent decides to use a tool:

```text
Research Agent
      │
      │ tool call
      ▼
LangChain StructuredTool
      │
      ▼
MCP Client
      │
      │ call_tool(...)
      ▼
MCP Server
      │
      ▼
Actual Python Function
      │
      ▼
External Service / Data Source
      │
      ▼
MCP Server Result
      │
      ▼
MCP Client
      │
      ▼
Research Agent
```

This separates:

```text
Reasoning
    from
Capability execution
```

---

# 11. Current MCP Research Tools

The current Research MCP Server exposes:

| Tool | Purpose |
|---|---|
| `duckduckgo_search` | General web search |
| `google_search` | Google Custom Search |
| `read_webpage` | Extract webpage content |
| `youtube_search` | Search YouTube |
| `youtube_transcript` | Retrieve video transcripts |
| `arxiv_search` | Search academic papers |

Credentials such as Google API credentials are configured server-side through application settings rather than being exposed as normal LLM tool arguments.

---

# 12. Coding Agent Architecture

The Coding Agent has two distinct modes.

## Code Generation

If the user asks:

```text
Give me a Python implementation of X.
```

the agent generates the code in the response.

It does **not** automatically create a file.

---

## File Operation

If the user explicitly asks:

```text
Create app.py with this implementation.
```

the agent can use:

```text
create_file
```

or:

```text
write_file
```

This distinction prevents a simple code-generation request from causing unexpected filesystem changes.

---

# 13. Coding Tools

Current local tools:

```text
list_files
read_files
write_file
create_file
append_to_file
analyze_python_file
```

The tools allow the Coding Agent to inspect and modify a project when the user explicitly requests those operations.

---

# 14. LLM Architecture

The project supports local and cloud inference.

```text
                    Agent
                      │
                      ▼
               LLM Configuration
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
          Ollama              Groq
        Local LLM          Cloud LLM
```

Each agent can have its own model configuration:

```text
Supervisor Model
General Model
Research Model
Coding Model
```

This allows future optimization such as:

```text
Supervisor → small/fast model
General    → small model
Research   → reasoning model
Coding     → coding-capable model
```

---

# 15. Logging

The project includes logging across the application.

Important events include:

```text
Application startup
Agent initialization
MCP server initialization
Tool discovery
MCP tool calls
Tool results
Errors
Workflow execution
Application shutdown
```

A useful future improvement is to attach:

```text
session_id
request_id
agent_id
tool_name
timestamp
latency
```

to every relevant log entry.

---

# 16. Current Limitations

The current architecture is intentionally a foundation.

Important limitations:

1. Conversation history is not yet persistent.
2. Sessions are not explicitly managed.
3. Each query is largely treated as an independent workflow execution.
4. Supervisor performs initial routing only.
5. Dynamic Coding → Research collaboration is not yet implemented.
6. Long-running memory is not implemented.
7. Tool authorization is limited.
8. Coding execution sandboxing is not implemented.
9. Streamlit UI is an extension rather than the core runtime.
10. Automated evaluation is limited.
11. Production-grade authentication is not implemented.

---

# 17. Upgrade Architecture

The planned architecture evolves from:

```text
User
 ↓
Supervisor
 ↓
One Specialist
 ↓
Response
```

to:

```text
                         User
                          │
                          ▼
                     Session Layer
                          │
                          ▼
                     Conversation
                        State
                          │
                          ▼
                     Supervisor
                          │
                          ▼
                      Planner
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          Research      Coding       General
             │            │
             │            │
             └──────┬─────┘
                    │
                    ▼
              Shared State
                    │
                    ▼
               Validation
                    │
                    ▼
               Final Answer
```

---

# 18. Future Coding ↔ Research Loop

One of the most important planned upgrades is removing the fixed assumption:

```text
Supervisor → Research → Coding
```

and instead allowing:

```text
Supervisor
    │
    ▼
Coding Agent
    │
    ├── Enough information?
    │        │
    │       YES
    │        │
    │        ▼
    │      Code
    │
    └── NO
         │
         ▼
    Research Request
         │
         ▼
    Research Agent
         │
         ▼
    Research Result
         │
         ▼
    Coding Agent
         │
         ▼
      Code
```

The Coding Agent should be able to determine:

```text
CONTINUE
RESEARCH
FINISH
```

A future structured decision could be:

```python
class CodingDecision(BaseModel):
    action: Literal["continue", "research", "finish"]
    research_query: str | None = None
    reason: str
```

---

# 19. Future Iterative Workflow

The future graph may look like:

```text
START
  │
  ▼
Supervisor
  │
  ▼
Coding
  │
  ├── continue ───────► Coding
  │
  ├── research ───────► Research
  │                         │
  │                         ▼
  │                       Coding
  │
  └── finish ──────────► END
```

To prevent infinite loops, the state should contain controls such as:

```text
iteration_count
max_iterations
research_count
max_research_requests
```

---

# 20. Message History Upgrade

Future state:

```text
AgentState
│
├── session_id
├── user_query
├── messages[]
├── current_task
├── supervisor_decision
├── research_result
├── coding_result
├── tool_calls[]
└── iteration_count
```

Instead of storing only the latest query, the system will maintain conversation messages.

---

# 21. Session Architecture

A session should become the top-level boundary for a conversation.

```text
Session
│
├── session_id
├── user_id
├── created_at
├── updated_at
│
├── messages
├── workflow state
├── memory
└── metadata
```

Potential storage:

```text
Development:
    SQLite

Production:
    PostgreSQL

Fast temporary state/cache:
    Redis
```

---

# 22. Memory Architecture

Memory should be separated into two categories.

### Short-Term Memory

Used for the current conversation:

```text
Recent messages
Current task
Current agent state
Current research
Current coding context
```

### Long-Term Memory

Used across conversations:

```text
User preferences
Project context
Previous decisions
Important persistent information
```

A retrieval layer can be introduced for long-term semantic memory where required.

---

# 23. Streamlit Architecture

The UI should sit above the application/workflow layer.

```text
                 Streamlit UI
                      │
                      ▼
               Application Layer
                      │
                      ▼
                LangGraph
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Agents       State        MCP
```

The UI should not contain the agent logic.

Recommended responsibilities:

```text
app.py
    ↓
User interaction

Application/service layer
    ↓
Session + workflow lifecycle

LangGraph
    ↓
Agent orchestration

Agents
    ↓
Reasoning

MCP
    ↓
External capabilities
```

---

# 24. Observability Upgrade

A production-oriented request should have a trace:

```text
Request
 │
 ├── Supervisor
 │     └── latency
 │
 ├── Research Agent
 │     ├── MCP Tool
 │     ├── MCP Tool
 │     └── latency
 │
 ├── Coding Agent
 │     └── tool calls
 │
 └── Final Response
```

A future `request_id` can connect all events.

---

# 25. Security Upgrade

As the system gains more tools, security becomes increasingly important.

Potential controls:

```text
User
 │
 ▼
Authentication
 │
 ▼
Authorization
 │
 ▼
Agent
 │
 ▼
Tool Permission Check
 │
 ▼
MCP / Local Tool
```

For coding capabilities:

- Restrict filesystem roots
- Prevent path traversal
- Separate read/write permissions
- Require approval for destructive operations
- Sandbox code execution
- Restrict shell access
- Apply resource/time limits

---

# 26. Testing Strategy

Testing should eventually be divided into:

```text
Unit Tests
    ↓
Tool Tests
    ↓
Agent Tests
    ↓
MCP Integration Tests
    ↓
Workflow Tests
    ↓
End-to-End Tests
    ↓
Evaluation Tests
```

Example evaluation dimensions:

```text
Routing accuracy
Tool selection
Research relevance
Research grounding
Code correctness
Agent collaboration
Final response quality
```

---

# 27. Target Architecture

The longer-term architecture can become:

```text
                              ┌───────────────┐
                              │   Streamlit   │
                              │      UI       │
                              └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ Session Layer │
                              └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ Conversation  │
                              │    Memory     │
                              └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │  Supervisor   │
                              └───────┬───────┘
                                      │
                                      ▼
                                ┌───────────┐
                                │  Planner  │
                                └─────┬─────┘
                                      │
                         ┌────────────┼────────────┐
                         ▼            ▼            ▼
                     Research      Coding       General
                         │            │
                         └──────┬─────┘
                                │
                                ▼
                          Shared State
                                │
                                ▼
                            Validator
                                │
                                ▼
                           Final Answer

              ┌─────────────────────────────────────┐
              │              MCP Layer              │
              │                                     │
              │ Research │ GitHub │ DB │ Browser  │
              │ Filesystem │ Docs │ Other Tools   │
              └─────────────────────────────────────┘
```

---

# 28. Architectural Principles

The project should continue following these principles:

### Separation of Concerns

Agents reason.

Orchestrator controls workflow.

MCP provides capabilities.

Tools execute actions.

State carries context.

UI handles interaction.

---

### Explicit State

Important information should be represented in structured state rather than hidden inside prompts.

---

### Controlled Agent Autonomy

Agents should be capable of making decisions, but with:

- iteration limits
- tool permissions
- timeouts
- validation
- clear termination conditions

---

### Capability Decoupling

MCP tools should remain independent from the reasoning logic of individual agents.

---

### Observability by Default

Agent and tool behavior should be traceable through logs and future distributed tracing.

---

### Incremental Evolution

The architecture should support adding:

```text
New Agent
New MCP Server
New Tool
New Model
New UI
New Memory Backend
```

without rewriting the entire system.

---

# 29. Current → Future Evolution

```text
CURRENT

User
 ↓
Supervisor
 ↓
Specialist Agent
 ↓
Result


NEXT

User
 ↓
Session
 ↓
Supervisor
 ↓
Coding / Research / General
 ↓
Shared State
 ↓
Result


FUTURE

User
 ↓
Session + Memory
 ↓
Supervisor
 ↓
Planner
 ↓
Agent Collaboration
 ↓
MCP Capabilities
 ↓
Validation
 ↓
Iterative Execution
 ↓
Final Response
```

---

# 30. Documentation Ownership

Keep documentation responsibilities separate:

```text
README.md
    ↓
What the project is
How to install it
How to run it
Current features
Examples
Roadmap
Upgrade scope

PROJECT_ARCHITECTURE.md
    ↓
How the system works
Directory structure
Agent architecture
Workflow
State
MCP
Pipeline
Current limitations
Target architecture
```

This prevents the README from becoming a large implementation document as the project grows.
