from langchain.tools import tool
from config.logging_config import setup_logger, log_tool_call, log_tool_output, log_tool_error

from pathlib import Path
import os

logger = setup_logger("filesystem_tools")


@tool
def list_files(directory: str = '.') -> str:
    """
    List files and directories inside a specified directory.

    Use this tool when you need to understand the structure
    of a software project.

    This tool is read-only.
    """
    try:
        log_tool_call(logger, "list_files", directory=directory)

        path = Path(directory)

        if not path.exists():
            error_msg = f"Directory does not exists: {directory}"
            log_tool_output(logger, "list_files", error_msg, success=False)
            return error_msg

        if not path.is_dir():
            error_msg = f"Not a directory: {directory}"
            log_tool_output(logger, "list_files", error_msg, success=False)
            return error_msg

        items = []

        for item in sorted(path.iterdir()):
            prefix = "[DIR]" if item.is_dir() else "[FILE]"
            items.append(f"{prefix} {item.name}")

        result = '\n'.join(items)
        log_tool_output(logger, "list_files", result, success=True)
        return result

    except Exception as exc:
        log_tool_error(logger, "list_files", exc)
        error_msg = f"Failed to load the directory: {directory}. Error: {str(exc)}"
        log_tool_output(logger, "list_files", error_msg, success=False)
        return error_msg


@tool
def read_files(file_path: str) -> str:
    """
    Read the contents of source code or configuration code.

    Use this tool when you need to inspect the existing code.
    This is the Read-only tool.
    """

    try:
        log_tool_call(logger, "read_files", file_path=file_path)

        path = Path(file_path)

        if not path.exists():
            error_msg = f"File does not exists: {path}"
            log_tool_output(logger, "read_files", error_msg, success=False)
            return error_msg

        if not path.is_file():
            error_msg = f"Not a file: {path}"
            log_tool_output(logger, "read_files", error_msg, success=False)
            return error_msg

        max_size = 100_000

        if path.stat().st_size > max_size:
            error_msg = (
                f"File size too large to read directly."
                f"Size: {path.stat().st_size}"
            )
            log_tool_output(logger, "read_files", error_msg, success=False)
            return error_msg

        result = path.read_text(encoding='utf-8', errors='replace')
        log_tool_output(logger, "read_files", result, success=True)
        return result

    except Exception as exc:
        log_tool_error(logger, "read_files", exc)
        error_msg = f"Failed to read file: {exc}"
        log_tool_output(logger, "read_files", error_msg, success=False)
        return error_msg


@tool
def write_file(file_path: str, content: str, create_dirs: bool = True) -> str:
    """
    Write content to a file. Creates the file if it doesn't exist.
    If the file exists, it will be overwritten.

    Use this tool when you need to create or update a file with specific content.

    Args:
        file_path: Path to the file to write (e.g., 'odd.py', 'src/main.py')
        content: The content to write to the file
        create_dirs: If True, creates parent directories if they don't exist (default: True)

    Returns:
        Success message with file path and size, or error message

    Examples:
        - write_file('odd.py', 'print("hello")')
        - write_file('src/utils.py', 'def add(a, b): return a + b', create_dirs=True)
    """
    try:
        log_tool_call(logger, "write_file", file_path=file_path, content_length=len(content))

        path = Path(file_path)

        # Create parent directories if needed
        if create_dirs and path.parent != Path('.'):
            path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {path.parent}")

        # Write content to file
        path.write_text(content, encoding='utf-8')

        # Get file size for confirmation
        file_size = path.stat().st_size

        success_msg = (
            f"Successfully wrote {len(content)} characters ({file_size} bytes) to '{file_path}'.\n"
            f"File location: {path.absolute()}"
        )
        log_tool_output(logger, "write_file", success_msg, success=True)
        return success_msg

    except Exception as exc:
        log_tool_error(logger, "write_file", exc)
        error_msg = f"Failed to write file '{file_path}': {str(exc)}"
        log_tool_output(logger, "write_file", error_msg, success=False)
        return error_msg


@tool
def create_file(file_path: str, content: str) -> str:
    """
    Create a new file with the specified content.
    If the file already exists, returns an error (use write_file to overwrite).

    Use this tool when you want to ensure you're creating a NEW file
    and not accidentally overwriting an existing one.

    Args:
        file_path: Path to the new file to create
        content: The content to write to the new file

    Returns:
        Success message with file path, or error if file exists

    Examples:
        - create_file('new_script.py', 'print("Hello, World!")')
        - create_file('config.json', '{"setting": "value"}')
    """
    try:
        log_tool_call(logger, "create_file", file_path=file_path)

        path = Path(file_path)

        # Check if file already exists
        if path.exists():
            error_msg = (
                f"File '{file_path}' already exists. "
                f"Use write_file tool if you want to overwrite it."
            )
            log_tool_output(logger, "create_file", error_msg, success=False)
            return error_msg

        # Create parent directories if needed
        if path.parent != Path('.'):
            path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {path.parent}")

        # Create and write to the new file
        path.write_text(content, encoding='utf-8')

        file_size = path.stat().st_size

        success_msg = (
            f"Successfully created file '{file_path}' with {len(content)} characters ({file_size} bytes).\n"
            f"File location: {path.absolute()}"
        )
        log_tool_output(logger, "create_file", success_msg, success=True)
        return success_msg

    except Exception as exc:
        log_tool_error(logger, "create_file", exc)
        error_msg = f"Failed to create file '{file_path}': {str(exc)}"
        log_tool_output(logger, "create_file", error_msg, success=False)
        return error_msg


@tool
def append_to_file(file_path: str, content: str) -> str:
    """
    Append content to the end of an existing file.
    If the file doesn't exist, creates it.

    Use this tool when you want to add content to a file without overwriting existing content.

    Args:
        file_path: Path to the file to append to
        content: The content to append to the file

    Returns:
        Success message with updated file size

    Examples:
        - append_to_file('log.txt', 'New log entry\n')
        - append_to_file('script.py', '\n\nprint("Additional code")')
    """
    try:
        log_tool_call(logger, "append_to_file", file_path=file_path)

        path = Path(file_path)

        # Create parent directories if needed
        if path.parent != Path('.'):
            path.parent.mkdir(parents=True, exist_ok=True)

        # Get original size if file exists
        original_size = path.stat().st_size if path.exists() else 0

        # Append content
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)

        new_size = path.stat().st_size

        success_msg = (
            f"Successfully appended {len(content)} characters to '{file_path}'.\n"
            f"File size: {original_size} bytes → {new_size} bytes\n"
            f"File location: {path.absolute()}"
        )
        log_tool_output(logger, "append_to_file", success_msg, success=True)
        return success_msg

    except Exception as exc:
        log_tool_error(logger, "append_to_file", exc)
        error_msg = f"Failed to append to file '{file_path}': {str(exc)}"
        log_tool_output(logger, "append_to_file", error_msg, success=False)
        return error_msg