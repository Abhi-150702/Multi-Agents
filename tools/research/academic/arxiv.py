from langchain.tools import tool
from langchain_community.utilities import ArxivAPIWrapper
from config.logging_config import setup_logger, log_tool_call, log_tool_output, log_tool_error

arxiv = ArxivAPIWrapper(top_k_results=5, load_max_docs=5)
logger = setup_logger("arxiv_search")

@tool
def arxiv_search(query: str) -> str:
    """
    Search academic papers on arXiv.

    Use this tool when:
    - the user asks about research papers or when the google search of duckduckgo search is not enough
    - the user asks about algorithms or academic methods
    - the user asks for recent scientific research
    - evidence from academic literature is useful

    Do not use this tool for general web searches.
    """

    try:
        log_tool_call(logger, "arxiv_search", query=query)
        result = arxiv.run(query)
        log_tool_output(logger, "arxiv_search", result, success=True)
        return result
    except Exception as e:
        log_tool_error(logger, "arxiv_search", e)
        error_msg = f"Error searching arXiv: {str(e)}"
        log_tool_output(logger, "arxiv_search", error_msg, success=False)
        return error_msg