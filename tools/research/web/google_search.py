from langchain_google_community.search import GoogleSearchAPIWrapper
from langchain.tools import tool
from config.settings import Settings
from config.logging_config import setup_logger, log_tool_call, log_tool_output, log_tool_error

search = GoogleSearchAPIWrapper(
    k=5,
    google_api_key=Settings().google_api_key,
    google_cse_id=Settings().google_cse_id
)
logger = setup_logger("google_search")


@tool
def google_search(query: str, num_results: int = 5) -> str:
    """
    Search Google for web results.
    Useful for broad web research and finding official documentation.
    """
    try:
        log_tool_call(logger, "google_search", query=query)

        results = search.results(query=query, num_results=num_results)

        formatted_results = []
        for result in results:
            formatted_results.append(
                f"""
Title: {result.get('title', '')}
URL: {result.get("link", '')}
Snippet: {result.get('snippet', '')}
"""
            )

        final_result = "--".join(formatted_results)
        log_tool_output(logger, "google_search", final_result, success=True)
        return final_result

    except Exception as e:
        log_tool_error(logger, "google_search", e)
        error_msg = f"Error performing Google search: {str(e)}"
        log_tool_output(logger, "google_search", error_msg, success=False)
        return error_msg
