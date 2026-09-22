import sys
from pathlib import Path

# Add parent directory to Python path to import config module
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastmcp import FastMCP
from config.logging_config import setup_logger, log_tool_error, log_tool_output, log_tool_call

logger = setup_logger("Coding MCP Tools")

mcp = FastMCP("Coding Server")


@mcp.tool
def read_file(file_path: str) -> str:
    """
    Read the contents of a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File contents or error message
    """
    try:
        log_tool_call(logger, "read_file", file_path=file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        log_tool_output(logger, "read_file", f"Successfully read {len(content)} characters", success=True)
        return content
        
    except Exception as e:
        log_tool_error(logger, "read_file", e)
        error_msg = f"Error reading file: {str(e)}"
        log_tool_output(logger, "read_file", error_msg, success=False)
        return error_msg


@mcp.tool
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        
    Returns:
        Success or error message
    """
    try:
        log_tool_call(logger, "write_file", file_path=file_path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        success_msg = f"Successfully wrote {len(content)} characters to {file_path}"
        log_tool_output(logger, "write_file", success_msg, success=True)
        return success_msg
        
    except Exception as e:
        log_tool_error(logger, "write_file", e)
        error_msg = f"Error writing file: {str(e)}"
        log_tool_output(logger, "write_file", error_msg, success=False)
        return error_msg


@mcp.tool
def list_directory(directory_path: str) -> str:
    """
    List contents of a directory.
    
    Args:
        directory_path: Path to the directory to list
        
    Returns:
        Directory contents or error message
    """
    try:
        log_tool_call(logger, "list_directory", directory_path=directory_path)
        
        path = Path(directory_path)
        if not path.exists():
            return f"Directory does not exist: {directory_path}"
        
        if not path.is_dir():
            return f"Path is not a directory: {directory_path}"
        
        items = []
        for item in sorted(path.iterdir()):
            item_type = "DIR" if item.is_dir() else "FILE"
            items.append(f"[{item_type}] {item.name}")
        
        result = "\n".join(items) if items else "Directory is empty"
        log_tool_output(logger, "list_directory", f"Found {len(items)} items", success=True)
        return result
        
    except Exception as e:
        log_tool_error(logger, "list_directory", e)
        error_msg = f"Error listing directory: {str(e)}"
        log_tool_output(logger, "list_directory", error_msg, success=False)
        return error_msg


@mcp.tool
def analyze_code(code: str, language: str = "python") -> str:
    """
    Analyze code for potential issues and improvements.
    
    Args:
        code: The code to analyze
        language: Programming language (default: python)
        
    Returns:
        Analysis results
    """
    try:
        log_tool_call(logger, "analyze_code", language=language)
        
        # Basic code analysis
        lines = code.split('\n')
        analysis = []
        
        analysis.append(f"Code Statistics:")
        analysis.append(f"  - Total lines: {len(lines)}")
        analysis.append(f"  - Non-empty lines: {len([l for l in lines if l.strip()])}")
        analysis.append(f"  - Language: {language}")
        
        if language.lower() == "python":
            # Python-specific analysis
            imports = [l for l in lines if l.strip().startswith('import') or l.strip().startswith('from')]
            functions = [l for l in lines if 'def ' in l]
            classes = [l for l in lines if 'class ' in l]
            
            analysis.append(f"\nPython Analysis:")
            analysis.append(f"  - Imports: {len(imports)}")
            analysis.append(f"  - Functions: {len(functions)}")
            analysis.append(f"  - Classes: {len(classes)}")
        
        result = "\n".join(analysis)
        log_tool_output(logger, "analyze_code", "Analysis complete", success=True)
        return result
        
    except Exception as e:
        log_tool_error(logger, "analyze_code", e)
        error_msg = f"Error analyzing code: {str(e)}"
        log_tool_output(logger, "analyze_code", error_msg, success=False)
        return error_msg


if __name__ == "__main__":
    mcp.run()
