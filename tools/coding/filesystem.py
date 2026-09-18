from langchain.tools import tool
from config.logging_config import setup_logger, log_tool_call, log_tool_output, log_tool_error

from pathlib import Path

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
    