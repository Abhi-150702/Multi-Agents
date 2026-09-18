# 🤖 Multi-Agent AI System with Comprehensive Logging

## 📋 Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Understanding the Code](#understanding-the-code)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Agents](#agents)
- [Tools](#tools)
- [Logging System](#logging-system)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

This is a **production-ready Multi-Agent AI System** built with LangChain and LangGraph that provides two specialized AI agents:

1. **Research Agent** - Conducts comprehensive research using multiple information sources (web search, academic papers, GitHub, YouTube, etc.)
2. **Coding Agent** - Assists with software development tasks including code analysis, file operations, and code generation

The system features **enterprise-grade logging** that tracks all tool executions, providing complete visibility into agent operations for debugging, monitoring, and audit purposes.

### Key Highlights
- 🔍 **10 Specialized Tools** across two agents
- 📊 **Comprehensive Logging** with dual output (console + file)
- 🚀 **Powered by Groq LLMs** for fast inference
- 🛠️ **Modular Architecture** for easy extension
- 📝 **Complete Documentation** with examples and guides
- ✅ **Fully Tested** with dedicated test scripts

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Main Application                      │
│                         (main.py)                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ├─────────────────┬──────────────────┐
                         ▼                 ▼                  ▼
              ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐
              │  Research Agent   │  │ Coding Agent │  │   LLM Models │
              │  (7 Tools)        │  │ (3 Tools)    │  │   (Groq)     │
              └──────────────────┘  └──────────────┘  └──────────────┘
                         │                 │
                         │                 │
              ┌──────────┴─────────────────┴──────────┐
              │                                        │
              ▼                                        ▼
    ┌─────────────────┐                    ┌─────────────────┐
    │  Research Tools │                    │  Coding Tools   │
    ├─────────────────┤                    ├─────────────────┤
    │ • Web Search    │                    │ • File System   │
    │ • GitHub        │                    │ • Code Analysis │
    │ • arXiv         │                    │ • File Reading  │
    │ • YouTube       │                    └─────────────────┘
    │ • Web Scraping  │
    └─────────────────┘
              │
              ▼
    ┌─────────────────────────────────────┐
    │      Logging System                  │
    │  • Console Output (INFO)             │
    │  • File Logs (DEBUG)                 │
    │  • Error Tracking                    │
    │  • Performance Monitoring            │
    └─────────────────────────────────────┘
```

---

## 🧠 Understanding the Code

### Core Components

#### 1. **Main Entry Point** (`main.py`)
- Initializes the application
- Takes user query as input
- Creates and invokes the Research Agent
- Logs the final response

**Flow:**
```python
User Input → Create Agent → Invoke Agent → Get Response → Log Output
```

#### 2. **Agent Configuration**

##### Research Agent (`agents/research/agent.py`)
- **Purpose**: Conducts comprehensive research using multiple sources
- **Tools**: 7 specialized research tools
- **Model**: Configurable LLM from Groq (via environment variables)
- **System Prompt**: Detailed instructions for research methodology

**Key Functions:**
- `create_research_agent()` - Initializes agent with tools and model

##### Coding Agent (`agents/coding/agent.py`)
- **Purpose**: Assists with software development tasks
- **Tools**: 3 file system and code analysis tools
- **Model**: Configurable LLM from Groq
- **System Prompt**: Guidelines for code generation and analysis

**Key Functions:**
- `create_coding_agent()` - Initializes agent with coding tools

#### 3. **Language Models** (`models/llm.py`)

Provides two LLM configurations:
- **Research LLM**: Optimized for information retrieval and synthesis
- **Coding LLM**: Optimized for code understanding and generation

Both use:
- **Provider**: Groq (fast inference)
- **Temperature**: 0 (deterministic outputs)
- **Models**: Configurable via environment variables

#### 4. **Configuration** (`config/settings.py`)

Manages environment variables using Pydantic:
```python
Settings:
  - groq_api_key        # Groq API authentication
  - google_api_key      # Google Search API
  - google_cse_id       # Google Custom Search Engine ID
  - research_model      # Model name for research agent
  - coding_model        # Model name for coding agent
```

#### 5. **Logging System** (`config/logging_config.py`)

Centralized logging infrastructure:
- **Dual Output**: Console (INFO) + File (DEBUG)
- **Timestamped Files**: `logs/tools_YYYYMMDD_HHMMSS.log`
- **Smart Truncation**: Readable console, complete file logs

**Key Functions:**
- `setup_logger(name)` - Initialize logger for a component
- `log_tool_call(logger, tool_name, **kwargs)` - Log tool invocations
- `log_tool_output(logger, tool_name, output, success)` - Log results
- `log_tool_error(logger, tool_name, error)` - Log errors with traces

---

## ✨ Features

### Research Agent Capabilities
1. **Web Search**
   - DuckDuckGo search (no API key required)
   - Google Custom Search (requires API key)

2. **Academic Research**
   - arXiv paper search and retrieval

3. **Code Discovery**
   - GitHub repository search
   - Open-source implementation discovery

4. **Video Content**
   - YouTube video search
   - YouTube transcript extraction

5. **Web Scraping**
   - Webpage content extraction
   - HTML parsing and text extraction

### Coding Agent Capabilities
1. **File System Operations**
   - Directory listing with file/folder distinction
   - File content reading with size limits

2. **Code Analysis**
   - Python AST (Abstract Syntax Tree) parsing
   - Extract imports, functions, classes
   - Syntax error detection

### Logging Features
1. **Comprehensive Tracking**
   - All tool calls logged with parameters
   - All outputs logged (truncated in console, full in files)
   - All errors logged with full stack traces

2. **Dual Output System**
   - Console: Real-time INFO level logs
   - Files: Detailed DEBUG level logs

3. **Smart Management**
   - Automatic log directory creation
   - Timestamped log files
   - UTF-8 encoding support
   - Configurable truncation thresholds

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- API keys (Groq, Google Search - optional)

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
   touch .env
   ```

5. **Configure Environment Variables**
   Edit `.env` file:
   ```env
   # Required
   GROQ_API_KEY=your_groq_api_key_here
   RESEARCH_MODEL=mixtral-8x7b-32768
   CODING_MODEL=llama3-70b-8192

   # Optional (for Google Search)
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_custom_search_engine_id
   ```

---

## ⚙️ Configuration

### Required API Keys

#### 1. Groq API Key (Required)
- **Purpose**: Powers the LLM models
- **Get it**: [https://console.groq.com](https://console.groq.com)
- **Free Tier**: Available with rate limits

#### 2. Google Search API (Optional)
- **Purpose**: Enables Google Custom Search tool
- **Get it**: [Google Cloud Console](https://console.cloud.google.com)
- **Note**: DuckDuckGo search works without this

### Model Configuration

Available Groq models:
- `mixtral-8x7b-32768` - Good for research tasks
- `llama3-70b-8192` - Good for coding tasks
- `llama3-8b-8192` - Faster, lighter option
- `gemma-7b-it` - Alternative option

Edit in `.env`:
```env
RESEARCH_MODEL=mixtral-8x7b-32768
CODING_MODEL=llama3-70b-8192
```

### Logging Configuration

Customize logging in `config/logging_config.py`:

```python
# Change console log level
console_handler.setLevel(logging.INFO)  # Default
console_handler.setLevel(logging.DEBUG)  # More verbose
console_handler.setLevel(logging.WARNING)  # Less verbose

# Change file log level
file_handler.setLevel(logging.DEBUG)  # Default (detailed)
file_handler.setLevel(logging.INFO)  # Less detail

# Change truncation threshold
if len(output) > 1000:  # Default
if len(output) > 2000:  # Show more in console
```

---

## 🚀 Usage

### Running the Application

#### Basic Usage
```bash
python main.py
```

You'll be prompted:
```
Query: [Enter your question here]
```

#### Example Queries

**Research Agent Examples:**
```
Query: What are the latest trends in artificial intelligence for 2024?
Query: Find Python libraries for web scraping and their GitHub repositories
Query: Search for academic papers on transformer models
Query: Find YouTube tutorials on LangChain framework
```

**Coding Agent Examples:**
```python
# You'll need to modify main.py to use coding agent
from agents.coding.agent import create_coding_agent

Query: List all Python files in the current directory
Query: Analyze the structure of config/settings.py
Query: Read the contents of main.py and explain the code
```

### Using Specific Agents

#### Use Research Agent (Default)
```python
# main.py (current implementation)
from agents.research.agent import create_research_agent

def main(query: str) -> None:
    agent = create_research_agent()
    response = agent.invoke({"messages": [{"role": "user", "content": query}]})
    # Process response
```

#### Use Coding Agent
```python
# Modify main.py
from agents.coding.agent import create_coding_agent

def main(query: str) -> None:
    agent = create_coding_agent()
    response = agent.invoke({"messages": [{"role": "user", "content": query}]})
    # Process response
```

---

## 🤖 Agents

### Research Agent

**System Prompt Strategy:**
The Research Agent follows a structured research process:

1. **Understand** the user's question
2. **Determine** appropriate information sources
3. **Search** those sources
4. **Inspect** relevant results
5. **Read** underlying sources when necessary
6. **Cross-check** important information
7. **Synthesize** the information
8. **Return** clear answer with source references

**Tool Selection Logic:**
- General web info → `duckduckgo_search` or `google_search`
- Academic papers → `arxiv_search`
- Code repositories → `github_search`
- Video content → `youtube_search` + `youtube_transcript`
- Deep content → `read_webpage`

**Best Practices:**
- Never invents tool names
- Preserves source URLs
- Cross-checks multiple sources
- Prefers primary sources
- Handles tool failures gracefully

### Coding Agent

**System Prompt Strategy:**
The Coding Agent follows software engineering best practices:

1. **Understand** requirements
2. **Identify** programming language and framework
3. **Inspect** existing code
4. **Design** solution
5. **Write** clean, maintainable code
6. **Handle** errors appropriately
7. **Explain** implementation decisions

**Code Quality Guidelines:**
- Uses type hints
- Clear variable names
- Modular structure
- Appropriate error handling
- Production-quality code
- Minimal dependencies

**Available Tools:**
- `list_files` - Explore project structure
- `read_files` - Inspect source code
- `analyze_python_file` - Understand Python code structure

---

## 🛠️ Tools

### Research Tools (7 Tools)

#### 1. **duckduckgo_search**
- **Purpose**: General web search
- **API Required**: No
- **Parameters**: `query` (str)
- **Returns**: Formatted search results with titles, URLs, snippets
- **Example**:
  ```python
  duckduckgo_search.invoke({"query": "Python tutorials"})
  ```

#### 2. **google_search**
- **Purpose**: Google Custom Search
- **API Required**: Yes (Google API Key + CSE ID)
- **Parameters**: `query` (str)
- **Returns**: Google search results
- **Example**:
  ```python
  google_search.invoke({"query": "machine learning"})
  ```

#### 3. **arxiv_search**
- **Purpose**: Search academic papers on arXiv
- **API Required**: No
- **Parameters**: `query` (str)
- **Returns**: Paper titles, abstracts, URLs
- **Example**:
  ```python
  arxiv_search.invoke({"query": "neural networks"})
  ```

#### 4. **github_search**
- **Purpose**: Search GitHub repositories
- **API Required**: No (uses public API)
- **Parameters**: `query` (str), `max_results` (int, default=5)
- **Returns**: Repository info (name, stars, forks, URL)
- **Example**:
  ```python
  github_search.invoke({"query": "web scraping python", "max_results": 3})
  ```

#### 5. **youtube_search**
- **Purpose**: Search YouTube videos
- **API Required**: No
- **Parameters**: `query` (str), `max_results` (int, default=5)
- **Returns**: Video titles, URLs, channels, views
- **Example**:
  ```python
  youtube_search.invoke({"query": "Python tutorial", "max_results": 5})
  ```

#### 6. **youtube_transcript**
- **Purpose**: Extract YouTube video transcripts
- **API Required**: No
- **Parameters**: `video_url` (str), `max_characters` (int, default=1000)
- **Returns**: Video transcript with timestamps
- **Example**:
  ```python
  youtube_transcript.invoke({"video_url": "https://youtube.com/watch?v=..."})
  ```

#### 7. **read_webpage**
- **Purpose**: Extract content from webpages
- **API Required**: No
- **Parameters**: `url` (str), `max_characters` (int, default=1000)
- **Returns**: Extracted text content
- **Example**:
  ```python
  read_webpage.invoke({"url": "https://example.com", "max_characters": 2000})
  ```

### Coding Tools (3 Tools)

#### 1. **list_files**
- **Purpose**: List directory contents
- **Parameters**: `directory` (str, default='.')
- **Returns**: Formatted list with [DIR]/[FILE] prefixes
- **File Limit**: None
- **Example**:
  ```python
  list_files.invoke({"directory": "./tools"})
  ```

#### 2. **read_files**
- **Purpose**: Read file contents
- **Parameters**: `file_path` (str)
- **Returns**: File content as string
- **File Limit**: 100KB max
- **Encoding**: UTF-8 with error replacement
- **Example**:
  ```python
  read_files.invoke({"file_path": "config/settings.py"})
  ```

#### 3. **analyze_python_file**
- **Purpose**: Python AST analysis
- **Parameters**: `file_path` (str)
- **Returns**: Lists of imports, functions, classes
- **Method**: Uses Python's AST module
- **Example**:
  ```python
  analyze_python_file.invoke({"file_path": "main.py"})
  ```

---

## 📊 Logging System

### Overview
Every tool call is automatically logged with:
- ✅ Tool name
- ✅ Input parameters
- ✅ Execution timestamp
- ✅ Output/results
- ✅ Success/failure status
- ✅ Error messages and stack traces

### Log File Structure

```
logs/
├── tools_20240115_143022.log
├── tools_20240115_150133.log
└── tools_20240115_163045.log
```

### Log Entry Format

#### Tool Call
```
============================================================
2024-01-15 14:30:22 - duckduckgo_search - INFO - Tool Called: duckduckgo_search
2024-01-15 14:30:22 - duckduckgo_search - INFO - Parameters:
2024-01-15 14:30:22 - duckduckgo_search - INFO -   - query: Python tutorials
============================================================
```

#### Tool Output (Success)
```
------------------------------------------------------------
2024-01-15 14:30:25 - duckduckgo_search - INFO - Tool Output: duckduckgo_search
2024-01-15 14:30:25 - duckduckgo_search - INFO - Status: SUCCESS
2024-01-15 14:30:25 - duckduckgo_search - INFO - Output: Title: Learn Python...
------------------------------------------------------------
```

#### Tool Error
```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
2024-01-15 14:30:25 - read_files - ERROR - Tool Error: read_files
2024-01-15 14:30:25 - read_files - ERROR - Error Type: FileNotFoundError
2024-01-15 14:30:25 - read_files - ERROR - Error Message: File not found
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

### Viewing Logs

#### Real-time Monitoring
```bash
# Watch logs in real-time
tail -f logs/tools_*.log

# Filter by tool
tail -f logs/tools_*.log | grep "github_search"
```

#### Search Logs
```bash
# Find all errors
grep "ERROR" logs/tools_*.log

# Find specific tool calls
grep "Tool Called: list_files" logs/tools_*.log

# Count tool usage
grep "Tool Called" logs/tools_*.log | wc -l

# See all tools used
grep "Tool Called:" logs/tools_*.log | cut -d: -f3 | sort | uniq
```

### Log Configuration

**Console Output** (stdout):
- Level: INFO and above
- Shows: Real-time progress
- Truncates: Long outputs (>1000 chars)

**File Output** (logs/*.log):
- Level: DEBUG and above
- Shows: Everything in detail
- Truncates: Nothing (complete logs)

---

## 🧪 Testing

### Test Scripts

#### 1. Test Research Tools
```bash
python test_logging.py
```

**Tests:**
- DuckDuckGo search
- Google search (may fail without API keys)
- Webpage reading
- GitHub search
- arXiv search
- YouTube search
- YouTube transcript

#### 2. Test Coding Tools
```bash
python test_coding_tools_logging.py
```

**Tests:**
- List current directory
- List subdirectories
- List non-existent directory (error handling)
- Read existing files
- Read non-existent files (error handling)
- Analyze valid Python files
- Analyze files with syntax errors

### Manual Testing

#### Test Individual Tools
```python
# Test a research tool
from tools.research.web.duckduckgo_search import duckduckgo_search
result = duckduckgo_search.invoke({"query": "test query"})
print(result)

# Test a coding tool
from tools.coding.filesystem import list_files
result = list_files.invoke({"directory": "."})
print(result)
```

### Expected Test Results
- ✅ All tools execute without crashes
- ✅ Logs created in `logs/` directory
- ✅ Console shows INFO level logs
- ✅ Files contain DEBUG level logs
- ✅ Errors handled gracefully

---

## 📁 Project Structure

```
Multi-Agents/
│
├── 📁 agents/                          # Agent configurations
│   ├── 📁 coding/
│   │   ├── agent.py                   # Coding agent setup
│   │   └── prompt.py                  # Coding agent system prompt
│   └── 📁 research/
│       ├── agent.py                   # Research agent setup
│       └── prompt.py                  # Research agent system prompt
│
├── 📁 config/                          # Configuration files
│   ├── logging_config.py              # Logging setup
│   └── settings.py                    # Environment variables
│
├── 📁 models/                          # LLM configurations
│   └── llm.py                         # Groq model setup
│
├── 📁 tools/                           # Tool implementations
│   ├── 📁 coding/
│   │   ├── code_analysis.py          # Python AST analysis
│   │   └── filesystem.py             # File operations
│   └── 📁 research/
│       ├── 📁 academic/
│       │   └── arxiv.py              # arXiv search
│       ├── 📁 code/
│       │   └── github.py             # GitHub search
│       └── 📁 web/
│           ├── duckduckgo_search.py  # DuckDuckGo search
│           ├── google_search.py      # Google search
│           ├── webpage.py            # Web scraping
│           ├── youtube.py            # YouTube search
│           └── youtube_transcripts.py # YouTube transcripts
│
├── 📁 logs/                            # Auto-generated logs
│   └── tools_YYYYMMDD_HHMMSS.log     # Timestamped log files
│
├── 📄 main.py                          # Main entry point
├── 📄 requirements.txt                 # Python dependencies
├── 📄 .env                             # Environment variables (create this)
├── 📄 .gitignore                       # Git ignore rules
│
├── 📄 test_logging.py                  # Research tools test
├── 📄 test_coding_tools_logging.py     # Coding tools test
│
└── 📚 Documentation/
    ├── LOGGING_DOCUMENTATION.md       # Complete logging docs
    ├── LOGGING_QUICK_REFERENCE.md     # Quick reference
    ├── LOGGING_SYSTEM_README.md       # Logging system overview
    ├── CODING_AGENT_LOGGING_SUMMARY.md # Implementation details
    └── IMPLEMENTATION_CHECKLIST.md    # Implementation checklist
```

---

## 🔄 How It Works

### Execution Flow

```
1. User Input
   ↓
2. main.py receives query
   ↓
3. Create Agent (Research/Coding)
   ├── Load LLM model from Groq
   ├── Load system prompt
   └── Register tools
   ↓
4. Agent processes query
   ├── Analyzes query
   ├── Decides which tools to use
   └── Plans execution strategy
   ↓
5. Tool Execution
   ├── Log tool call (parameters)
   ├── Execute tool logic
   ├── Log output (results)
   └── Handle errors (if any)
   ↓
6. Agent synthesizes results
   ↓
7. Return final response
   ↓
8. Log and display output
```

### Tool Execution Pattern

Every tool follows this pattern:

```python
@tool
def tool_name(param: str) -> str:
    try:
        # 1. Log the call
        log_tool_call(logger, "tool_name", param=param)

        # 2. Execute logic
        result = perform_operation(param)

        # 3. Log success
        log_tool_output(logger, "tool_name", result, success=True)
        return result

    except Exception as e:
        # 4. Log error
        log_tool_error(logger, "tool_name", e)
        error_msg = f"Error: {str(e)}"
        log_tool_output(logger, "tool_name", error_msg, success=False)
        return error_msg
```

### Agent Decision Making

1. **Query Analysis**: Agent analyzes user's question
2. **Tool Selection**: Based on system prompt, selects appropriate tools
3. **Execution**: Calls tools in logical sequence
4. **Result Processing**: Processes tool outputs
5. **Synthesis**: Combines information into coherent answer
6. **Iteration**: May call additional tools if needed
7. **Response**: Returns final answer to user

---

## ✅ Best Practices

### For Users

1. **Clear Queries**: Be specific about what you want
   - ❌ "Tell me about AI"
   - ✅ "Find recent research papers on transformer models from arXiv"

2. **Review Logs**: Check logs after runs for insights
   ```bash
   tail -100 logs/tools_*.log
   ```

3. **API Keys**: Keep API keys secure
   - Never commit `.env` to version control
   - Use environment variables

4. **Test First**: Run test scripts before production use
   ```bash
   python test_logging.py
   python test_coding_tools_logging.py
   ```

### For Developers

1. **Adding New Tools**:
   ```python
   from langchain.tools import tool
   from config.logging_config import setup_logger, log_tool_call, log_tool_output, log_tool_error

   logger = setup_logger("new_tool")

   @tool
   def new_tool(param: str) -> str:
       try:
           log_tool_call(logger, "new_tool", param=param)
           result = do_something(param)
           log_tool_output(logger, "new_tool", result, success=True)
           return result
       except Exception as e:
           log_tool_error(logger, "new_tool", e)
           error_msg = f"Error: {str(e)}"
           log_tool_output(logger, "new_tool", error_msg, success=False)
           return error_msg
   ```

2. **Modifying Agents**: Update system prompts for behavior changes

3. **Log Management**: Archive old logs regularly
   ```bash
   # Compress logs older than 7 days
   find logs/ -name "*.log" -mtime +7 -exec gzip {} \;
   ```

4. **Error Handling**: Always log errors with context

---

## 🐛 Troubleshooting

### Common Issues

#### 1. API Key Errors
**Problem**: `AuthenticationError` or `Invalid API Key`

**Solution**:
```bash
# Check .env file exists
ls -la .env

# Verify API key format
cat .env | grep GROQ_API_KEY

# Ensure no extra spaces or quotes
GROQ_API_KEY=your_key_here  # Correct
GROQ_API_KEY="your_key_here"  # May cause issues
```

#### 2. Import Errors
**Problem**: `ModuleNotFoundError`

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify virtual environment
which python

# Check installed packages
pip list
```

#### 3. No Logs Generated
**Problem**: Logs directory empty

**Solution**:
```bash
# Check permissions
ls -la logs/

# Manually create if needed
mkdir logs
chmod 755 logs

# Verify logging configuration
python -c "from config.logging_config import setup_logger; logger = setup_logger('test'); logger.info('test')"
```

#### 4. Tool Failures
**Problem**: Tools returning errors

**Solution**:
```bash
# Check specific tool logs
grep "Tool Error" logs/tools_*.log

# Test tool individually
python test_logging.py

# Verify API access (for API-based tools)
curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/v1/models
```

#### 5. Large Log Files
**Problem**: Logs consuming disk space

**Solution**:
```bash
# Check log sizes
du -sh logs/

# Compress old logs
gzip logs/tools_202401*.log

# Delete very old logs
find logs/ -name "*.log" -mtime +30 -delete

# Or implement log rotation in logging_config.py
```

### Debug Mode

Enable more verbose logging:

```python
# In config/logging_config.py
console_handler.setLevel(logging.DEBUG)  # Show everything
```

### Getting Help

1. Check documentation files in the repo
2. Review test scripts for examples
3. Examine logs for detailed error messages
4. Test tools individually before full system runs

---

## 🤝 Contributing

### Adding New Tools

1. **Create tool file** in appropriate directory
2. **Implement tool function** with `@tool` decorator
3. **Add logging** (call, output, error)
4. **Register tool** in agent configuration
5. **Update documentation**
6. **Add tests**

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings
- Include error handling
- Log all operations

### Testing

- Write tests for new tools
- Ensure logging works
- Test error scenarios
- Verify API integrations

---

## 📄 License

This project is provided as-is for educational and research purposes.

---

## 🙏 Acknowledgments

- **LangChain** - Framework for building agents
- **LangGraph** - Agent orchestration
- **Groq** - Fast LLM inference
- **DuckDuckGo** - Privacy-focused search
- **arXiv** - Academic paper repository

---

## 📞 Support

- **Documentation**: See `LOGGING_DOCUMENTATION.md` for detailed logging info
- **Quick Reference**: See `LOGGING_QUICK_REFERENCE.md` for common commands
- **Examples**: Check test scripts for usage examples

---

## 📊 Statistics

- **Total Agents**: 2 (Research + Coding)
- **Total Tools**: 10 (7 Research + 3 Coding)
- **Lines of Code**: ~2000+
- **Documentation Files**: 5 comprehensive guides
- **Test Scripts**: 2 with 15+ test cases
- **Logging Coverage**: 100% of tools

---

## 🎉 Summary

This Multi-Agent AI System provides:

✅ **Production-Ready** - Comprehensive logging and error handling  
✅ **Well-Documented** - 5 documentation files with examples  
✅ **Fully Tested** - Test scripts for all tools  
✅ **Modular Design** - Easy to extend and customize  
✅ **Enterprise Features** - Logging, monitoring, audit trails  
✅ **Multiple Agents** - Research and Coding capabilities  
✅ **10 Specialized Tools** - Covering diverse use cases  
✅ **Fast Inference** - Powered by Groq  

**Get started in minutes, scale to production!** 🚀

---

*Last Updated: January 2024*  
*Version: 2.0*  
*Status: Production Ready* ✅