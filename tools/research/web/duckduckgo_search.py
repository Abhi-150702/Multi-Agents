from langchain.tools import tool
from ddgs import DDGS
from config.logging_config import setup_logger, log_tool_call, log_tool_output, log_tool_error

logger = setup_logger("duckduckgo_search")

@tool
def duckduckgo_search(query: str) -> str:
    """
    Search the web using DuckDuckGo.

    Use this tool when you need current information from the internet.
    """
    try:
        log_tool_call(logger, "duckduckgo_search", query=query)

        results = DDGS().text(
            query,
            max_results = 5
        )

        if not results:
            no_result_msg = 'No search results found'
            log_tool_output(logger, "duckduckgo_search", no_result_msg, success=True)
            return no_result_msg

        formatted_results = []

        for result in results:
            formatted_results.append(
                f"""
Title : {result.get('title', '')}
URL : {result.get('href', '')}
Snippet : {result.get('body', '')}
"""
            )

        final_result = '--'.join(formatted_results)
        log_tool_output(logger, "duckduckgo_search", final_result, success=True)
        return final_result

    except Exception as e:
        log_tool_error(logger, "duckduckgo_search", e)
        error_msg = f"Error performing DuckDuckGo search: {str(e)}"
        log_tool_output(logger, "duckduckgo_search", error_msg, success=False)
        return error_msg