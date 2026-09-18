from langchain.tools import tool
import json
import requests
from config.logging_config import setup_logger, log_tool_call, log_tool_output, log_tool_error

GITHUB_API = "https://api.github.com"
logger = setup_logger("github_search")


@tool
def github_search(query: str, max_results: int =5) -> str:
    """
    Search public GitHub repositories.

    Use this tool when:
    - the user asks about open-source implementations
    - code repositories are relevant
    - the user wants examples of a technology
    - a research topic has useful GitHub implementations

    This uses the public GitHub API and does not require a GitHub
    token for basic searches.

    Returns repository name, description, URL, language,
    stars, forks and last update time.
    """

    try:
        log_tool_call(logger, "github_search", query=query, max_results=max_results)

        url = f"{GITHUB_API}/search/repositories"

        params = {
            'q' : query,
            'per_page' : min(max_results, 10),
            'sort' : 'stars',
            'order' : 'desc'
        }

        headers = {
            'Accept' : 'application/vnd.github+json',
            'User-Agent' : 'Agentic-AI-Research-Agent'
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        repositories = []

        for repo in data.get("items", []):
            repositories.append({
                "name": repo.get("full_name"),
                "description": repo.get("description"),
                "url": repo.get("html_url"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count"),
                "forks": repo.get("forks_count"),
                "open_issues": repo.get("open_issues_count"),
                "updated_at": repo.get("updated_at"),
            })

        result = json.dumps(
            {
                'query' : query,
                'total_results' : data.get('total_count'),
                'repositories' : repositories
            },
            indent = 4,
            ensure_ascii=False
        )

        log_tool_output(logger, "github_search", result, success=True)
        return result

    except requests.RequestException as exc:
        log_tool_error(logger, "github_search", exc)
        error_result = json.dumps(
            {
                "error" : f"GitHub API request failed: {str(exc)}"
            }
        )
        log_tool_output(logger, "github_search", error_result, success=False)
        return error_result

    except Exception as exc:
        log_tool_error(logger, "github_search", exc)
        error_result = json.dumps(
            {
                'error' : f"GitHub search failed: {str(exc)}"
            }
        )
        log_tool_output(logger, "github_search", error_result, success=False)
        return error_result