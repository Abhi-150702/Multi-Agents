# 🤖 Multi-Agent AI System with MCP Integration

## 📋 Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Key Features](#key-features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Application Flow](#application-flow)
- [Agents Deep Dive](#agents-deep-dive)
- [MCP Architecture](#mcp-architecture)
- [Tools & Capabilities](#tools--capabilities)
- [Routing & Orchestration](#routing--orchestration)
- [State Management](#state-management)
- [LLM Configuration](#llm-configuration)
- [Testing](#testing)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This is a **production-ready Multi-Agent AI System** built with **LangChain**, **LangGraph**, and **Model Context Protocol (MCP)** that provides **four specialized AI agents orchestrated by an intelligent supervisor**:

### The Four Agents

1. **Supervisor Agent** 🧠
   - Analyzes user queries and intelligently routes to appropriate specialist agents
   - Makes routing decisions: General, Research, Coding, or ResearchAndCoding
   - Provides reasoning for each routing decision

2. **General Agent** 💬
   - Handles general conversational queries
   - No specialized tools required
   - For simple Q&A and general assistance

3. **Research Agent** 🔍
   - Conducts comprehensive research using MCP-based tools
   - Accesses: web search, academic papers, GitHub, YouTube transcripts, and more
   - 7 specialized research tools exposed via MCP server

4. **Coding Agent** 💻
   - Assists with software development tasks
   - Code analysis, file operations, and code generation
   - 6 file system and analysis tools
   - Can incorporate research results when using ResearchAndCoding route

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Query Input                        │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
              ┌────────────────────────┐
              │   Supervisor Agent     │  ← Analyzes & Routes
              │  (Intelligent Router)  │
              └────────┬───────────────┘
                       │
         ┌─────────────┼──────────────┬───────────────┐
         │             │              │               │
         ↓             ↓              ↓               ↓
    [General]    [Research]      [Coding]    [ResearchAndCoding]
         │             │              │               │
         ↓             ↓              ↓               ↓
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │  General    │ │  Research   │ │   Coding    │ │  Research   │
  │   Agent     │ │   Agent     │ │   Agent     │ │   Agent     │
  │ (No Tools)  │ │ (7 MCP      │ │ (6 Tools)   │ │             │
  │             │ │  Tools)     │ │             │ │             │
  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
         │               │               │               │
         ↓               ↓               ↓               ↓
       [END]           [END]           [END]       ┌─────────────┐
                                                   │   Coding    │
                                                   │   Agent     │
                                                   │  (receives  │
                                                   │  research)  │
                                                   └──────┬──────┘
                                                          ↓
                                                        [END]

┌───────────────────────────────────────────────────────────────┐
│                      MCP Architecture                          │
├───────────────────────────────────────────────────────────────┤
│  MCP Manager                                                   │
│  ├── Research MCP Server (mcp_servers/research_server.py)     │
│  │   └── Exposes 7 Research Tools                            │
│  │                                                             │
│  └── MCP Client (mcp_client/)                                 │
│      ├── client.py         - MCP server communication         │
│      ├── manager.py        - Server lifecycle management      │
│      └── langchain_adapters.py - Tool conversion             │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│                    LLM Configuration                           │
├───────────────────────────────────────────────────────────────┤
│  Primary: Ollama (Local)     Fallback: Groq (Cloud)          │
│  ├── Supervisor Model        ├── Supervisor Model            │
│  ├── General Model           ├── General Model               │
│  ├── Research Model          ├── Research Model              │
│  └── Coding Model            └── Coding Model                │
│                                                               │
│  Auto-fallback if Ollama unavailable                         │
└───────────────────────────────────────────────────────────────┘
```

---

## 🌟 Key Features

### Core Features
- 🤖 **4 Specialized Agents** (Supervisor, General, Research, Coding)
- 🎯 **Intelligent Routing** - Supervisor analyzes queries and routes optimally
- 🔌 **MCP Integration** - Modular tool architecture via Model Context Protocol
- 🔄 **Dual LLM Support** - Ollama (local) primary with Groq (cloud) fallback
- 📊 **Research Tools** - 7 MCP-based tools (DuckDuckGo, Google, arXiv, YouTube, etc.)
- 💻 **Coding Tools** - 6 file system and analysis tools
- 🎨 **LangGraph Orchestration** - Conditional routing with state management
- 📝 **Comprehensive Logging** - Full visibility into all operations
- ⚡ **Async Architecture** - Efficient async/await implementation
- 🔧 **Flexible Configuration** - Environment-based settings with Pydantic
- 📸 **Workflow Visualization** - Auto-generated workflow diagrams
- 🛠️ **Modular Design** - Easy to extend and customize

### Advanced Features
- **Lazy Agent Initialization** - Agents created on-demand or at startup
- **Error Resilience** - Graceful fallback mechanisms
- **State Persistence** - Track query flow and results across agents
- **Structured Output** - Type-safe routing decisions with Pydantic
- **Command-line Interface** - Support for runtime configuration flags
- **Tool Discovery** - Dynamic tool registration via MCP

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Groq API key (for cloud LLM fallback)
- Optional: Ollama installed locally (for local LLM execution)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Multi-Agents
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv .venv

   # On Windows
   .venv\Scripts\activate

   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Environment File**
   ```bash
   # Create .env file in project root
   touch .env  # Linux/Mac
   type nul > .env  # Windows
   ```

5. **Configure Environment Variables**
   Edit `.env` file:
   ```env
   # ============================================================
   # Groq Configuration (Cloud LLM - Fallback)
   # ============================================================
   GROQ_API_KEY=your_groq_api_key_here
   SUPERVISOR_MODEL=llama-3.3-70b-versatile
   GENERAL_MODEL=llama-3.3-70b-versatile
   RESEARCH_MODEL=llama-3.3-70b-versatile
   CODING_MODEL=llama-3.3-70b-versatile

   # ============================================================
   # Ollama Configuration (Local LLM - Primary)
   # ============================================================
   OLLAMA_BASE_URL=http://localhost:11434
   SUPERVISOR_OLLAMA_MODEL=llama3.2:latest
   GENERAL_OLLAMA_MODEL=llama3.2:latest
   RESEARCH_OLLAMA_MODEL=llama3.2:latest
   CODING_OLLAMA_MODEL=llama3.2:latest

   # ============================================================
   # Google Search (Optional)
   # ============================================================
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_custom_search_engine_id
   ```

6. **Install Ollama** (Optional - for local LLM)
   ```bash
   # Visit https://ollama.ai and install
   # Then pull models:
   ollama pull llama3.2:latest
   ```

---

## ⚙️ Configuration

### Environment Variables

The system uses Pydantic Settings for configuration management. All settings are loaded from `.env` file:

| Variable | Purpose | Required |
|----------|---------|----------|
| `GROQ_API_KEY` | Groq API authentication | Yes |
| `GOOGLE_API_KEY` | Google Search API | No |
| `GOOGLE_CSE_ID` | Google Custom Search Engine ID | No |
| `SUPERVISOR_MODEL` | Groq model for supervisor | Yes |
| `GENERAL_MODEL` | Groq model for general agent | Yes |
| `RESEARCH_MODEL` | Groq model for research agent | Yes |
| `CODING_MODEL` | Groq model for coding agent | Yes |
| `OLLAMA_BASE_URL` | Ollama server URL | No |
| `SUPERVISOR_OLLAMA_MODEL` | Ollama model for supervisor | No |
| `GENERAL_OLLAMA_MODEL` | Ollama model for general | No |
| `RESEARCH_OLLAMA_MODEL` | Ollama model for research | No |
| `CODING_OLLAMA_MODEL` | Ollama model for coding | No |

### LLM Provider Selection

**Use Ollama (Local)**:
```bash
python main.py --use-ollama
```

**Use Groq (Cloud) - Default**:
```bash
python main.py
```

The system will automatically fall back to Groq if Ollama is unavailable.

### Logging Configuration

Customize in `config/logging_config.py`:
- Console log level (default: INFO)
- File log level (default: DEBUG)
- Log directory location
- Log file format and rotation

---

## 🚀 Usage

### Running the Application

**Basic Usage (Groq)**:
```bash
python main.py
```

**With Ollama (Local LLM)**:
```bash
python main.py --use-ollama
```

**Interactive Session**:
```
Starting Multi-Agent Application...
Use Ollama: False
=============================================================
Initializing MCP Servers...
=============================================================
Research MCP Server initialized successfully!
[1/4] Initializing Supervisor Agent...
[1/4] Supervisor Agent initialized successfully!
[2/4] Initializing General Agent...
[2/4] General Agent initialized successfully!
[3/4] Initializing Research Agent...
Discovered 7 MCP tools for Research Agent.
[3/4] Research Agent initialized successfully!
[4/4] Initializing Coding Agent...
[4/4] Coding Agent initialized successfully!
All agents initialized successfully!
Application ready to accept queries!


User Query: What are the latest AI trends in 2024?
```

### Example Queries

**General Queries** (Routes to General Agent):
```
What is the capital of France?
Explain the concept of machine learning
What is the difference between AI and ML?
```

**Research Queries** (Routes to Research Agent):
```
Find recent papers on transformer models
Search for Python web scraping tutorials on YouTube
What are the latest AI trends according to arXiv papers?
Find GitHub repositories for building chatbots
```

**Coding Queries** (Routes to Coding Agent):
```
List all Python files in the current directory
Analyze the structure of main.py
Read the contents of config/settings.py
Create a new Python file with a basic class structure
```

**Combined Queries** (Routes to Research then Coding):
```
Research LangChain best practices and create a sample agent
Find arXiv papers on RAG and implement a basic version
Search for FastAPI tutorials and create a basic API structure
```

### Exit the Application
```
User Query: exit
# or
User Query: quit
```

---

## 📁 Project Structure

```
Multi-Agents/
│
├── 📁 agents/                          # Agent configurations
│   ├── 📁 supervisor/                 # Supervisor agent
│   │   ├── agent.py                   # Agent initialization
│   │   └── prompt.py                  # System prompt for routing
│   ├── 📁 general/                    # General agent
│   │   ├── agents.py                  # Agent initialization
│   │   └── prompt.py                  # System prompt
│   ├── 📁 coding/                     # Coding agent
│   │   ├── agent.py                   # Agent initialization
│   │   └── prompt.py                  # System prompt
│   └── 📁 research/                   # Research agent
│       ├── agent.py                   # Agent initialization
│       └── prompt.py                  # System prompt
│
├── 📁 orchestrator/                    # LangGraph workflow
│   ├── workflow.py                    # Graph definition & compilation
│   ├── nodes.py                       # Node implementations (agent calls)
│   └── routes.py                      # Routing logic & conditions
│
├── 📁 schemas/                         # Data structures
│   ├── state.py                       # AgentState (workflow state)
│   └── routing.py                     # RoutingDecision schema
│
├── 📁 config/                          # Configuration
│   ├── settings.py                    # Environment variables (Pydantic)
│   └── logging_config.py              # Logging setup
│
├── 📁 models/                          # LLM configurations
│   └── llm.py                         # Ollama + Groq LLM setup
│
├── 📁 mcp_client/                      # MCP client infrastructure
│   ├── client.py                      # MCP server communication
│   ├── manager.py                     # Server lifecycle management
│   └── langchain_adapters.py          # Convert MCP tools to LangChain
│
├── 📁 mcp_servers/                     # MCP server implementations
│   └── research_server.py             # Research tools MCP server
│
├── 📁 tools/                           # Tool implementations
│   ├── 📁 coding/
│   │   ├── code_analysis.py          # Python AST analysis
│   │   └── filesystem.py             # File operations (read, write, list)
│   └── 📁 research/
│       ├── 📁 academic/
│       │   └── arxiv.py              # arXiv search (deprecated - now in MCP)
│       ├── 📁 code/
│       │   └── github.py             # GitHub search (deprecated - now in MCP)
│       └── 📁 web/
│           ├── duckduckgo_search.py  # DuckDuckGo (deprecated - now in MCP)
│           ├── google_search.py      # Google search (deprecated - now in MCP)
│           ├── webpage.py            # Web scraping (deprecated - now in MCP)
│           ├── youtube.py            # YouTube search (deprecated - now in MCP)
│           └── youtube_transcripts.py # Transcripts (deprecated - now in MCP)
│
├── 📁 logs/                            # Auto-generated logs
│   └── tools_YYYYMMDD_HHMMSS.log     # Timestamped log files
│
├── 📁 .codemie/                        # CodeMie IDE configurations
│   └── 📁 virtual_assistants/
│       └── *.yaml                     # Assistant configurations
│
├── 📄 main.py                          # Main entry point
├── 📄 requirements.txt                 # Python dependencies
├── 📄 .env                             # Environment variables (create this)
├── 📄 .gitignore                       # Git ignore rules
├── 📄 workflow.png                     # Auto-generated workflow diagram
│
└── 📚 README.md                        # This file
```

### Key Files Explained

#### 1. `main.py` - Application Entry Point
- Parses command-line arguments (`--use-ollama`)
- Initializes MCP Manager and registers MCP servers
- Initializes all agents at startup
- Creates and compiles LangGraph workflow
- Generates workflow visualization (workflow.png)
- Runs interactive query loop
- Handles graceful shutdown

#### 2. `orchestrator/workflow.py` - Workflow Definition
- Defines LangGraph StateGraph with AgentState
- Adds nodes: Supervisor, General, Researcher, Coder
- Configures conditional routing from Supervisor
- Configures conditional routing after Research
- Compiles the executable workflow

#### 3. `orchestrator/nodes.py` - Node Implementations
- Agent caching for performance
- `initialize_agents()` - Initializes all agents at startup
- `supervisor_node()` - Calls supervisor for routing decision
- `general_node()` - Handles general queries
- `research_node()` - Performs research
- `coding_node()` - Handles coding tasks (with optional research context)

#### 4. `orchestrator/routes.py` - Routing Logic
- `route_from_supervisor()` - Routes based on supervisor decision
- `route_after_research()` - Determines next step after research
- `get_supervisor_routes()` - Maps routes to nodes
- `get_research_coder_routes()` - Maps research completion to next node

#### 5. `schemas/state.py` - Workflow State
Defines `AgentState` with:
- `user_query` - Original user input
- `supervisor_route` - Routing decision (General/Research/Coding/ResearchAndCoding)
- `supervisor_route_rationale` - Reasoning for the route
- `general_result` - Output from general agent
- `research_result` - Output from research agent
- `coding_result` - Output from coding agent

#### 6. `mcp_servers/research_server.py` - Research MCP Server
Exposes 7 research tools via MCP:
- `duckduckgo_search` - Web search
- `google_search` - Google search
- `read_webpage` - Extract webpage content
- `youtube_search` - Search YouTube videos
- `youtube_transcript` - Get video transcripts
- `arxiv_search` - Search academic papers

---

## 🔄 Application Flow

### Complete Execution Flow

```
1. Application Startup
   ├── Parse command-line arguments (--use-ollama)
   ├── Load configuration from .env (Settings)
   ├── Initialize MCP Manager
   ├── Register Research MCP Server
   │   └── Discover 7 research tools
   ├── Initialize all agents
   │   ├── Supervisor Agent (no tools)
   │   ├── General Agent (no tools)
   │   ├── Research Agent (7 MCP tools)
   │   └── Coding Agent (6 local tools)
   ├── Create LangGraph workflow
   │   ├── Add nodes (Supervisor, General, Researcher, Coder)
   │   ├── Add conditional edges
   │   └── Compile graph
   ├── Generate workflow visualization (workflow.png)
   └── Enter interactive query loop

2. Query Processing
   User enters query
   ↓
   Workflow invokes START
   ↓
   [Supervisor Node]
   ├── Receives: user_query
   ├── Analyzes query with Supervisor LLM
   ├── Outputs: RoutingDecision
   │   ├── route: "General" | "Research" | "Coding" | "ResearchAndCoding"
   │   └── rationale: "Reasoning for this route"
   └── Updates state:
       ├── supervisor_route
       └── supervisor_route_rationale
   ↓
   [Conditional Routing from Supervisor]
   ├── If "General" → General Node → END
   ├── If "Research" → Researcher Node → END
   ├── If "Coding" → Coder Node → END
   └── If "ResearchAndCoding" → Researcher Node → Coder Node → END

3. Agent Execution

   [General Agent Path]
   └── No tools, just conversational response
       └── Updates state.general_result
           └── END

   [Research Agent Path]
   ├── Receives: user_query
   ├── Uses 7 MCP tools
   │   ├── duckduckgo_search
   │   ├── google_search
   │   ├── read_webpage
   │   ├── youtube_search
   │   ├── youtube_transcript
   │   └── arxiv_search
   ├── Synthesizes research results
   └── Updates state.research_result
       └── If supervisor_route == "ResearchAndCoding"
           └── Go to Coder Node
       └── Else
           └── END

   [Coding Agent Path]
   ├── Receives: user_query + (optional) research_result
   ├── If research_result exists:
   │   └── Constructs prompt combining research + coding task
   ├── Uses 6 coding tools
   │   ├── list_files
   │   ├── read_files
   │   ├── write_file
   │   ├── create_file
   │   ├── append_to_file
   │   └── analyze_python_file
   ├── Generates code or performs file operations
   └── Updates state.coding_result
       └── END

4. Response Return
   ├── Workflow returns final state
   ├── main.py extracts appropriate result:
   │   ├── general_result (if General path)
   │   ├── research_result (if Research path)
   │   └── coding_result (if Coding or ResearchAndCoding path)
   └── Display result to user

5. Loop or Exit
   ├── Wait for next query
   └── Or exit on "exit"/"quit"
       └── Disconnect MCP servers
           └── Shutdown gracefully
```

---

## 🤖 Agents Deep Dive

### 1. Supervisor Agent

**Purpose**: Intelligent query routing

**Location**: `agents/supervisor/agent.py`

**System Prompt**: `agents/supervisor/prompt.py`

**Tools**: None (decision-making only)

**LLM**: `get_supervisor_llm()` - Ollama primary, Groq fallback

**Output Format**: Structured `RoutingDecision`
```python
class RoutingDecision(BaseModel):
    route: Literal["General", "Research", "Coding", "ResearchAndCoding"]
    rationale: str
```

**Routing Logic**:
- **"General"** - Simple conversational queries, no tools needed
- **"Research"** - Information gathering, web search, academic papers
- **"Coding"** - File operations, code analysis, code generation
- **"ResearchAndCoding"** - Research first, then use results in coding

**Example Decisions**:
```
Query: "What is Python?" → Route: "General"
Query: "Find papers on transformers" → Route: "Research"
Query: "Create a Flask API" → Route: "Coding"
Query: "Research FastAPI best practices and create an API" → Route: "ResearchAndCoding"
```

---

### 2. General Agent

**Purpose**: Handle general conversational queries

**Location**: `agents/general/agents.py`

**System Prompt**: `agents/general/prompt.py`

**Tools**: None

**LLM**: `get_general_llm()` - Ollama primary, Groq fallback

**Use Cases**:
- General Q&A
- Simple explanations
- Conversational responses
- No tool invocation needed

**Example Queries**:
```
"What is machine learning?"
"Explain object-oriented programming"
"What's the difference between Python and JavaScript?"
```

---

### 3. Research Agent

**Purpose**: Comprehensive research using multiple sources

**Location**: `agents/research/agent.py`

**System Prompt**: `agents/research/prompt.py`

**Tools**: 7 MCP-based research tools

**LLM**: `get_research_llm()` - Ollama primary, Groq fallback

**Tool Discovery**:
```python
# Tools are discovered from MCP server at runtime
mcp_tools = await mcp_manager.get_tools("research")
# Returns 7 LangChain-compatible tools
```

**Research Strategy**:
1. Analyze query to determine information needs
2. Select appropriate tools (web, academic, video, etc.)
3. Execute searches and retrieve information
4. Cross-reference multiple sources
5. Synthesize comprehensive answer
6. Preserve source URLs and citations

**Example Queries**:
```
"Find recent arXiv papers on RAG systems"
"Search YouTube for LangChain tutorials"
"What are the best Python web scraping libraries?"
"Find GitHub repositories for building chatbots"
```

---

### 4. Coding Agent

**Purpose**: Software development assistance

**Location**: `agents/coding/agent.py`

**System Prompt**: `agents/coding/prompt.py`

**Tools**: 6 file system and code analysis tools

**LLM**: `get_coding_llm()` - Ollama primary, Groq fallback

**Tools**:
1. `list_files` - List directory contents
2. `read_files` - Read file contents (up to 100KB)
3. `write_file` - Write/overwrite files
4. `create_file` - Create new files
5. `append_to_file` - Append to existing files
6. `analyze_python_file` - Python AST analysis

**Special Feature - Research Integration**:
When route is "ResearchAndCoding":
```python
# Coding agent receives research context
prompt = f"""
User request:
{state.user_query}

Research performed by the Research Agent:
{state.research_result}

Using the research above, complete the user's coding request.
"""
```

**Example Queries**:
```
"List all Python files in the agents directory"
"Read and explain the main.py file"
"Create a new FastAPI application file"
"Analyze the structure of orchestrator/workflow.py"
```

---

## 🔌 MCP Architecture

### What is MCP (Model Context Protocol)?

MCP is a protocol for exposing tools and resources to LLM applications. It provides:
- **Modular tool architecture** - Tools as independent servers
- **Dynamic discovery** - Tools discovered at runtime
- **Language-agnostic** - MCP servers can be in any language
- **Scalable** - Add new tool servers without modifying core code

### Components

#### 1. MCP Manager (`mcp_client/manager.py`)
Central hub for managing MCP servers:
```python
class MCPManager:
    async def register_server(server_name, server_path)
        # Connect to MCP server
    
    async def get_tools(server_name)
        # Get LangChain tools from server
    
    async def disconnect()
        # Clean shutdown
```

**Usage in main.py**:
```python
mcp_manager = MCPManager()
await mcp_manager.register_server(
    server_name="research",
    server_path="mcp_servers/research_server.py"
)
```

#### 2. MCP Client (`mcp_client/client.py`)
Low-level communication with MCP servers:
```python
class MCPClient:
    async def connect()
        # Establish connection
    
    async def list_tools()
        # Discover available tools
    
    async def call_tool(tool_name, arguments)
        # Execute tool
    
    async def disconnect()
        # Close connection
```

#### 3. LangChain Adapters (`mcp_client/langchain_adapters.py`)
Converts MCP tools to LangChain format:
```python
async def get_langchain_tools(mcp_client):
    # Discover MCP tools
    # Convert to LangChain tool format
    # Return list of LangChain tools
```

#### 4. Research MCP Server (`mcp_servers/research_server.py`)
FastMCP-based server exposing 7 research tools:

**Initialization**:
```python
from fastmcp import FastMCP

mcp = FastMCP("Research Server")

@mcp.tool
def duckduckgo_search(query: str, max_results: int = 5) -> str:
    # Implementation
    pass

# ... more tools

if __name__ == "__main__":
    mcp.run()
```

**Exposed Tools**:
1. `duckduckgo_search` - Web search without API key
2. `google_search` - Google Custom Search (requires API key)
3. `read_webpage` - Extract webpage content with BeautifulSoup
4. `youtube_search` - Search YouTube videos with yt-dlp
5. `youtube_transcript` - Get video transcripts
6. `arxiv_search` - Search academic papers

### MCP Server Lifecycle

```
Application Start
↓
MCPManager created
↓
Register Research Server
├── MCPClient connects to research_server.py
├── Server starts (FastMCP)
├── Discover available tools
└── Convert to LangChain tools
↓
Research Agent initialized with MCP tools
↓
[During queries]
├── Agent decides to use tool
├── LangChain calls MCP tool
├── MCPClient.call_tool()
├── MCP Server executes tool
├── Result returned to agent
└── Agent continues reasoning
↓
Application Shutdown
└── mcp_manager.disconnect()
    └── All MCP servers shutdown gracefully
```

---

## 🛠️ Tools & Capabilities

### Research Tools (7 MCP Tools)

#### 1. **duckduckgo_search**
- **Purpose**: General web search (no API key required)
- **Parameters**: 
  - `query` (str) - Search query
  - `max_results` (int) - Number of results (default: 5)
- **Returns**: Formatted results with title, URL, snippet
- **Use Case**: Current information, general web search

#### 2. **google_search**
- **Purpose**: Google Custom Search
- **Parameters**: 
  - `query` (str) - Search query
  - `num_results` (int) - Number of results (default: 5)
- **Returns**: Google search results
- **Requires**: `GOOGLE_API_KEY`, `GOOGLE_CSE_ID`
- **Use Case**: Authoritative sources, official documentation

#### 3. **read_webpage**
- **Purpose**: Extract text content from webpages
- **Parameters**:
  - `url` (str) - Full HTTP/HTTPS URL
  - `max_characters` (int) - Max content length (default: 5000)
- **Returns**: JSON with URL and extracted content
- **Features**: 
  - Removes scripts, styles, navigation
  - Focuses on main content
  - Handles HTML parsing with BeautifulSoup
- **Use Case**: Deep content extraction, article reading

#### 4. **youtube_search**
- **Purpose**: Search YouTube videos
- **Parameters**:
  - `query` (str) - Search query
  - `max_results` (int) - Number of videos (default: 5)
- **Returns**: JSON array with video title, URL, channel, duration, views
- **Uses**: yt-dlp library
- **Use Case**: Video tutorials, demonstrations

#### 5. **youtube_transcript**
- **Purpose**: Extract video transcripts
- **Parameters**:
  - `video_url` (str) - YouTube URL or video ID
  - `max_characters` (int) - Max transcript length (default: 5000)
- **Returns**: JSON with video_id, full transcript, timed segments
- **Uses**: youtube_transcript_api
- **Use Case**: Video content analysis, lecture transcription

#### 6. **arxiv_search**
- **Purpose**: Search academic papers on arXiv
- **Parameters**:
  - `query` (str) - Search query
  - `top_k_results` (int) - Number of results (default: 5)
  - `load_max_docs` (int) - Max documents to load (default: 5)
- **Returns**: Paper titles, abstracts, authors, URLs
- **Uses**: LangChain ArxivAPIWrapper
- **Use Case**: Academic research, scientific papers

### Coding Tools (6 Local Tools)

#### 1. **list_files**
- **Purpose**: List directory contents
- **Parameters**: 
  - `directory` (str) - Path (default: ".")
- **Returns**: Formatted list with [DIR] and [FILE] prefixes
- **Use Case**: Explore project structure

#### 2. **read_files**
- **Purpose**: Read file contents
- **Parameters**: 
  - `file_path` (str) - Path to file
- **Returns**: File content as string
- **Limits**: 100KB max file size
- **Encoding**: UTF-8 with error replacement
- **Use Case**: Inspect source code, configuration files

#### 3. **write_file**
- **Purpose**: Write/overwrite file
- **Parameters**:
  - `file_path` (str) - Path to file
  - `content` (str) - Content to write
- **Creates**: Parent directories if needed
- **Use Case**: Save generated code, update files

#### 4. **create_file**
- **Purpose**: Create new file (error if exists)
- **Parameters**:
  - `file_path` (str) - Path to file
  - `content` (str) - Content to write
- **Safety**: Won't overwrite existing files
- **Use Case**: Create new source files

#### 5. **append_to_file**
- **Purpose**: Append content to existing file
- **Parameters**:
  - `file_path` (str) - Path to file
  - `content` (str) - Content to append
- **Use Case**: Add to logs, append to files

#### 6. **analyze_python_file**
- **Purpose**: Python AST analysis
- **Parameters**: 
  - `file_path` (str) - Path to Python file
- **Returns**: 
  - List of imports
  - List of functions with signatures
  - List of classes with methods
- **Method**: Uses Python `ast` module
- **Use Case**: Understand code structure, detect syntax errors

---

## 🎨 Routing & Orchestration

### LangGraph Workflow

The workflow is defined in `orchestrator/workflow.py` using LangGraph:

```python
from langgraph.graph import StateGraph, START

builder = StateGraph(AgentState)

# Add nodes
builder.add_node("Supervisor", supervisor_node_with_config)
builder.add_node("General", general_node_with_config)
builder.add_node("Researcher", research_node_with_config)
builder.add_node("Coder", coding_node_with_config)

# Add edges
builder.add_edge(START, "Supervisor")

# Conditional routing from Supervisor
builder.add_conditional_edges(
    "Supervisor",
    route_from_supervisor,
    {
        "General": "General",
        "Research": "Researcher",
        "Coding": "Coder",
        "ResearchAndCoding": "Researcher"
    }
)

# Conditional routing after Research
builder.add_conditional_edges(
    "Researcher",
    route_after_research,
    {
        "Coder": "Coder",
        "end": END
    }
)

workflow = builder.compile()
```

### Routing Functions

**From Supervisor** (`orchestrator/routes.py`):
```python
def route_from_supervisor(state: AgentState) -> str:
    # Returns: "General" | "Research" | "Coding" | "ResearchAndCoding"
    return state.supervisor_route
```

**After Research** (`orchestrator/routes.py`):
```python
def route_after_research(state: AgentState) -> str:
    if state.supervisor_route == 'ResearchAndCoding':
        return "Coder"
    else:
        return "end"
```

### Node Implementations

All nodes are in `orchestrator/nodes.py`:

```python
async def supervisor_node(state: AgentState, config_settings) -> AgentState:
    # Calls supervisor agent
    # Returns routing decision
    pass

async def general_node(state: AgentState, config_settings) -> AgentState:
    # Calls general agent
    # Updates state.general_result
    pass

async def research_node(state: AgentState, config_settings) -> AgentState:
    # Calls research agent with MCP tools
    # Updates state.research_result
    pass

async def coding_node(state: AgentState, config_settings) -> AgentState:
    # Calls coding agent (with optional research context)
    # Updates state.coding_result
    pass
```

### Workflow Visualization

The application generates `workflow.png` showing the graph structure:

```python
png_bytes = workflow.get_graph().draw_mermaid_png()
with open("workflow.png", "wb") as f:
    f.write(png_bytes)
```

---

## 📊 State Management

### AgentState Schema

Defined in `schemas/state.py`:

```python
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    # Input
    user_query: str = Field(
        description="Input query from user"
    )
    
    # Routing
    supervisor_route: str = Field(
        default="",
        description="Decision for routing from supervisor Agent"
    )
    supervisor_route_rationale: str = Field(
        default="",
        description="Reasoning behind the route from supervisor agent."
    )
    
    # Outputs
    general_result: str = Field(
        default="",
        description="Response from general agent"
    )
    research_result: str = Field(
        default="",
        description="Output research data from research agent."
    )
    coding_result: str = Field(
        default="",
        description="Output coding result from coding agent."
    )
```

### RoutingDecision Schema

Defined in `schemas/routing.py`:

```python
from pydantic import BaseModel, Field
from typing import Literal

class RoutingDecision(BaseModel):
    route: Literal["General", "Research", "Coding", "ResearchAndCoding"] = Field(
        description="The routing decision"
    )
    rationale: str = Field(
        description="Explanation for the routing choice"
    )
```

### State Flow Example

```python
# Initial state
state = AgentState(
    user_query="Find papers on RAG and implement it"
)

# After Supervisor
state.supervisor_route = "ResearchAndCoding"
state.supervisor_route_rationale = "Query requires research followed by implementation"

# After Research Agent
state.research_result = "RAG (Retrieval-Augmented Generation) combines..."

# After Coding Agent
state.coding_result = """
import openai
from langchain.vectorstores import FAISS

# RAG implementation
class RAGSystem:
    ...
"""

# Final result returned to user
```

---

## 🔧 LLM Configuration

### Dual LLM Support

The system supports two LLM providers with automatic fallback:

1. **Ollama** (Primary) - Local LLM execution
2. **Groq** (Fallback) - Cloud-based LLM

### Configuration in `models/llm.py`

**Core Function**:
```python
def get_llm_with_fallback(
    ollama_model: str,
    groq_model: str,
    model_type: str,
    temperature: float = 0,
    config_settings: Settings = None
) -> Union[ChatOllama, ChatGroq]:
    # 1. Check if Ollama requested
    if config_settings.use_ollama:
        # 2. Check Ollama availability
        if check_ollama_availability(config_settings):
            try:
                # 3. Try Ollama
                llm = ChatOllama(
                    model=ollama_model,
                    base_url=config_settings.ollama_base_url,
                    temperature=temperature
                )
                # 4. Test model
                llm.invoke("test")
                return llm
            except Exception as e:
                # 5. Fallback to Groq
                logger.warning(f"Ollama failed: {e}")
    
    # 6. Use Groq
    return ChatGroq(
        model=groq_model,
        temperature=temperature,
        api_key=config_settings.groq_api_key
    )
```

### LLM Functions

```python
# Supervisor LLM
get_supervisor_llm(config_settings)
# → llama3.2:latest (Ollama) or llama-3.3-70b-versatile (Groq)

# General LLM
get_general_llm(config_settings)
# → llama3.2:latest (Ollama) or llama-3.3-70b-versatile (Groq)

# Research LLM
get_research_llm(config_settings)
# → llama3.2:latest (Ollama) or llama-3.3-70b-versatile (Groq)

# Coding LLM
get_coding_llm(config_settings)
# → llama3.2:latest (Ollama) or llama-3.3-70b-versatile (Groq)
```

### Ollama Availability Check

```python
def check_ollama_availability(config_settings) -> bool:
    try:
        response = requests.get(
            f"{config_settings.ollama_base_url}/api/tags",
            timeout=3
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
```

**Cached Result**: Checked once per application run

### Recommended Models

**Ollama (Local)**:
```env
SUPERVISOR_OLLAMA_MODEL=llama3.2:latest
GENERAL_OLLAMA_MODEL=llama3.2:latest
RESEARCH_OLLAMA_MODEL=llama3.2:latest
CODING_OLLAMA_MODEL=llama3.2:latest
```

**Groq (Cloud)**:
```env
SUPERVISOR_MODEL=llama-3.3-70b-versatile
GENERAL_MODEL=llama-3.3-70b-versatile
RESEARCH_MODEL=llama-3.3-70b-versatile
CODING_MODEL=llama-3.3-70b-versatile
```

---

## 🧪 Testing

### Running Tests

The project doesn't have explicit test files in the structure, but you can test components:

**Test Supervisor Routing**:
```python
python -c "
import asyncio
from agents.supervisor.agent import create_supervisor_agent
from config.settings import Settings

async def test():
    agent = await create_supervisor_agent(Settings())
    result = await agent.ainvoke({
        'messages': [{'role': 'user', 'content': 'What is Python?'}]
    })
    print(result['structured_response'])

asyncio.run(test())
"
```

**Test Research Agent**:
```python
python -c "
import asyncio
from agents.research.agent import create_research_agent
from mcp_client.manager import MCPManager
from config.settings import Settings

async def test():
    mcp_manager = MCPManager()
    await mcp_manager.register_server('research', 'mcp_servers/research_server.py')
    
    agent = await create_research_agent(Settings(), mcp_manager)
    result = await agent.ainvoke({
        'messages': [{'role': 'user', 'content': 'Search for Python tutorials'}]
    })
    print(result['messages'][-1].content)
    
    await mcp_manager.disconnect()

asyncio.run(test())
"
```

**Test Coding Agent**:
```python
python -c "
import asyncio
from agents.coding.agent import create_coding_agent
from config.settings import Settings

async def test():
    agent = await create_coding_agent(Settings())
    result = await agent.ainvoke({
        'messages': [{'role': 'user', 'content': 'List files in current directory'}]
    })
    print(result['messages'][-1].content)

asyncio.run(test())
"
```

### Manual Testing

**Full Workflow Test**:
```bash
# Test with Groq
python main.py

# Test with Ollama
python main.py --use-ollama
```

**Test Queries**:
```
# General
User Query: What is machine learning?

# Research
User Query: Find papers on transformers from arXiv

# Coding
User Query: List all Python files

# ResearchAndCoding
User Query: Research LangChain and create a sample agent
```

---

## ✅ Best Practices

### For Users

1. **Clear Queries**: Be specific about what you need
   - ❌ "Tell me about AI"
   - ✅ "Find recent arXiv papers on transformer models"

2. **Review Logs**: Check `logs/` directory for detailed execution traces

3. **API Key Security**: Never commit `.env` file
   ```bash
   # Verify .gitignore includes .env
   cat .gitignore | grep .env
   ```

4. **Choose Right LLM**:
   - Use Ollama for privacy and no API costs
   - Use Groq for faster inference and larger models

### For Developers

1. **Adding New Agents**:
   ```python
   # 1. Create agent file in agents/
   # 2. Define system prompt
   # 3. Register tools
   # 4. Add to orchestrator/nodes.py
   # 5. Update routing logic
   ```

2. **Adding New MCP Tools**:
   ```python
   # In mcp_servers/research_server.py
   @mcp.tool
   def new_tool(param: str) -> str:
       '''Tool description for LLM'''
       try:
           result = do_something(param)
           return result
       except Exception as e:
           return f"Error: {str(e)}"
   ```

3. **Adding New Local Tools**:
   ```python
   # In tools/coding/
   from langchain.tools import tool
   
   @tool
   def new_tool(param: str) -> str:
       '''Tool description'''
       # Implementation
       pass
   ```

4. **Modifying Routing**:
   - Update `schemas/routing.py` for new route types
   - Update `orchestrator/routes.py` for routing logic
   - Update supervisor prompt for routing decisions

5. **Error Handling**:
   ```python
   try:
       result = await agent.ainvoke(...)
   except Exception as e:
       logger.exception(f"Agent error: {e}")
       # Handle gracefully
   ```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. MCP Server Connection Fails
**Error**: `Failed to connect to MCP server`

**Solutions**:
```bash
# Check Python path in mcp_servers/research_server.py
# Verify dependencies installed
pip install fastmcp ddgs beautifulsoup4 yt-dlp youtube-transcript-api

# Test server directly
python mcp_servers/research_server.py
```

#### 2. Ollama Not Available
**Error**: `Ollama service is not available`

**Solutions**:
```bash
# Check Ollama running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Pull required model
ollama pull llama3.2:latest

# Or use Groq fallback
python main.py  # (without --use-ollama flag)
```

#### 3. Groq API Key Error
**Error**: `AuthenticationError` or `Invalid API Key`

**Solutions**:
```bash
# Verify .env file
cat .env | grep GROQ_API_KEY

# Check for extra spaces/quotes
# Correct format:
GROQ_API_KEY=gsk_xxxxxxxxxxxxx

# Get new key from https://console.groq.com
```

#### 4. Import Errors
**Error**: `ModuleNotFoundError`

**Solutions**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check virtual environment activated
which python  # Should show .venv path

# Verify Python version
python --version  # Should be 3.10+
```

#### 5. Workflow Compilation Error
**Error**: `Graph compilation failed`

**Solutions**:
- Check all node functions are async
- Verify routing functions return correct types
- Ensure state schema matches node updates
- Review `orchestrator/workflow.py` for typos

#### 6. Tool Execution Timeout
**Error**: `Tool execution timed out`

**Solutions**:
- Increase timeout in tool implementation
- Check internet connectivity for web tools
- Verify API rate limits not exceeded

### Debug Mode

**Enable Detailed Logging**:
```python
# In config/logging_config.py
console_handler.setLevel(logging.DEBUG)
```

**View Logs**:
```bash
# Real-time
tail -f logs/tools_*.log

# Search for errors
grep ERROR logs/tools_*.log

# View specific tool
grep "duckduckgo_search" logs/tools_*.log
```

### Getting Help

1. Check `logs/` directory for detailed error traces
2. Review system prompts in `agents/*/prompt.py`
3. Test agents individually (see Testing section)
4. Verify environment variables in `.env`
5. Check workflow.png for graph structure

---

## 🤝 Contributing

### Adding Features

1. **New Agent**:
   - Create directory in `agents/`
   - Implement agent.py and prompt.py
   - Register in `orchestrator/nodes.py`
   - Update routing logic

2. **New MCP Tool**:
   - Add to `mcp_servers/research_server.py`
   - Use `@mcp.tool` decorator
   - Include docstring for LLM
   - Handle errors gracefully

3. **New Local Tool**:
   - Create in `tools/coding/` or `tools/research/`
   - Use `@tool` decorator from LangChain
   - Register with appropriate agent

4. **New Route Type**:
   - Update `schemas/routing.py`
   - Modify supervisor prompt
   - Update routing functions
   - Add to workflow graph

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings
- Implement async where possible
- Include error handling
- Add logging statements

### Testing Your Changes

1. Test individual components
2. Test full workflow
3. Check logs for errors
4. Verify with both Ollama and Groq
5. Test edge cases and error scenarios

---

## 📊 Project Statistics

- **Agents**: 4 (Supervisor, General, Research, Coding)
- **MCP Servers**: 1 (Research)
- **Research Tools**: 7 (via MCP)
- **Coding Tools**: 6 (local)
- **Total Tools**: 13
- **Routing Options**: 4 (General, Research, Coding, ResearchAndCoding)
- **LLM Providers**: 2 (Ollama, Groq)
- **Architecture**: Async, MCP-based, LangGraph orchestration
- **Lines of Code**: ~3500+

---

## 🎉 Summary

This Multi-Agent AI System provides:

✅ **4 Specialized Agents** - Supervisor, General, Research, Coding  
✅ **Intelligent Routing** - Context-aware task delegation  
✅ **MCP Integration** - Modular, extensible tool architecture  
✅ **Dual LLM Support** - Ollama local + Groq cloud with fallback  
✅ **13 Specialized Tools** - Web, academic, code, file operations  
✅ **LangGraph Orchestration** - Conditional workflow with state management  
✅ **Production-Ready** - Comprehensive logging, error handling  
✅ **Async Architecture** - Efficient async/await implementation  
✅ **Well-Documented** - Detailed README and code comments  
✅ **Flexible** - Easy to extend and customize  

**Start building with AI agents today!** 🚀

---

*Last Updated: January 2025*  
*Version: 3.0 (MCP-Enhanced)*  
*Status: Production Ready* ✅
