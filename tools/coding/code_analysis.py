import ast
from langchain.tools import tool
from config.logging_config import setup_logger, log_tool_call, log_tool_output, log_tool_error

logger = setup_logger("analyze_python_file")

@tool
def analyze_python_file(file_path: str) -> str:
    """
    Analyze a Python source file using Python's AST.

    Use this tool when you need to understand:
    - classes
    - functions
    - imports
    - basic module structure

    This tool does not execute the code.
    """
    try:
        log_tool_call(logger, "analyze_python_file", file_path=file_path)

        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            source = file.read()

        tree = ast.parse(source)

        imports = []
        functions = []
        classes = []

        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(node)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")

            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

            elif isinstance(node, ast.AsyncFunctionDef):
                functions.append(f"async {node.name}")

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

        result = (
            f"File: {file_path}\n\n"
            f"Imports:\n{chr(10).join(imports) or 'None'}\n\n"
            f"Functions:\n{chr(10).join(functions) or 'None'}\n\n"
            f"Classes:\n{chr(10).join(classes) or 'None'}\n\n"
        )

        log_tool_output(logger, "analyze_python_file", result, success=True)
        return result

    except SyntaxError as exc:
        log_tool_error(logger, "analyze_python_file", exc)
        error_msg = (
            f"Python syntax error:\n"
            f"Line {exc.lineno}: {exc.msg}"
        )
        log_tool_output(logger, "analyze_python_file", error_msg, success=False)
        return error_msg

    except Exception as exc:
        log_tool_error(logger, "analyze_python_file", exc)
        error_msg = f"Analysis failed: {exc}"
        log_tool_output(logger, "analyze_python_file", error_msg, success=False)
        return error_msg