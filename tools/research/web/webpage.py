import json
import requests

from bs4 import BeautifulSoup
from langchain_core.tools import tool
from config.logging_config import setup_logger, log_tool_call, log_tool_output, log_tool_error

logger = setup_logger("read_webpage")


@tool
def read_webpage(
    url: str,
    max_characters: int = 5000
) -> str:
    """
    Read and extract textual content from a public webpage.

    Use this tool when:
    - a search result contains a useful URL
    - deeper information is needed from a webpage
    - the search result snippet is insufficient
    - an academic paper HTML page needs to be inspected
    - documentation or technical articles need to be read

    Input must be a complete HTTP or HTTPS URL.

    This tool retrieves publicly accessible webpages and does not
    require a paid API.
    """

    try:
        log_tool_call(logger, "read_webpage", url=url, max_characters=max_characters)

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/140 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=120,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove non-content elements
        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "noscript",
            "svg",
        ]):
            element.decompose()

        # Try to focus on the main content
        main = soup.find("main")

        if main:
            text = main.get_text(
                separator="\n",
                strip=True
            )
        else:
            text = soup.get_text(
                separator="\n",
                strip=True
            )

        # Remove excessive blank lines
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        text = "\n".join(lines)

        result = json.dumps({
            "url": url,
            "content": text[:max_characters],
        }, indent=2, ensure_ascii=False)

        log_tool_output(logger, "read_webpage", result, success=True)
        return result

    except requests.RequestException as exc:
        log_tool_error(logger, "read_webpage", exc)
        error_result = json.dumps({
            "url": url,
            "error": f"Failed to retrieve webpage: {str(exc)}"
        })
        log_tool_output(logger, "read_webpage", error_result, success=False)
        return error_result

    except Exception as exc:
        log_tool_error(logger, "read_webpage", exc)
        error_result = json.dumps({
            "url": url,
            "error": f"Webpage extraction failed: {str(exc)}"
        })
        log_tool_output(logger, "read_webpage", error_result, success=False)
        return error_result